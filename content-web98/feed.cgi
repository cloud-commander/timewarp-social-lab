#!/usr/bin/perl
use strict;
use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
my $u = require_login($cgi);
my $sid = $u->{sid};

# basic profile + counts for sidebar
my $me_rows = db_query("SELECT full_name, photo_url, bio, hometown FROM users WHERE id=$u->{id} LIMIT 1");
my ($me_name,$me_photo,$me_bio,$me_home) = @$me_rows ? @{$me_rows->[0]} : ($u->{full_name}, undef, '', '');
$me_photo = $me_photo || 'img/default.jpg';
my $friend_rows = db_query("SELECT COUNT(*) FROM friendships WHERE (requester_id=$u->{id} OR addressee_id=$u->{id}) AND status='accepted'");
my $friend_count = @$friend_rows ? $friend_rows->[0]->[0] : 0;

# simple micro-cache (60s) per user feed
my $cache_dir = 'cache';
my $cache_file = "$cache_dir/feed_$u->{id}.html";
if (-f $cache_file && (time - (stat($cache_file))[9]) < 60) {
    open my $cf, '<', $cache_file and do { local $/; print <$cf>; close $cf; exit; };
}

my $friends_sql = "SELECT addressee_id FROM friendships WHERE requester_id=$u->{id} AND status='accepted' UNION SELECT requester_id FROM friendships WHERE addressee_id=$u->{id} AND status='accepted'";
my $post_sql = "SELECT posts.id, users.full_name, users.photo_url, posts.body, DATE_FORMAT(posts.created_at,'%b %e %H:%i') FROM posts JOIN users ON posts.user_id=users.id WHERE posts.user_id=$u->{id} OR posts.user_id IN ($friends_sql) ORDER BY posts.id DESC LIMIT 20";
my $rows = db_query($post_sql);

my $out = '';
open my $buf, '>', \$out;
select $buf;
layout_header('News Feed', $u);
print '<table class=layout><tr><td class=sidebar>';
print '<div class=card><b>'.html_escape($me_name).'</b><br/>';
print "<img src='".html_escape($me_photo)."' width='120' height='80' alt='' style='border:1px solid #ccc;margin-top:4px;'><br/>";
print '<div class=meta>Friends: '.$friend_count.'</div>';
print '<div class=meta>'.html_escape($me_home).'</div>' if $me_home;
print '<div class=meta>'.html_escape($me_bio).'</div>' if $me_bio;
print '</div>';
print '<div class=card><b>Shortcuts</b><ul class=clean>';
print '<li><a href="profile.cgi?sid='.$sid.'&id='.$u->{id}.'">View your profile</a></li>';
print '<li><a href="friends.cgi?sid='.$sid.'">Friend list</a></li>';
print '<li><a href="messages.cgi?sid='.$sid.'">Inbox</a></li>';
print '</ul></div>';
print '</td><td class=main>';

print '<div class=card><b>Share an update</b><form method="post" action="post.cgi"><textarea name="body" rows="3" cols="48"></textarea><br/><input type="hidden" name="sid" value="'.html_escape($sid).'"/><input type="submit" value="Post" class="btn"></form></div>';

foreach my $r (@$rows) {
    my ($id,$author,$photo,$body,$ts) = @$r;
    my $img = $photo ? "<img src='".html_escape($photo)."' width='70' height='50' align='left' hspace='6' vspace='4' alt=''>" : "";
    print '<div class=card>'.$img.'<b>'.html_escape($author).'</b><div class=meta>'.$ts.'</div><div>'.html_escape($body).'</div><div style="clear:both"></div></div>';
}
print '</td></tr></table>';
layout_footer();
select STDOUT;
print $out;

# write cache safely
mkdir $cache_dir unless -d $cache_dir;
if (open my $cf, '>', $cache_file) { print $cf $out; close $cf; }
