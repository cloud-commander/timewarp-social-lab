**Act as a Legacy PHP Developer (Year 2001).**

**Objective:**
Write the complete source code for **"LoveLink 2000"**, a dating app for **WAP 2.0** devices, running on **PHP 4.0** and **MySQL 3.23**.

---

## Core Constraints

1.  **Strict XHTML-MP:** The output must be valid XML. Use `htmlspecialchars()` on ALL dynamic data.
2.  **No Modern PHP:** Do not use `PDO` or `mysqli`. Use `mysql_query`. Do not use `try/catch`.
3.  **Session Hardening:** Do not rely on cookies. You must append the session ID constant (`SID`) to every HTML link (e.g., `<a href="action.php?<?php echo SID; ?>">`).
4.  **Variable Scope:** Assume `register_globals` is OFF. Use the legacy arrays `$HTTP_GET_VARS` and `$HTTP_POST_VARS`. **IMPORTANT:** These are NOT superglobals. You must declare `global $HTTP_GET_VARS;` inside functions.
5.  **Headers:** You MUST send the correct WAP header at the top of every PHP file: `header("Content-Type: application/vnd.wap.xhtml+xml; charset=ISO-8859-1");`.
6.  **Input Security:** Use `addslashes()` on ALL user input before sending to MySQL. Do not use `mysql_real_escape_string` (not in PHP 4.0).
7.  **Encoding:** Ensure all output is strictly **ISO-8859-1** (Latin-1). Do not use UTF-8.
8.  **No External Dependencies:** Do not use any external libraries or CDNs. All code must be self-contained.
9.  **Performance Simulation:** To accurately represent the 2001 experience, add a `simulate_latency()` function in `header.php` that sleeps for a random duration (e.g., 200ms - 1000ms) on every request to mimic slow CGI/DB processing.

---

## The Application Structure

### 1. Database (`schema.sql`)

- Tables:
  - `users`: `id`, `username`, `password` (MD5), `age`, `gender`, `bio`, `last_active`, `created_at`.
  - `user_photos`: `id`, `user_id`, `filename`, `is_primary` (0 or 1).
  - `likes`: `from_user_id`, `to_user_id`, `action` ('pass' or 'date'), `timestamp`.
  - `matches`: `user_id_1`, `user_id_2`, `timestamp`.
  - `messages`: `id`, `match_id`, `sender_id`, `body`, `timestamp`.
  - `blocks`: `user_id`, `blocked_user_id`, `timestamp`.
- **Foreign Keys:** Do NOT use foreign keys. MySQL 3.23 MyISAM does not support them.
- **Seeding:** Insert 5 users with initial data.

### 2. Configuration (`db.php`)

- Standard `mysql_connect`.
- Define database credentials as constants.

### 3. Shared Layout (`header.php`, `footer.php`)

- **`header.php`:** Contains the `<?xml ... ?>` declaration, `<!DOCTYPE>`, `<html>`, `<head>` (with CSS link), and opening `<body>`.
- **`footer.php`:** Contains the "Soft Keys" navigation table and closing `</body></html>`.
- **Soft Keys Logic:** The footer must accept arguments (e.g. via global variables `$softkey_left_label`, `$softkey_left_url`, etc.) to change the soft key targets/labels per page.

### 4. The Swiping Deck (`index.php`)

- Include `header.php`.
- **Layout:** Use a `<table>` with `width="100%"` to structure the page.
- **Image:** Display the user's **primary photo** from `user_photos` (max 96x96 pixels). If no photo, show a placeholder.
- **Navigation (Soft Keys):**
  - **Left Cell:** `[ PASS ]` (Red link, `accesskey="1"`, style as beveled button). Links to `action.php?do=pass&uid=X`.
  - **Right Cell:** `[ DATE ]` (Green link, `accesskey="3"`, style as beveled button). Links to `action.php?do=date&uid=X`.
  - **Top Link:** `Menu` (`accesskey="0"`). Links to `menu.php`.
- **Logic:**
  - Exclude users in `blocks` table.
  - Update `last_active` timestamp for current user.

### 5. The Logic (`action.php`)

