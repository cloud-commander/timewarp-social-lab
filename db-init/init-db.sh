#!/bin/bash

# Add compiled MySQL bin to PATH
export PATH="/usr/local/mysql/bin:$PATH"

# Start MySQL in background
# In 3.23, safe_mysqld is the wrapper.
echo "Starting safe_mysqld..."
/usr/local/mysql/bin/safe_mysqld --user=mysql &
pid="$!"

# Wait for MySQL to start
echo "Waiting for MySQL to start..."
# We need to specify socket or host. localhost should work if socket is standard.
# Compiled default socket might be /tmp/mysql.sock.
until mysqladmin ping --silent; do
    echo "MySQL is unavailable - sleeping"
    sleep 1
done

echo "MySQL is up - executing init"

# Create Database
mysql -u root -e "CREATE DATABASE IF NOT EXISTS lovelink;"
mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;"
mysql -u root -e "FLUSH PRIVILEGES;"

# Set root password (initially empty)
# mysqladmin -u root password 'password'
# But we need to do this AFTER creating DB if we want to use password in next steps.
# Let's set it at the end or use it now.
# If we set it now, subsequent commands need -ppassword.

# Import Schema if it exists
if [ -f /docker-entrypoint-initdb.d/schema.sql ]; then
    echo "Importing schema..."
    mysql -u root lovelink < /docker-entrypoint-initdb.d/schema.sql
fi

# Secure it (Set password)
echo "Setting root password..."
mysqladmin -u root password 'password'

echo "Initialization complete. MySQL running."

# Wait for process
wait "$pid"
