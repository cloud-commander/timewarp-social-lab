#!/bin/bash

# Add compiled MySQL bin to PATH
export PATH="/usr/local/mysql/bin:$PATH"

# Start MySQL in background
# In 3.23, safe_mysqld is the wrapper.
echo "Starting safe_mysqld..."
/usr/local/mysql/bin/safe_mysqld --user=mysql &
pid="$!"

# Wait for MySQL to start (root password may already be set in data dir)
echo "Waiting for MySQL to start..."
until mysqladmin -uroot -ppassword ping --silent >/dev/null 2>&1; do
    # fallback attempt without password in case of a brand-new datadir
    if mysqladmin ping --silent >/dev/null 2>&1; then
        break
    fi
    echo "MySQL is unavailable - sleeping"
    sleep 1
done

echo "MySQL is up - executing init"

# Create Database
mysql -u root -ppassword -e "CREATE DATABASE IF NOT EXISTS lovelink;"
mysql -u root -ppassword -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;"
mysql -u root -ppassword -e "FLUSH PRIVILEGES;"

# Set root password (initially empty)
# mysqladmin -u root password 'password'
# But we need to do this AFTER creating DB if we want to use password in next steps.
# Let's set it at the end or use it now.
# If we set it now, subsequent commands need -ppassword.

# Import Schema if it exists
if [ -f /docker-entrypoint-initdb.d/schema.sql ]; then
    echo "Importing schema..."
    mysql -u root -ppassword lovelink < /docker-entrypoint-initdb.d/schema.sql
fi

echo "Initialization complete. MySQL running."

# Wait for process
wait "$pid"
