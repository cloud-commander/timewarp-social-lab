<?php
// edit_profile.php - Edit Profile & Blocking
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
global $HTTP_POST_VARS;

// Handle Update
if (isset($HTTP_POST_VARS['update'])) {
    $age = intval($HTTP_POST_VARS['age']);
    $gender = $HTTP_POST_VARS['gender'];
    $bio = addslashes($HTTP_POST_VARS['bio']);
    
    $sql = "UPDATE users SET age=$age, gender='$gender', bio='$bio' WHERE id=$my_id";
    mysql_query($sql);
    echo "<p>Profile Updated!</p>";
}

// Handle Block
if (isset($HTTP_POST_VARS['block'])) {
    $block_id = intval($HTTP_POST_VARS['block_id']);
    if ($block_id) {
        $now = time();
        $sql = "INSERT INTO blocks (user_id, blocked_user_id, timestamp) VALUES ($my_id, $block_id, $now)";
        mysql_query($sql);
        echo "<p>User Blocked.</p>";
    }
}

// Get Current Data
$sql = "SELECT * FROM users WHERE id = $my_id";
$result = mysql_query($sql);
$user = mysql_fetch_array($result);
?>

<div align="center"><b>Edit Profile</b></div>

<form method="post" action="edit_profile.php<?php echo (SID ? "?" . SID : ""); ?>">
    Age: <input type="text" name="age" value="<?php echo $user['age']; ?>" size="3"/><br/>
    Gender: 
    <select name="gender">
        <option value="M" <?php if ($user['gender'] == 'M') echo 'selected'; ?>>Male</option>
        <option value="F" <?php if ($user['gender'] == 'F') echo 'selected'; ?>>Female</option>
    </select><br/>
    Bio:<br/>
    <input type="text" name="bio" value="<?php echo htmlspecialchars($user['bio']); ?>" maxlength="100"/><br/>
    <input type="submit" name="update" value="Update Profile"/>
</form>

<hr/>
<b>Block User</b><br/>
<form method="post" action="edit_profile.php?<?php echo SID; ?>">
    User ID: <input type="text" name="block_id" size="5"/><br/>
    <input type="submit" name="block" value="Block"/>
</form>

<?php include 'footer.php'; ?>
