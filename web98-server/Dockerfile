# 1998 Web Stack (Apache 1.3.x + Perl 5.005_03 + MySQL 3.23 client)
# Base: Debian Stretch (9.0) for build tooling; we compile period-appropriate sources.

FROM debian:stretch

# Build toolchain
RUN echo 'deb http://archive.debian.org/debian stretch main' > /etc/apt/sources.list && \
    echo 'deb http://archive.debian.org/debian-security stretch/updates main' >> /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until \"false\";' > /etc/apt/apt.conf.d/99no-check-valid-until && \
    apt-get update && \
    apt-get install -y --force-yes \
    gcc \
    g++ \
    make \
    wget \
    gzip \
    tar \
    libncurses5-dev \
    bison \
    flex \
    automake \
    gawk \
    procps \
    perl \
    libcgi-pm-perl

# -----------------------------------------------------------------------------
# 1. Compile MySQL 3.23.58 client libs (close to 1998 protocol, readily available)
# -----------------------------------------------------------------------------
WORKDIR /usr/src
RUN wget http://download.nust.na/pub2/openpkg1/sources/DST/mysql3/mysql-3.23.58.tar.gz && \
    tar xzf mysql-3.23.58.tar.gz && \
    cp /usr/share/automake-*/config.guess mysql-3.23.58/config.guess && \
    cp /usr/share/automake-*/config.sub mysql-3.23.58/config.sub

WORKDIR /usr/src/mysql-3.23.58
# Patch configure for modern pthread/NPTL detection
RUN sed -i 's/LinuxThreads/pthread/g' configure && \
    sed -i 's/Linuxthreads/pthread/g' configure && \
    sed -i 's/gethostbyname_r((A),(B),(C),(D),(E))/({ struct hostent *__r; gethostbyname_r((A),(B),(C),(D),\\&__r,(E)); __r; })/' include/my_net.h && \
    sed -i 's/((a) >? (b))/((a) > (b) ? (a) : (b))/g' include/global.h && \
    sed -i 's/((a) <? (b))/((a) < (b) ? (a) : (b))/g' include/global.h

RUN CFLAGS="-std=gnu89 -O0" CXXFLAGS="-O0" ./configure \
    --prefix=/usr/local/mysql \
    --without-server \
    --enable-thread-safe-client \
    --with-charset=latin1 \
    ac_cv_ps_var="ps -p"

RUN cp config.h include/my_config.h && \
    sed -i 's|.*cp ../config.h my_config.h.*|echo \"Skipping cp\"|' include/Makefile

RUN make CFLAGS="-std=gnu89 -O0" CXXFLAGS="-O0" && make install && \
    echo "/usr/local/mysql/lib/mysql" > /etc/ld.so.conf.d/mysql.conf && \
    ldconfig
ENV LD_LIBRARY_PATH="/usr/local/mysql/lib/mysql:$LD_LIBRARY_PATH"
ENV PATH="/usr/local/mysql/bin:$PATH"

# -----------------------------------------------------------------------------
# 2. Compile Apache 1.3.4 (1999)
# -----------------------------------------------------------------------------
WORKDIR /usr/src
RUN wget http://archive.apache.org/dist/httpd/apache_1.3.4.tar.gz && \
    tar xzf apache_1.3.4.tar.gz && \
    cp /usr/share/automake-*/config.guess apache_1.3.4/src/config.guess && \
    cp /usr/share/automake-*/config.sub apache_1.3.4/src/config.sub

WORKDIR /usr/src/apache_1.3.4
# Fix 'getline' conflict with modern glibc
RUN sed -i 's/getline/apache_getline/g' src/support/htdigest.c && \
    sed -i 's/getline/apache_getline/g' src/support/htpasswd.c && \
    sed -i 's/getline/apache_getline/g' src/support/logresolve.c && \
    sed -i 's/getline/apache_getline/g' src/main/http_protocol.c

RUN CFLAGS="-std=gnu89 -O0" bash ./configure \
    --prefix=/usr/local/apache \
    --enable-module=so
RUN make && make install

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Configuration (CGI only)
# -----------------------------------------------------------------------------
RUN { \
      echo "AddHandler cgi-script .cgi"; \
      echo "DirectoryIndex index.cgi index.html"; \
      echo "Options Indexes FollowSymLinks ExecCGI"; \
      echo "ServerName 127.0.0.1"; \
    } >> /usr/local/apache/conf/httpd.conf && \
    sed -i 's#Options Indexes FollowSymLinks#Options Indexes FollowSymLinks ExecCGI#g' /usr/local/apache/conf/httpd.conf && \
    grep -v -E 'php3_module|libphp\\.so|AddModule.*php3|AddType application/x-httpd-php' /usr/local/apache/conf/httpd.conf > /tmp/httpd.conf && \
    mv /tmp/httpd.conf /usr/local/apache/conf/httpd.conf

# Traffic shaping tool
RUN apt-get install -y --force-yes iproute2

RUN echo '#!/bin/bash' > /start.sh && \
    echo '# Traffic Control: 48kbps, ~250ms latency (dial-up feel)' >> /start.sh && \
    echo 'export PATH=/usr/local/mysql/bin:$PATH' >> /start.sh && \
    echo 'tc qdisc add dev eth0 root tbf rate 48kbit burst 10kb latency 250ms' >> /start.sh && \
    echo '/usr/local/apache/bin/apachectl start' >> /start.sh && \
    echo 'tail -f /usr/local/apache/logs/error_log' >> /start.sh && \
    chmod +x /start.sh

CMD ["/start.sh"]
