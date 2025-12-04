<?php
header("Content-Type: application/vnd.wap.xhtml+xml; charset=ISO-8859-1");
echo '<?xml version="1.0" encoding="ISO-8859-1"?>';
?>
<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>DB Test</title>
    <link rel="stylesheet" type="text/css" href="style.css"/>
</head>
<body>
    <div class="container">
        <p>PHP Version: <?php echo phpversion(); ?></p>
        <p>MySQL Status:</p>
        <p>
        <?php
        $link = mysql_connect('wap-db', 'root', 'password');
        if (!$link) {
            echo 'Could not connect: ' . mysql_error();
        } else {
            echo 'Connected successfully';
            echo '<br/>Server: ' . mysql_get_server_info();
            mysql_close($link);
        }
        ?>
        </p>
        <p><a href="index.xhtml">Back</a></p>
    </div>
</body>
</html>