- Accepts `uid` (user_id) and `do` (action) via `$HTTP_GET_VARS`.
- Updates the `likes` table.
- **Matching Algorithm:** If the action is "date", check if the target user already liked the current user.
  - If yes: Insert into `matches` table.
  - If no: Do nothing (silent pass).
- Redirect back to `index.php` using `header("Location: index.php?" . SID);`.

### 6. The Inbox (`inbox.php`)

- Query the `matches` table for the current user.
- Display a numbered list of links: `1. Chat with [Name]` (`accesskey="1"`).
- **Styling:** Use alternating row colors (e.g., `#C0C0C0` and `#D0D0D0`) for the list.
- No AJAX. User must manually refresh to see new matches.

### 7. The Chat (`chat.php`)

- Accept `match_id` via `$HTTP_GET_VARS`.
- Display the last 10 messages from the DB, oldest first.
- A simple `<form method="post">` with:
  - A text input (`<input type="text" name="msg" maxlength="160">`).
  - A "Send" button.
- On POST, write to DB and reload the page.

### 8. Visuals (`style.css`)

- Background color: `#C0C0C0` (Windows 98 Grey).
- Text: Black, `font-family: monospace; font-size: 10px;`.
- Links: Underlined, `color: #000080;`.
- Soft Key Bar: `background: #000080; color: #FFFFFF;`.
- Max width: `176px` (Nokia 6600 screen).
- **Beveled Buttons:** Use `border-style: outset; border-width: 2px; border-color: #FFFFFF #000000 #000000 #FFFFFF;` for action links.
- **Alternating Rows:** Classes `.row0` and `.row1`.
- **Compact Header:** Minimal height, just logo/title.

### 9. Dummy Image Generator (`img_gen.php`)

- **Strictly No GD:** GD was hard to compile in 2001.
- **Fallback:** Serve a static binary string of a minimal 1x1 JPEG (hardcoded base64 decoded) with the correct `Content-Type: image/jpeg` header.

### 10. Registration (`register.php`)

- Simple form: Username, Password, Age, Gender, Bio.
- **Validation:** Check if username exists. Ensure all fields are filled.
- **Security:** Hash password with `md5()`.
- On success: Redirect to `login.php`.

### 11. Login (`login.php`)

- Form: Username, Password.
- Validate against DB.
- Set Session variables (simulate session if needed or use PHP default sessions with `SID` propagation).

### 12. Menu (`menu.php`)

- Links to:
  - `index.php` (Start Swiping)
  - `inbox.php` (Messages)
  - `likes.php` (Who Liked Me)
  - `gallery.php` (My Photos)
  - `edit_profile.php` (Edit Profile)
  - `logout.php`

### 13. Who Liked Me (`likes.php`)

- List users who have 'dated' (liked) the current user.
- Show "Online" status if `last_active` is within 5 minutes.
- Link to their profile/chat if matched.

### 14. Edit Profile (`edit_profile.php`)

- Form to update: Bio, Age, Gender.
- **Block User:** Option to block a specific user ID (e.g. via a separate form or link on their profile).

### 15. Gallery Administration (`gallery.php`)

- List current user's uploaded photos.
- **Actions per photo:**
  - `[Make Primary]`: Updates `user_photos` to set `is_primary=1` for this photo and 0 for others.
  - `[Delete]`: Deletes record and file.
- **Upload Link:** Link to `upload.php`.

### 16. Photo Upload (`upload.php`)

- Form with `<input type="file" name="photo">`.
- **Handling:**
  - Check `$HTTP_POST_FILES` (legacy array).
  - Validate MIME type (must be `image/jpeg` or `image/gif`).
  - Max size: 50KB.
  - Move uploaded file to `img/` directory with a unique name (e.g., `user_{id}_{timestamp}.jpg`).
  - Insert record into `user_photos`.
  - If it's the first photo, set `is_primary=1`.

---

## Integration Notes

> [!IMPORTANT]
> This application is designed to run inside the **WAP 2.0 Simulation Environment** defined in `wap2-env.md`. Ensure the `schema.sql` generated here is compatible with the `init-db.sh` script in that environment.

---
