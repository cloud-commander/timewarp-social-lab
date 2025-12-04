<?php
// db.php - Database Connection
// PHP 4.0 / MySQL 3.23

define('DB_HOST', 'wap-db');
define('DB_USER', 'root');
define('DB_PASS', 'password');
define('DB_NAME', 'lovelink');

$link = mysql_connect(DB_HOST, DB_USER, DB_PASS);
if (!$link) {
    die('Could not connect: ' . mysql_error());
}
mysql_select_db(DB_NAME, $link) or die('Could not select database');
