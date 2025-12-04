<?php
// index.php - The Swiping Deck
include 'init.php';

// Check Login
// Check Login
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

// Get a user to swipe on
// Exclude: Self, Already Liked/Passed, Blocked
$sql = "SELECT u.*, p.filename as photo 
        FROM users u 
        LEFT JOIN user_photos p ON u.id = p.user_id AND p.is_primary = 1
        LEFT JOIN likes l ON l.to_user_id = u.id AND l.from_user_id = $my_id
        LEFT JOIN blocks b ON b.blocked_user_id = u.id AND b.user_id = $my_id
        WHERE u.id != $my_id 
        AND l.from_user_id IS NULL 
        AND b.user_id IS NULL
        LIMIT 1";

$result = mysql_query($sql);
$user = mysql_fetch_array($result);

if ($user) {
    // Set Soft Keys
    $softkey_left_label = '[ PASS ]';
    $softkey_left_url = "action.php?do=pass&uid=" . $user['id'];
    $softkey_right_label = '[ DATE ]';
    $softkey_right_url = "action.php?do=date&uid=" . $user['id'];
} else {
    $softkey_left_label = '';
    $softkey_right_label = '';
}

?>

<table width="100%">
    <tr>
        <td align="center">
            <?php if ($user): ?>
                <?php if ($user['photo']): ?>
                    <img src="img/<?php echo $user['photo']; ?>" alt="Photo" width="96" height="96" /><br/>
                <?php else: ?>
                    <img src="img_gen.php" alt="No Photo" /><br/>
                <?php endif; ?>
                
                <b><?php echo htmlspecialchars($user['username']); ?></b>, <?php echo $user['age']; ?><br/>
                <?php echo htmlspecialchars($user['bio']); ?><br/>
                
                <?php if ($user['last_active'] > (time() - 300)): ?>
                    <small>Online</small>
                <?php endif; ?>
                
            <?php else: ?>
                <p>No more users to swipe on!</p>
                <p>Check back later.</p>
            <?php endif; ?>
        </td>
    </tr>
</table>

<?php include 'footer.php'; ?>
