#!/usr/bin/perl
use strict;use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
if ($cgi->request_method eq 'POST') {
    my $user = $cgi->param('user') || '';
    my $pass = $cgi->param('pass') || '';
    my $rows = db_query("SELECT id, full_name FROM users WHERE username='".sql_str($user)."' AND password_md5=MD5('".sql_str($pass)."') LIMIT 1");
    if (@$rows) {
        my $sid = rand_sid();
        my $uid = $rows->[0]->[0];
        db_do("DELETE FROM sessions WHERE user_id=$uid");
        db_do("INSERT INTO sessions (id,user_id,expires_at) VALUES ('$sid',$uid,DATE_ADD(NOW(),INTERVAL 7 DAY))");
        my $cookie = $cgi->cookie(-name=>'sid',-value=>$sid,-expires=>'+7d');
        print $cgi->redirect(-uri=>'feed.cgi?sid='.$sid,-cookie=>$cookie);
        exit;
    } else {
        show_form('Invalid username or password.');
        exit;
    }
} else {
    show_form('');
}

sub show_form {
    my ($err) = @_;
    layout_header('Login', undef);
    print '<div class=card><b>Sign in</b><br/>';
    print '<form method="post" action="login.cgi">';
    print 'Username:<br/><input type="text" name="user" size="20"><br/>';
    print 'Password:<br/><input type="password" name="pass" size="20"><br/>';
    print '<input type="submit" value="Login" class="btn"> ';
    print '<a class="btn" href="signup.cgi">Sign up</a>';
    print '</form>';
    print '<div class=meta>'.html_escape($err).'</div>' if $err;
    print '</div>';
    layout_footer();
}
