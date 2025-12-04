<?php
// chat.php - Chat Interface
include 'init.php';

global $HTTP_SESSION_VARS, $user_id;
if (!isset($user_id) && !isset($HTTP_SESSION_VARS['user_id'])) {
    header("Location: login.php?" . SID);
    exit;
}

include 'header.php';

if (isset($user_id)) {
    $my_id = $user_id;
} else {
    $my_id = $HTTP_SESSION_VARS['user_id'];
}
global $HTTP_GET_VARS, $HTTP_POST_VARS;

$match_id = isset($HTTP_GET_VARS['match_id']) ? $HTTP_GET_VARS['match_id'] : '';
if (!$match_id) {
    header("Location: inbox.php" . (SID ? "?" . SID : ""));
    exit;
}

// Parse match_id to get other user id
$ids = explode('-', $match_id);
$other_id = ($ids[0] == $my_id) ? $ids[1] : $ids[0];

// Handle Send
if (isset($HTTP_POST_VARS['msg'])) {
    $msg = addslashes(substr($HTTP_POST_VARS['msg'], 0, 160));
    $now = time();
    if ($msg) {
        $sql = "INSERT INTO messages (match_id, sender_id, receiver_id, body, timestamp) 
                VALUES ('$match_id', $my_id, $other_id, '$msg', $now)";
        mysql_query($sql);
    }
}

// Get Messages
$sql = "SELECT * FROM messages WHERE match_id = '$match_id' ORDER BY timestamp ASC LIMIT 10";
$result = mysql_query($sql);
?>

<div align="center"><b>Chat</b></div>
<hr/>

<?php
while ($row = mysql_fetch_array($result)) {
    $sender = ($row['sender_id'] == $my_id) ? 'Me' : 'Them';
    echo "<b>$sender:</b> " . htmlspecialchars($row['body']) . "<br/>";
}
?>

<hr/>
<form method="post" action="chat.php?match_id=<?php echo $match_id . (SID ? '&' . SID : ''); ?>">
    <input type="text" name="msg" maxlength="160" /><br/>
    <input type="submit" value="Send" />
</form>

<?php include 'footer.php'; ?>
