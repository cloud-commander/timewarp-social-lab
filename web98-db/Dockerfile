# MySQL 3.22.x (1998-era) on Debian Stretch build base
# Purpose: standalone DB container for the web98 stack without touching WAP services.

FROM debian:stretch

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
    procps

WORKDIR /usr/src
RUN wget http://download.nust.na/pub2/openpkg1/sources/DST/mysql3/mysql-3.23.58.tar.gz && \
    tar xzf mysql-3.23.58.tar.gz && \
    cp /usr/share/automake-*/config.guess mysql-3.23.58/config.guess && \
    cp /usr/share/automake-*/config.sub mysql-3.23.58/config.sub

WORKDIR /usr/src/mysql-3.23.58
RUN sed -i 's/LinuxThreads/pthread/g' configure && \
    sed -i 's/Linuxthreads/pthread/g' configure && \
    sed -i 's/gethostbyname_r((A),(B),(C),(D),(E))/({ struct hostent *__r; gethostbyname_r((A),(B),(C),(D),\\&__r,(E)); __r; })/' include/my_net.h && \
    sed -i 's/((a) >? (b))/((a) > (b) ? (a) : (b))/g' include/global.h && \
    sed -i 's/((a) <? (b))/((a) < (b) ? (a) : (b))/g' include/global.h

RUN CFLAGS="-std=gnu89 -O0" CXXFLAGS="-O0" ./configure \
    --prefix=/usr/local/mysql \
    --with-charset=latin1 \
    --with-extra-charsets=none \
    --enable-thread-safe-client \
    --with-mysqld-user=mysql \
    --without-bench \
    --without-docs \
    --without-man \
    ac_cv_ps_var="ps -p"

RUN cp config.h include/my_config.h && \
    sed -i 's|.*cp ../config.h my_config.h.*|echo \"Skipping cp\"|' include/Makefile

RUN make CFLAGS="-std=gnu89 -O0" CXXFLAGS="-O0" && make install

RUN groupadd mysql && useradd -g mysql mysql

RUN /usr/local/mysql/bin/mysql_install_db --user=mysql

RUN chown -R root /usr/local/mysql && \
    chown -R mysql /usr/local/mysql/var && \
    chgrp -R mysql /usr/local/mysql

EXPOSE 3306
ENV PATH="/usr/local/mysql/bin:${PATH}"

CMD ["/docker-entrypoint-initdb.d/init-db.sh"]
