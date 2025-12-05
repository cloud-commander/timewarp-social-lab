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

my $rows = db_query("SELECT id, username, full_name, bio, hometown, photo_url, DATE_FORMAT(created_at,'%b %e, %Y') FROM users WHERE id=".int($view_id)." LIMIT 1");
my $out = '';
open my $buf, '>', \$out;
select $buf;
layout_header('Profile', $u);
if (!@$rows) {
    print '<div class=card>User not found.</div>';
    layout_footer();
    select STDOUT; print $out; exit;
}
my ($id,$uname,$fname,$bio,$home,$photo,$created) = @{$rows->[0]};
my $img = $photo ? "<img src='".html_escape($photo)."' width='120' height='80' align='right' hspace='6' vspace='4' alt=''>" : "";
print '<div class=card>'.$img.'<b>'.html_escape($fname).'</b> ('.html_escape($uname).')<br/>';
print '<div class=meta>Member since '.$created.'</div>';
print '<div>'.html_escape($bio).'</div>' if $bio;
print '<div class=meta>Hometown: '.html_escape($home).'</div>' if $home;
if ($id != $u->{id}) {
    print '<div><a class="btn" href="addfriend.cgi?sid='.$u->{sid}.'&id='.$id.'">Add Friend</a> ';
    print '<a class="btn" href="sendmessage.cgi?sid='.$u->{sid}.'&to='.$id.'">Message</a></div>';
}
print '</div>';

# Recent posts by profile owner (limit 10)
my $posts = db_query("SELECT body, DATE_FORMAT(created_at,'%b %e %H:%i') FROM posts WHERE user_id=$id ORDER BY id DESC LIMIT 10");
foreach my $p (@$posts) {
    print '<div class=card><div class=meta>'.$p->[1].'</div><div>'.html_escape($p->[0]).'</div></div>';
}
layout_footer();
select STDOUT;
print $out;

# write cache
mkdir $cache_dir unless -d $cache_dir;
if (open my $cf, '>', $cache_file) { print $cf $out; close $cf; }
