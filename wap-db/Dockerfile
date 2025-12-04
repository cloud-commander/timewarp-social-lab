# MySQL 3.23.58 (Last of 3.23 series)
# Debian Potato (2.2) is missing. Jessie (8.0) crashes on ARM64.
# We use Debian Stretch (9.0) as a build base.
# We strictly compile the 2001 software (MySQL 3.23)

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
    bison \
    flex \
    automake \
    procps

# Download MySQL 3.23.58
WORKDIR /usr/src
# Using a mirror or archive since official might be gone.
# MySQL archives usually keep old versions.
# Using a mirror since official archives removed it.
# Download MySQL 3.23.58 and updated config scripts for ARM64 support
RUN wget http://download.nust.na/pub2/openpkg1/sources/DST/mysql3/mysql-3.23.58.tar.gz && \
    tar xzf mysql-3.23.58.tar.gz && \
    cp /usr/share/automake-*/config.guess mysql-3.23.58/config.guess && \
    cp /usr/share/automake-*/config.sub mysql-3.23.58/config.sub

# Compile MySQL
WORKDIR /usr/src/mysql-3.23.58
# Patch configure to ignore LinuxThreads check (Debian Stretch uses NPTL)
RUN sed -i 's/LinuxThreads/pthread/g' configure && \
    sed -i 's/Linuxthreads/pthread/g' configure && \
    sed -i 's/gethostbyname_r((A),(B),(C),(D),(E))/({ struct hostent *__r; gethostbyname_r((A),(B),(C),(D),\&__r,(E)); __r; })/' include/my_net.h && \
    sed -i 's/((a) >? (b))/((a) > (b) ? (a) : (b))/g' include/global.h && \
    sed -i 's/((a) <? (b))/((a) < (b) ? (a) : (b))/g' include/global.h

# Configure for static linking to avoid lib issues, and basic setup
# We use -std=gnu89 for GCC 6 compatibility.
# We use -O0 to avoid GCC segfaults on ARM64 emulation.
# We pass ac_cv_ps_var to fix "Could not find the right ps switches" error.
# We remove -std=gnu89 from CXXFLAGS to avoid "long long" errors in C++ checks.
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

# Manually copy config.h to avoid make segfault on "link_sources" target
RUN cp config.h include/my_config.h && \
    sed -i 's/.*cp ..\/config.h my_config.h.*/echo "Skipping cp"/' include/Makefile

RUN make CFLAGS="-std=gnu89 -O0" CXXFLAGS="-O0" && make install

# Setup User
RUN groupadd mysql && useradd -g mysql mysql

# Initialize DB
RUN /usr/local/mysql/bin/mysql_install_db --user=mysql

# Setup Permissions
RUN chown -R root /usr/local/mysql && \
    chown -R mysql /usr/local/mysql/var && \
    chgrp -R mysql /usr/local/mysql

# Expose Port
EXPOSE 3306

# Add bin to path
ENV PATH="/usr/local/mysql/bin:${PATH}"

# Copy init script (we'll use the one we made, but we need to adapt it)
# The init-db.sh expects to run mysqld.
# We will just use the init-db.sh as the command.

CMD ["/docker-entrypoint-initdb.d/init-db.sh"]
