#!/usr/bin/perl
use strict;use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
if ($cgi->request_method eq 'POST') {
    my %p = map { $_ => $cgi->param($_) || '' } qw(user full_name email pass bio hometown);
    foreach my $k (qw(user full_name email pass)) { unless ($p{$k}) { return show_form('Please fill all required fields.'); } }
    my $exists = db_query("SELECT id FROM users WHERE username='".sql_str($p{user})."' OR email='".sql_str($p{email})."' LIMIT 1");
    if (@$exists) { return show_form('That username or email is taken.'); }
    my $sql = sprintf "INSERT INTO users (username,full_name,email,password_md5,bio,hometown,photo_url,created_at) VALUES ('%s','%s','%s',MD5('%s'),'%s','%s','img/default.jpg',NOW())",
        sql_str($p{user}), sql_str($p{full_name}), sql_str($p{email}), sql_str($p{pass}), sql_str($p{bio}), sql_str($p{hometown});
    db_do($sql);
    print $cgi->redirect('login.cgi');
    exit;
} else { show_form(''); }

sub show_form {
    my ($msg) = @_;
    layout_header('Sign up', undef);
    print '<div class=card><b>Create account</b><br/>';
    print '<form method="post" action="signup.cgi">';
    print 'Username*<br/><input name="user" size="22"><br/>';
    print 'Full name*<br/><input name="full_name" size="30"><br/>';
    print 'Email*<br/><input name="email" size="30"><br/>';
    print 'Password*<br/><input type="password" name="pass" size="22"><br/>';
    print 'Hometown<br/><input name="hometown" size="30"><br/>';
    print 'Bio<br/><textarea name="bio" rows="3" cols="32"></textarea><br/>';
    print '<input type="submit" value="Join" class="btn">';
    print '</form>';
    print '<div class=meta>'.html_escape($msg).'</div>' if $msg;
    print '</div>';
    layout_footer();
}
