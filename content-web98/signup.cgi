#!/usr/bin/perl
use strict;use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
if ($cgi->request_method eq 'POST') {
    my %p = map { $_ => $cgi->param($_) || '' } qw(user full_name email pass bio hometown school class_year dorm concentration gender status looking_for phone birthday);
    foreach my $k (qw(user full_name email pass school)) { unless ($p{$k}) { return show_form('Please fill all required fields.'); } }
    if ($p{email} !~ /@.+\.edu$/i) { return show_form('Use your .edu address to join.'); }
    my $exists = db_query("SELECT id FROM users WHERE username='".sql_str($p{user})."' OR email='".sql_str($p{email})."' LIMIT 1");
    if (@$exists) { return show_form('That username or email is taken.'); }
    my $sql = sprintf "INSERT INTO users (username,full_name,email,password_md5,school,class_year,dorm,concentration,gender,status,looking_for,phone,birthday,bio,hometown,photo_url,created_at) VALUES ('%s','%s','%s',MD5('%s'),'%s',%s,'%s','%s','%s','%s','%s','%s',%s,'%s','%s','img/default.jpg',NOW())",
        sql_str($p{user}), sql_str($p{full_name}), sql_str($p{email}), sql_str($p{pass}), sql_str($p{school}),
        $p{class_year} ? int($p{class_year}) : 'NULL',
        sql_str($p{dorm}), sql_str($p{concentration}), sql_str($p{gender}), sql_str($p{status}),
        sql_str($p{looking_for}), sql_str($p{phone}),
        $p{birthday} ? "'" . sql_str($p{birthday}) . "'" : 'NULL',
        sql_str($p{bio}), sql_str($p{hometown});
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
    print 'School*<br/><input name="school" value="Harvard University" size="30"><br/>';
    print 'Class year<br/><input name="class_year" size="6"><br/>';
    print 'House / Dorm<br/><input name="dorm" size="26"><br/>';
    print 'Concentration<br/><input name="concentration" size="30"><br/>';
    print 'Gender<br/><select name="gender"><option>Male</option><option>Female</option><option>Other</option><option selected>Prefer not to say</option></select><br/>';
    print 'Status<br/><select name="status"><option>Single</option><option>In a relationship</option><option>Engaged</option><option>Married</option><option selected>Rather not say</option></select><br/>';
    print 'Looking for<br/><select name="looking_for"><option>Friendship</option><option>Dating</option><option>Networking</option></select><br/>';
    print 'Phone<br/><input name="phone" size="20"><br/>';
    print 'Birthday (YYYY-MM-DD)<br/><input name="birthday" size="12"><br/>';
    print 'Hometown<br/><input name="hometown" size="30"><br/>';
    print 'Bio<br/><textarea name="bio" rows="3" cols="32"></textarea><br/>';
    print '<input type="submit" value="Join" class="btn">';
    print '</form>';
    print '<div class=meta>'.html_escape($msg).'</div>' if $msg;
    print '</div>';
    layout_footer();
}
