#!/usr/bin/perl
use strict;
use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
my $u = require_login($cgi);
my $view_id = $cgi->param('id') || $u->{id};

# micro-cache profile view (60s)
my $cache_dir = 'cache';
my $cache_file = "$cache_dir/profile_$view_id.html";
if (-f $cache_file && (time - (stat($cache_file))[9]) < 60) {
    open my $cf, '<', $cache_file and do { local $/; print <$cf>; close $cf; exit; };
}

my $rows = db_query("SELECT id, username, full_name, school, class_year, dorm, concentration, gender, status, looking_for, phone, DATE_FORMAT(birthday,'%M %e, %Y'), bio, hometown, photo_url, DATE_FORMAT(created_at,'%b %e, %Y') FROM users WHERE id=".int($view_id)." LIMIT 1");
my $out = '';
open my $buf, '>', \$out;
select $buf;
layout_header('Profile', $u);
if (!@$rows) {
    print '<div class=card>User not found.</div>';
    layout_footer();
    select STDOUT; print $out; exit;
}
my ($id,$uname,$fname,$school,$class_year,$dorm,$conc,$gender,$status,$looking,$phone,$bday,$bio,$home,$photo,$created) = @{$rows->[0]};
my $img = $photo ? "<img src='".html_escape($photo)."' width='140' height='100' alt='' style='border:1px solid #ccc;'>" : "<img src='img/default.jpg' width='140' height='100' alt='' style='border:1px solid #ccc;'>";
print '<table class=layout><tr><td class=sidebar>';
print '<div class=card>'.$img.'<br/><b>'.html_escape($fname).'</b><br/><span class=meta>Member since '.$created.'</span>';
print '<div class=meta>Handle: '.html_escape($uname).'</div>';
print '<div class=meta>'.html_escape($school);
if ($class_year) { print " '".html_escape($class_year % 100); }
print '</div>';
print '<div class=meta>House: '.html_escape($dorm).'</div>' if $dorm;
print '<div class=meta>Concentration: '.html_escape($conc).'</div>' if $conc;
print '<div class=meta>Status: '.html_escape($status).'</div>' if $status;
print '<div class=meta>Looking for: '.html_escape($looking).'</div>' if $looking;
print '<div class=meta>Gender: '.html_escape($gender).'</div>' if $gender;
print '<div class=meta>Birthday: '.html_escape($bday).'</div>' if $bday;
print '<div class=meta>Phone: '.html_escape($phone).'</div>' if $phone;
print '<div class=meta>Hometown: '.html_escape($home).'</div>' if $home;
print '<div>'.html_escape($bio).'</div>' if $bio;
if ($id != $u->{id}) {
    print '<div style="margin-top:6px;"><a class="btn" href="addfriend.cgi?sid='.$u->{sid}.'&id='.$id.'">Add Friend</a> ';
    print '<a class="btn" href="sendmessage.cgi?sid='.$u->{sid}.'&to='.$id.'">Message</a></div>';
}
print '</div>';
print '</td><td class=main>';

# Recent posts by profile owner (limit 10)
my $posts = db_query("SELECT body, DATE_FORMAT(created_at,'%b %e %H:%i') FROM posts WHERE user_id=$id ORDER BY id DESC LIMIT 10");
print '<div class=card><b>Wall</b></div>';
foreach my $p (@$posts) {
    print '<div class=card><div class=meta>'.$p->[1].'</div><div>'.html_escape($p->[0]).'</div></div>';
}
print '</td></tr></table>';
layout_footer();
select STDOUT;
print $out;

# write cache
mkdir $cache_dir unless -d $cache_dir;
if (open my $cf, '>', $cache_file) { print $cf $out; close $cf; }
