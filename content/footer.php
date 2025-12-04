<?php
// footer.php - Soft Keys & Footer
// Expects global variables: $softkey_left_label, $softkey_left_url, $softkey_right_label, $softkey_right_url
global $softkey_left_label, $softkey_left_url, $softkey_right_label, $softkey_right_url;

// Defaults
if (!isset($softkey_left_label)) { $softkey_left_label = ''; }
if (!isset($softkey_right_label)) { $softkey_right_label = ''; }
?>

<hr/>
<table width="100%" class="softkeys">
    <tr>
        <td width="50%" align="left">
            <?php if ($softkey_left_label): ?>
                <?php
                    $url = $softkey_left_url;
                    if (SID) {
                        $url .= (strpos($url, '?') !== false ? '&' : '?') . SID;
                    }
                    $url = str_replace('&', '&amp;', $url);
                ?>
                <a href="<?php echo $url; ?>" accesskey="1" class="button"><?php echo $softkey_left_label; ?></a>
            <?php endif; ?>
        </td>
        <td width="50%" align="right">
            <?php if ($softkey_right_label): ?>
                <?php
                    $url = $softkey_right_url;
                    if (SID) {
                        $url .= (strpos($url, '?') !== false ? '&' : '?') . SID;
                    }
                    $url = str_replace('&', '&amp;', $url);
                ?>
                <a href="<?php echo $url; ?>" accesskey="3" class="button"><?php echo $softkey_right_label; ?></a>
            <?php endif; ?>
        </td>
    </tr>
</table>
<div align="center">
    <a href="menu.php<?php echo (SID ? '?' . SID : ''); ?>" accesskey="0">Menu</a>
</div>

</div> <!-- End mobile-wrapper -->
</div> <!-- End device-frame -->
</body>
</html>
