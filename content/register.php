<?php
// register.php - User Registration
include 'init.php';

global $HTTP_POST_VARS;
$error = '';

if (isset($HTTP_POST_VARS['submit'])) {
    $username = addslashes($HTTP_POST_VARS['username']);
    $password = md5($HTTP_POST_VARS['password']);
    $age = intval($HTTP_POST_VARS['age']);
    $gender = $HTTP_POST_VARS['gender'];
    $bio = addslashes($HTTP_POST_VARS['bio']);
    $now = time();

    if ($username && $password && $age && $gender) {
        $sql = "INSERT INTO users (username, password, age, gender, bio, last_active, created_at) 
                VALUES ('$username', '$password', $age, '$gender', '$bio', $now, $now)";
        if (mysql_query($sql)) {
            echo "<p>Registration Successful!</p>";
            echo "<a href='login.php?" . SID . "'>Login Now</a>";
            include 'footer.php';
            exit;
        } else {
            $error = "Username already taken.";
        }
    } else {
        $error = "All fields required.";
    }
}
?>

<?php include 'header.php'; ?>

<div align="center"><b>Register</b></div>
<?php if ($error) echo "<p style='color:red'>$error</p>"; ?>

<form method="post" action="register.php?<?php echo SID; ?>">
    Username: <input type="text" name="username" maxlength="20"/><br/>
    Password: <input type="password" name="password" maxlength="20"/><br/>
    Age: <input type="text" name="age" format="*N" maxlength="2"/><br/>
    Gender: 
    <select name="gender">
        <option value="M">Male</option>
        <option value="F">Female</option>
    </select><br/>
    Bio:<br/>
    <input type="text" name="bio" maxlength="100"/><br/>
    <input type="submit" name="submit" value="Register"/>
</form>
<br/>
<a href="login.php?<?php echo SID; ?>">Login</a>

<?php include 'footer.php'; ?>
