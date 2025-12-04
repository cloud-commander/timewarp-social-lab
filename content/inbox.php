<?php
// inbox.php - Matches Inbox
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

$sql = "SELECT m.*, u.username, u.id as other_id 
        FROM matches m 
        JOIN users u ON (m.user_id_1 = u.id OR m.user_id_2 = u.id) 
        WHERE (m.user_id_1 = $my_id OR m.user_id_2 = $my_id) 
        AND u.id != $my_id
        ORDER BY m.timestamp DESC";
$result = mysql_query($sql);
?>

<div align="center"><b>Inbox</b></div>
<table width="100%">
<?php
$i = 1;
while ($row = mysql_fetch_array($result)) {
    $match_id = $row['user_id_1'] . '-' . $row['user_id_2'];
    $bg = ($i % 2 == 0) ? '#D0D0D0' : '#C0C0C0';
    echo "<tr bgcolor='$bg'><td>";
    echo "$i. <a href='chat.php?match_id=$match_id" . (SID ? "&" . SID : "") . "' accesskey='$i'>" . htmlspecialchars($row['username']) . "</a>";
    echo "</td></tr>";
    $i++;
}

if ($i == 1) {
    echo "<tr><td>No matches yet.</td></tr>";
}
?>
</table>

<?php include 'footer.php'; ?>
