# Strict 2001 Compliance
# Base: Debian Stretch (9.0) - Jessie (8.0) dpkg crashes on ARM64 emulation.
# We use Stretch as a build base but compile strict 2001 software.

FROM debian:stretch

# Install build dependencies
# Install build dependencies
# We use standard GCC from Stretch.
RUN echo 'deb http://archive.debian.org/debian stretch main' > /etc/apt/sources.list && \
    echo 'deb http://archive.debian.org/debian-security stretch/updates main' >> /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until && \
    apt-get update && \
    apt-get install -y --force-yes \
    gcc \
    g++ \
    make \
    wget \
    gzip \
    tar \
    libncurses5-dev \
    libxml2-dev \
    bison \
    flex \
    automake \
    gawk \
    procps

# -----------------------------------------------------------------------------
# 1. Compile MySQL 3.23.58 Client Libs (For PHP)
# -----------------------------------------------------------------------------
# We cannot use Stretch's libmysqlclient-dev (too new for PHP 4.0).
WORKDIR /usr/src
# Download MySQL 3.23.58 and updated config scripts for ARM64 support
RUN wget http://download.nust.na/pub2/openpkg1/sources/DST/mysql3/mysql-3.23.58.tar.gz && \
    tar xzf mysql-3.23.58.tar.gz && \
    cp /usr/share/automake-*/config.guess mysql-3.23.58/config.guess && \
    cp /usr/share/automake-*/config.sub mysql-3.23.58/config.sub

WORKDIR /usr/src/mysql-3.23.58
# Configure for client only, static link
# Patch configure to ignore LinuxThreads check (Debian Stretch uses NPTL)
RUN sed -i 's/LinuxThreads/pthread/g' configure && \
    sed -i 's/Linuxthreads/pthread/g' configure && \
    sed -i 's/gethostbyname_r((A),(B),(C),(D),(E))/({ struct hostent *__r; gethostbyname_r((A),(B),(C),(D),\&__r,(E)); __r; })/' include/my_net.h && \
    sed -i 's/((a) >? (b))/((a) > (b) ? (a) : (b))/g' include/global.h && \
    sed -i 's/((a) <? (b))/((a) < (b) ? (a) : (b))/g' include/global.h
RUN CFLAGS="-std=gnu89 -O0" CXXFLAGS="-O0" ./configure \
    --prefix=/usr/local/mysql \
    --without-server \
    --enable-thread-safe-client \
    --with-charset=latin1 \
    ac_cv_ps_var="ps -p"

# Manually copy config.h to avoid make segfault on "link_sources" target
RUN cp config.h include/my_config.h && \
    sed -i 's/.*cp ..\/config.h my_config.h.*/echo "Skipping cp"/' include/Makefile

RUN make CFLAGS="-std=gnu89 -O0" CXXFLAGS="-O0" && make install && \
    echo "/usr/local/mysql/lib/mysql" > /etc/ld.so.conf.d/mysql.conf && \
    ldconfig
ENV LD_LIBRARY_PATH="/usr/local/mysql/lib/mysql:$LD_LIBRARY_PATH"

# -----------------------------------------------------------------------------
# 2. Compile Apache 1.3.20
# -----------------------------------------------------------------------------
WORKDIR /usr/src
RUN wget http://archive.apache.org/dist/httpd/apache_1.3.20.tar.gz && \
    tar xzf apache_1.3.20.tar.gz && \
    cp /usr/share/automake-*/config.guess apache_1.3.20/src/config.guess && \
    cp /usr/share/automake-*/config.sub apache_1.3.20/src/config.sub

WORKDIR /usr/src/apache_1.3.20
# Fix 'getline' conflict with modern glibc
RUN sed -i 's/getline/apache_getline/g' src/support/htdigest.c && \
    sed -i 's/getline/apache_getline/g' src/support/htpasswd.c && \
    sed -i 's/getline/apache_getline/g' src/support/logresolve.c && \
    sed -i 's/getline/apache_getline/g' src/main/http_protocol.c

# Configure and Install
# We use -std=gnu89 to avoid issues with inline functions in GCC 5+
# We use -O0 to avoid GCC segfaults on ARM64 emulation.
RUN CFLAGS="-std=gnu89 -O0" bash ./configure \
    --prefix=/usr/local/apache \
    --enable-module=so
RUN make && make install

# -----------------------------------------------------------------------------
# 3. Compile PHP 4.0.6
# -----------------------------------------------------------------------------
WORKDIR /usr/src
RUN wget http://museum.php.net/php4/php-4.0.6.tar.gz && \
    tar xzf php-4.0.6.tar.gz && \
    cp /usr/share/automake-*/config.guess php-4.0.6/config.guess && \
    cp /usr/share/automake-*/config.sub php-4.0.6/config.sub

WORKDIR /usr/src/php-4.0.6
# Configure with our compiled MySQL and Apache
# Note: --with-mysql=/usr/local/mysql points to our custom build
RUN CFLAGS="-std=gnu89 -O0" ./configure \
    --with-mysql=/usr/local/mysql \
    --with-apxs=/usr/local/apache/bin/apxs \
    --disable-libxml \
    --enable-track-vars
RUN make && make install

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
# Copy php.ini
RUN cp php.ini-dist /usr/local/lib/php.ini

# Configure Apache
RUN echo "AddType application/x-httpd-php .php" >> /usr/local/apache/conf/httpd.conf && \
    echo "AddType application/vnd.wap.xhtml+xml .xhtml" >> /usr/local/apache/conf/httpd.conf && \
    echo "AddType image/vnd.wap.wbmp .wbmp" >> /usr/local/apache/conf/httpd.conf && \
    echo "AddType text/vnd.wap.wml .wml" >> /usr/local/apache/conf/httpd.conf

# Install iproute2 for 'tc' (Traffic Control)
RUN apt-get install -y --force-yes iproute2

# Create startup script
RUN echo '#!/bin/bash' > /start.sh && \
    echo '# Traffic Control: 40kbps, 800ms latency' >> /start.sh && \
    echo 'tc qdisc add dev eth0 root tbf rate 40kbit burst 10kb latency 800ms' >> /start.sh && \
    echo '/usr/local/apache/bin/apachectl start' >> /start.sh && \
    echo 'tail -f /usr/local/apache/logs/error_log' >> /start.sh && \
    chmod +x /start.sh

CMD ["/start.sh"]
