<?php
// logout.php - Logout
session_start();
global $HTTP_SESSION_VARS;
session_unregister('user_id');
unset($HTTP_SESSION_VARS['user_id']);
session_destroy();
header("Location: login.php");
exit;
?>
