<?php
// init.php - Initialization & Logic
// Simulate GPRS Latency
function simulate_latency() {
    $min_latency = 200000; // 200ms
    $max_latency = 1000000; // 1s
    usleep(rand($min_latency, $max_latency));
}
simulate_latency();

include_once 'db.php';

// Start Session
session_start();
// DEBUG
// error_log("Session ID: " . session_id());
// error_log("Session User ID: " . (isset($_SESSION['user_id']) ? $_SESSION['user_id'] : 'Not Set'));

// Update Last Active
// Update Last Active
global $HTTP_SESSION_VARS, $user_id;
$uid = 0;
if (isset($user_id)) {
    $uid = $user_id;
} elseif (isset($HTTP_SESSION_VARS['user_id'])) {
    $uid = $HTTP_SESSION_VARS['user_id'];
}

if ($uid > 0) {
    $now = time();
    mysql_query("UPDATE users SET last_active = $now WHERE id = $uid");
}
