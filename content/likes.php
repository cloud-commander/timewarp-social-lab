<?php
// likes.php - Who Liked Me
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

$sql = "SELECT u.username, u.id, u.last_active 
        FROM likes l 
        JOIN users u ON l.from_user_id = u.id 
        WHERE l.to_user_id = $my_id AND l.action = 'date'
        ORDER BY l.timestamp DESC";
$result = mysql_query($sql);
?>

<div align="center"><b>Who Liked Me</b></div>
<table width="100%">
<?php
$i = 1;
while ($row = mysql_fetch_array($result)) {
    $bg = ($i % 2 == 0) ? '#D0D0D0' : '#C0C0C0';
    $online = ($row['last_active'] > (time() - 300)) ? ' (Online)' : '';
    echo "<tr bgcolor='$bg'><td>";
    echo htmlspecialchars($row['username']) . $online;
    echo "</td></tr>";
    $i++;
}

if ($i == 1) {
    echo "<tr><td>No likes yet.</td></tr>";
}
?>
</table>

<?php include 'footer.php'; ?>
