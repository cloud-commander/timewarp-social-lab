#!/usr/bin/perl
use strict;use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
my $u = require_login($cgi);
my $to = int($cgi->param('to') || 0);
if ($cgi->request_method eq 'POST') {
    my $body = $cgi->param('body') || '';
    if ($to && $body) {
        my $sql = sprintf "INSERT INTO messages (sender_id,recipient_id,body,created_at) VALUES (%d,%d,'%s','%s')", $u->{id}, $to, sql_str($body), now_ts();
        db_do($sql);
    }
    print $cgi->redirect('messages.cgi?sid='.$u->{sid});
    exit;
}
layout_header('Send Message', $u);
print '<div class=card><b>Send to user #'.html_escape($to).'</b><form method="post" action="sendmessage.cgi">';
print '<input type="hidden" name="sid" value="'.html_escape($u->{sid}).'">';
print '<input type="hidden" name="to" value="'.html_escape($to).'">';
print '<textarea name="body" rows="3" cols="40"></textarea><br/>';
print '<input type="submit" value="Send" class="btn">';
print '</form></div>';
layout_footer();
