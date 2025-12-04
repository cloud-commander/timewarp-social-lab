<?php
// upload.php - Photo Upload
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
global $HTTP_POST_FILES;

if (isset($HTTP_POST_FILES['photo'])) {
    $file = $HTTP_POST_FILES['photo'];
    $filename = $file['name'];
    $tmp_name = $file['tmp_name'];
    $size = $file['size'];
    $type = $file['type'];
    
    // Validate
    if (($type == 'image/jpeg' || $type == 'image/gif' || $type == 'image/pjpeg') && $size < 50000) {
        $ext = (strpos($type, 'gif') !== false) ? '.gif' : '.jpg';
        $new_name = 'user_' . $my_id . '_' . time() . $ext;
        $dest = 'img/' . $new_name;
        
        if (move_uploaded_file($tmp_name, $dest)) {
            // Check if first photo
            $check = mysql_query("SELECT id FROM user_photos WHERE user_id = $my_id");
            $is_primary = (mysql_num_rows($check) == 0) ? 1 : 0;
            
            $sql = "INSERT INTO user_photos (user_id, filename, is_primary) VALUES ($my_id, '$new_name', $is_primary)";
            mysql_query($sql);
            
            echo "<p>Upload Successful!</p>";
            echo "<a href='gallery.php" . (SID ? "?" . SID : "") . "'>Back to Gallery</a>";
        } else {
            echo "<p style='color:red'>Upload failed.</p>";
        }
    } else {
        echo "<p style='color:red'>Invalid file. Must be JPG/GIF and < 50KB.</p>";
    }
}
?>

<div align="center"><b>Upload Photo</b></div>
<form method="post" enctype="multipart/form-data" action="upload.php<?php echo (SID ? "?" . SID : ""); ?>">
    <input type="file" name="photo" /><br/>
    <input type="submit" value="Upload" />
</form>

<?php include 'footer.php'; ?>
