**Role:** You are a Lead DevOps Architect and Digital Archaeologist specializing in Legacy System Emulation.

**Objective:**
Build a Dockerized **WAP 2.0 (XHTML-MP)** simulation environment capable of running on **Apple Silicon (ARM64)**. The environment must strictly utilize the **LAMP stack from the year 2001**.

---

## Constraints & Tech Stack

1.  **Architecture:** The host is ARM64. You must use `platform: linux/amd64` for the server containers to support legacy binaries.
2.  **Web Server:** **Apache 1.3** (Strict requirement. Do not use Nginx. Do not use Apache 2).
3.  **Language:** **PHP 4.0.x** (If 4.0 is impossible to compile/find, acceptable fallback is the earliest working PHP 4.x, but prioritize 4.0).
4.  **Database:** **MySQL 3.23** (Legacy image required).
5.  **Client:** A generic Firefox container (KasmVNC) for viewing the content.
6.  **No Modern Software:** All software must be from the year 2001 or earlier. No modern helper tools like `curl` (unless it was in the base image).

---

## Required Deliverables

### 1. `docker-compose.yml`

- Define three services: `wap-server` (Apache/PHP), `wap-db` (MySQL), and `wap-client` (Firefox).
- **Networking:** All containers must communicate on an internal bridge network called `wap-net`.
- **Volumes:**
  - Mount local `./content` to the Apache Web Root (e.g., `/var/www/html`).
  - Mount local `./db-init` to a location accessible by the `wap-db` container.
- **Client Automation:**
  - Mount a `policies.json` or `user.js` into the Firefox container to pre-set the User Agent to: `Nokia6600/1.0 (5.27.0) SymbianOS/7.0s Series60/2.0 Profile/MIDP-2.0 Configuration/CLDC-1.0`.
  - **Window Size:** Configure the container (e.g. KasmVNC arguments) to launch with a small window size (e.g. 240x320) to mimic a phone screen.
- **Dependencies:** Ensure `wap-server` waits for `wap-db` to be healthy before starting (use `depends_on` with `condition: service_healthy` if the legacy image supports it, otherwise use a wrapper script).

---

### 2. `wap-server/Dockerfile` (The Hard Part)

- **Base Image:** Use a Debian Woody (3.0) or Potato (2.2) image from `archive.debian.org`. Update `sources.list` to point to valid archive URLs.
- **Compiler:** You must use the GCC version native to that era (GCC 2.95 or 3.0).
- **Source Compilation:** If the Debian archives are incomplete, you must script the compilation of Apache 1.3 and PHP 4 from source tarballs (available from `archive.org` or Apache's archive).
- **Kernel Compatibility:** Acknowledge that running 2001 userland on a modern kernel is risky. Attempt to use `setarch` or `linux32` wrappers if available.
- **MIME Types:** Configure Apache to serve WAP MIME types in `httpd.conf` or `.htaccess`:
  - `.xhtml` -> `application/vnd.wap.xhtml+xml`
  - `.wbmp` -> `image/vnd.wap.wbmp`
  - `.wml` -> `text/vnd.wap.wml`
- **Logging:** Configure Apache's `ErrorLog` to output to `/dev/stderr` so debugging is possible via `docker logs`.

---

### 3. `db-init/init-db.sh`

- Legacy MySQL 3.23 images **do not** support `docker-entrypoint-initdb.d`.
- Write a shell script that:
  1.  Waits for MySQL to be ready (loop with `mysqladmin ping`).
  2.  Creates the database if it doesn't exist.
  3.  Imports `schema.sql` using the `mysql` client.
- This script should be the `command:` or `entrypoint:` override for the `wap-db` service.

---

### 4. `content/index.xhtml` & Visuals

- Create a file that strictly adheres to **XHTML Mobile Profile 1.0**.
- **CSS:** Embed or link CSS to mimic a **Nokia 6600** display:
  - Canvas width: **176px**.
  - Canvas height: **208px**.
  - Font: Monospace/Bitmap style (`font-family: monospace; font-size: 10px;`).
  - Colors: 4096 color palette aesthetic (high contrast).
  - Active Links: Invert colors (Black background, White text) to simulate "d-pad navigation focus" (`:focus { background: #000; color: #FFF; }`).

---

### 5. `content/db-connect.php`

- A script to prove the stack is genuine.
- Use `mysql_connect()` (the old, deprecated extension).
- Print the **PHP Version** (`phpversion()`) and **MySQL Server Version** (`mysql_get_server_info()`) to the screen.

---

### 6. Post-Setup Guide

- **Network Simulation (The "Pure" Way):**
  - Do NOT use client-side throttling (Firefox Dev Tools).
  - Use **`tc` (Traffic Control)** from the `iproute` package (standard in Linux 2.2/2.4).
  - Create a startup script (`throttle.sh`) that uses `tc` to limit the interface bandwidth to **GPRS speeds (40kbps)** and adds **800ms latency**.
  - Example: `tc qdisc add dev eth0 root tbf rate 40kbit burst 10kb latency 800ms`.
- **Verification Commands:**
  - `php -v` (should show PHP 4.0.x).
  - `httpd -v` or `apache -v` (should show Apache/1.3.x).
  - `mysql --version` (should show Ver 9.x or 10.x for MySQL 3.23).

---

## Output Structure

Provide the following in order:

1.  **Directory Tree:** Show the complete project structure.
2.  **Code Blocks:** Provide the full content of each file.
3.  **Post-Setup Guide:** Text instructions for verification.

Ensure the Dockerfile is robust enough to build despite the age of the software. Acknowledge any known issues or workarounds.

---

## Integration Notes

> [!IMPORTANT]
> This environment is designed to run the **LoveLink 2000** application defined in `love-link-2000.md`. Ensure the `init-db.sh` script is compatible with the `schema.sql` generated by that application.

---
