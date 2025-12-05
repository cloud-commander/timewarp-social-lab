# Timewarp Social Lab

This repository is a historical recreation of two separate, intentionally legacy web stacks:

- A 2001-era WAP-style swipe app (Tinder-like) — the `wap-*` stack, content under `content/`.
- A 1998-era Web social site (Facebook-like) — the `web98-*` stack, content under `content-web98/`.

Both stacks are provided as educational artifacts and run in Docker containers to reproduce the original-era runtime constraints.

### Why "Timewarp Social Lab"?

We’re testing the hypothesis that the core ideas behind later-era hits (Facebook, Tinder) were technically achievable several years earlier using period-appropriate tools. By assembling both a 1998 desktop web stack (Perl CGI + MySQL 3.2x + Apache 1.3.x) and a 2001 WAP stack (PHP4 + MySQL 3.23), we show that nothing in the protocols or runtimes fundamentally blocked these social patterns—only timing, polish, and distribution.

### Could someone have built Facebook/Tinder years earlier?

- **Yes, at small scale.** The CRUD, session, and relational pieces required for profiles, feeds, likes, and messaging were all available in the late ’90s. A motivated team could have launched campus-scale (or niche) social networks with these stacks.
- **Constraints that would bite:**
  - Bandwidth/latency: 28.8–56k dial-up or early GPRS makes rich media painful; feeds would be text-first with tiny JPEGs/GIFs.
  - Hardware costs: Scaling beyond one or two boxes would be expensive; MySQL pre-transactional MyISAM lacked safety/replication maturity.
  - Device UX: WAP phones and 640×480 desktops limit the “swipe” feel; interaction would be more link-and-refresh than touch-first.
- **Conclusion:** Feasible in function, harder in adoption. The tech stack wasn’t the blocker—network effects, hardware cost, and user device ergonomics were.

--

## Quick Start

Prerequisites: Docker and Docker Compose installed, Python 3 (for mock-data script) and `pip` to install `Pillow` if you regenerate images.

From the repository root:

```zsh
# Build and start both stacks
docker-compose up --build

# To run in background (detached)
docker-compose up --build -d

# Watch logs for a specific service (example)
docker-compose logs -f wap-server
```

Web UIs after startup:

- WAP (Tinder-like): http://localhost:8080/
- Web98 (Facebook-like): http://localhost:8081/

Re-generate mock users and images (optional):

```zsh
# Activate repo venv if desired (venv-local exists)
source venv-local/bin/activate
pip install pillow
python scripts/generate_mock_data.py

# After generating, re-seed or import the generated SQL into the container DB as needed
# Example: exec into the wap-db container and import the generated SQL
docker exec -it wap-db sh
# inside container shell
mysql lovelink < /docker-entrypoint-initdb.d/seed_users.sql
```

--

## Project Overview (Executive Summaries)

### WAP — 2001-era Tinder clone (primary files in `content/`)

- Purpose: A compact WAP-style mobile swipe app built with classic PHP (PHP4-era patterns) to emulate early mobile interactions and constraints.
- Key behavior:
  - `content/index.php` shows a single candidate to the user (excludes self, prior likes/passes, and blocked users).
  - `content/action.php` records `pass` or `date` in the `likes` table and creates a `matches` row when two users mutually `date`.
  - Authentication via `content/login.php` / `content/register.php` using MD5-hashed passwords stored in `users`.
  - Photos are recorded in `user_photos` with a primary-photo flag; `img_gen.php` supplies placeholders where needed.
  - `content/init.php` includes a `usleep()` call to intentionally simulate GPRS latency for UI testing.
- Runtime: `wap-server` (Apache + PHP) and `wap-db` (MySQL) in Docker Compose; content is mounted from `content/`.
- Mock data: `scripts/generate_mock_data.py` produces 96×96 avatars and `content/seed_users.sql`.

Limitations & risks (WAP):

- Legacy APIs: uses `mysql_*` calls and legacy session globals (`$HTTP_POST_VARS`, `session_register`) — incompatible with modern PHP without shims.
- Security: SQL string interpolation (limited escaping), MD5 password storage, no CSRF protections — vulnerable to SQL injection and weak authentication.
- Scalability: single-row selection (`LIMIT 1`), no pagination, potential race conditions on match creation, no background workers.
- Testing: No unit tests or automated integration tests; DB init relies on manual container init scripts.

Files to inspect when changing behavior: `content/index.php`, `content/action.php`, `content/init.php`, `content/db.php`, `content/schema.sql`, `scripts/generate_mock_data.py`.

