<?php
// login.php - User Login
include 'init.php';

global $HTTP_POST_VARS;
$error = '';

if (isset($HTTP_POST_VARS['submit'])) {
    $username = addslashes($HTTP_POST_VARS['username']);
    $password = md5($HTTP_POST_VARS['password']);

    $sql = "SELECT id FROM users WHERE username = '$username' AND password = '$password'";
    $result = mysql_query($sql) or die(mysql_error());
    
    if ($row = mysql_fetch_array($result)) {
        $user_id = $row['id'];
        session_register('user_id');
        header("Location: index.php?" . SID);
        exit;
    } else {
        $error = "Invalid login.";
    }
}

?>
<?php include 'header.php'; ?>

<div align="center">
    <img src="img/logo.jpg" alt="LoveLink" /><br/>
    <b>Login</b>
</div>
<?php if ($error) echo "<p style='color:red'>$error</p>"; ?>

<form method="post" action="login.php?<?php echo SID; ?>">
    Username: <input type="text" name="username"/><br/>
    Password: <input type="password" name="password"/><br/>
    <input type="submit" name="submit" value="Login"/>
</form>
<br/>
<a href="register.php?<?php echo SID; ?>">Register</a>

<?php include 'footer.php'; ?>
