<?php
// gallery.php - Gallery Administration
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
global $HTTP_GET_VARS;

// Handle Actions
$action = isset($HTTP_GET_VARS['action']) ? $HTTP_GET_VARS['action'] : '';
$pid = isset($HTTP_GET_VARS['pid']) ? intval($HTTP_GET_VARS['pid']) : 0;

if ($pid && $action) {
    if ($action == 'primary') {
        // Reset all to 0
        mysql_query("UPDATE user_photos SET is_primary = 0 WHERE user_id = $my_id");
        // Set this to 1
        mysql_query("UPDATE user_photos SET is_primary = 1 WHERE id = $pid AND user_id = $my_id");
        echo "<p>Primary photo updated.</p>";
    } elseif ($action == 'delete') {
        // Get filename to delete file
        $res = mysql_query("SELECT filename FROM user_photos WHERE id = $pid AND user_id = $my_id");
        if ($row = mysql_fetch_array($res)) {
            @unlink('img/' . $row['filename']);
            mysql_query("DELETE FROM user_photos WHERE id = $pid AND user_id = $my_id");
            echo "<p>Photo deleted.</p>";
        }
    }
}

// List Photos
$sql = "SELECT * FROM user_photos WHERE user_id = $my_id";
$result = mysql_query($sql);
?>

<div align="center"><b>My Photos</b></div>
<a href="upload.php<?php echo (SID ? "?" . SID : ""); ?>">Upload New Photo</a><br/>
<hr/>

<table width="100%">
<?php
$i = 0;
while ($row = mysql_fetch_array($result)) {
    $bg = ($i % 2 == 0) ? '#D0D0D0' : '#C0C0C0';
    echo "<tr bgcolor='$bg'><td>";
    echo "<img src='img/" . $row['filename'] . "' width='48' height='48' /><br/>";
    if ($row['is_primary']) {
        echo "<b>[Primary]</b><br/>";
    } else {
        echo "<a href='gallery.php?action=primary&pid=" . $row['id'] . (SID ? "&" . SID : "") . "'>[Make Primary]</a><br/>";
    }
    echo "<a href='gallery.php?action=delete&pid=" . $row['id'] . (SID ? "&" . SID : "") . "'>[Delete]</a>";
    echo "</td></tr>";
    $i++;
}

if ($i == 0) {
    echo "<tr><td>No photos uploaded.</td></tr>";
}
?>
</table>

<?php include 'footer.php'; ?>