### Web98 — 1998-era Facebook clone (primary files in `content-web98/`)

- Purpose: A Web98-style social site implemented with Perl CGI and server-rendered pages to preserve late-1990s web constraints.
- Key behavior:
  - CGI endpoints: `feed.cgi`, `profile.cgi`, `friends.cgi`, `messages.cgi`, `login.cgi`, `signup.cgi` implement the social flows.
  - `content-web98/lib.pl` contains shared utilities used by the CGI scripts (session helpers, DB access utilities).
  - Static HTML scaffolding and image directories under `content-web98/` reproduce the look-and-feel of that era.
- Runtime: `web98-server` (Apache + CGI/Perl) and `web98-db` (MySQL); content is mounted from `content-web98/` and the site is exposed at port 8081.

Limitations & risks (Web98):

- Performance: CGI spawns per-request process overhead — not suited to high traffic without changes.
- Legacy runtime: May depend on older Perl modules/behaviors; the Docker images here mitigate host compatibility but require containerized runtime.
- Security & maintainability: Similar risks as WAP — string-interpolated SQL, likely weak input sanitization, and limited auth hardening.
- Period note: the application code itself is written to be 1998-safe (no `use warnings`, no modern Perl operators, CGI.pm-era APIs), but for time we currently run it on a newer base (Apache 1.3.4 from 1999 and MySQL 3.23.58 from 2003). Dropping those to 1998-grade versions is straightforward if desired; the code should still run unchanged.

Files to inspect when changing behavior: `content-web98/lib.pl`, the `*.cgi` scripts (e.g., `feed.cgi`, `profile.cgi`), and `db-init-web98/init-db.sh`.

--

## Architecture & Dev Notes

- The repo intentionally contains two _separate_ historical stacks; they are not integrated and use separate databases and containers (`wap-db` vs `web98-db`).
- Docker Compose is the primary way to run both stacks together for local testing; service hostnames (`wap-db`, `web98-db`) are referenced directly by `content/db.php` and `content-web98` scripts.
- DB initialization is handled by the `db-init/` and `db-init-web98/` directories; updates to schema or seed data should be mirrored into these init scripts to allow container re-seed.

Developer conventions and constraints to respect:

- Preserve legacy session and global semantics unless you intend to modernize the entire call graph (e.g., `session_register`, `$HTTP_SESSION_VARS`).
- Avoid bulk replacement of `mysql_*` calls in a single PR — prefer incremental changes, compatibility shims, and tests.
- When modifying DB schema, update the corresponding `db-init` scripts and document re-seeding steps.

--

## Security, Testing & Migration Guidance

- Security: Treat all user-facing inputs as untrusted. If modernizing, first add a compatibility layer and tests, then migrate to parameterized queries (PDO or `mysqli`) and replace MD5 with a strong password hash (`password_hash`).
- Testing: There is no existing test harness. Add small, focused integration tests that run against a disposable Docker Compose environment to validate migrations and fixes.
- Migration plan (high level):
  1. Add a DB compatibility shim or helper library providing parameterized query wrappers.
  2. Introduce unit/integration tests to cover login, swiping, and match creation.
  3. Migrate one query or module at a time (e.g., replace `login.php` auth path with PDO and `password_verify`) and validate via tests and the Docker environment.

--

## Where to Look

- Docker: `docker-compose.yml`
- WAP stack: `content/` (notable: `init.php`, `db.php`, `index.php`, `action.php`, `login.php`, `schema.sql`)
- Web98 stack: `content-web98/` (notable: `lib.pl`, `*.cgi`, `index.html`)
- DB init: `db-init/`, `db-init-web98/`
- Utilities: `scripts/` (image generation & seed SQL)

--


Maintainer: please open issues or request PR reviews for any modernization work — changes touching `db.php`, `init.php`, or `docker-compose.yml` should include a migration and smoke-test plan.

### Performance quick-wins implemented (Web98)
- Added DB indexes on posts, friendships, messages to speed common lookups.
- Capped feed/profile lists to modest lengths and kept images very small.
- Added micro-caches (60s) for feed and profile pages; invalidate naturally on write paths.
- Served static assets from a dedicated path for longer cache lifetimes.

### Heavier improvements left as future work
- Swap to DBI/DBD::mysql with persistent handles.
- Move CGI scripts under mod_perl 1.x or FastCGI.
- Introduce a front cache/proxy (e.g., Squid 2.x) for static and cacheable GETs.
- Downgrade infra to strictly 1998 versions (Apache 1.3.1, MySQL 3.22.x) once perf work is stable.
