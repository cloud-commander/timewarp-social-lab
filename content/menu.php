<?php
// menu.php - Main Menu
include 'init.php';

// Check Login
global $HTTP_SESSION_VARS, $user_id;
if (!isset($user_id) && !isset($HTTP_SESSION_VARS['user_id'])) {
    header("Location: login.php?" . SID);
    exit;
}

include 'header.php';
?>

<div align="center">
    <b>Menu</b>
</div>

<ul>
    <li><a href="index.php<?php echo (SID ? "?" . SID : ""); ?>">Start Swiping</a></li>
    <li><a href="inbox.php<?php echo (SID ? "?" . SID : ""); ?>">Messages</a></li>
    <li><a href="likes.php<?php echo (SID ? "?" . SID : ""); ?>">Who Liked Me</a></li>
    <li><a href="gallery.php<?php echo (SID ? "?" . SID : ""); ?>">My Photos</a></li>
    <li><a href="edit_profile.php<?php echo (SID ? "?" . SID : ""); ?>">Edit Profile</a></li>
    <li><a href="logout.php<?php echo (SID ? "?" . SID : ""); ?>">Logout</a></li>
</ul>

<?php include 'footer.php'; ?>
