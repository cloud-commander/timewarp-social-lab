<?php
// action.php - Handle Swiping Actions
include 'init.php';

global $HTTP_SESSION_VARS, $user_id;
if (!isset($user_id) && !isset($HTTP_SESSION_VARS['user_id'])) {
    header("Location: login.php?" . SID);
    exit;
}



if (isset($user_id)) {
    $my_id = $user_id;
} else {
    $my_id = $HTTP_SESSION_VARS['user_id'];
}
global $HTTP_GET_VARS;
$uid = isset($HTTP_GET_VARS['uid']) ? intval($HTTP_GET_VARS['uid']) : 0;
$do = isset($HTTP_GET_VARS['do']) ? $HTTP_GET_VARS['do'] : '';

if ($uid && ($do == 'pass' || $do == 'date')) {
    // Insert into likes
    $timestamp = time();
    $sql = "INSERT IGNORE INTO likes (from_user_id, to_user_id, action, timestamp) VALUES ($my_id, $uid, '$do', $timestamp)";
    mysql_query($sql);

    // Check for Match
    if ($do == 'date') {
        // Check if they liked me
        $check_sql = "SELECT * FROM likes WHERE from_user_id = $uid AND to_user_id = $my_id AND action = 'date'";
        $check_res = mysql_query($check_sql);
        if (mysql_num_rows($check_res) > 0) {
            // It's a match!
            $match_sql = "INSERT IGNORE INTO matches (user_id_1, user_id_2, timestamp) VALUES (" . min($my_id, $uid) . ", " . max($my_id, $uid) . ", $timestamp)";
            mysql_query($match_sql);
            
            include 'header.php';
            echo "<p>It's a Match!</p>";
            echo "<a href='chat.php?match_id=" . min($my_id, $uid) . "-" . max($my_id, $uid) . (SID ? "&" . SID : "") . "'>Chat Now</a><br/>";
            echo "<a href='index.php" . (SID ? "?" . SID : "") . "'>Keep Swiping</a>";
            include 'footer.php';
            exit;
        }
    }
}

header("Location: index.php" . (SID ? "?" . SID : ""));
exit;
?>
