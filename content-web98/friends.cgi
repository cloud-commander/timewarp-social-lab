#!/usr/bin/perl
use strict;use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
my $u = require_login($cgi);
layout_header('Friends', $u);
my $accepted = db_query("SELECT users.id, users.full_name FROM friendships JOIN users ON friendships.addressee_id=users.id WHERE friendships.requester_id=$u->{id} AND friendships.status='accepted' UNION SELECT users.id, users.full_name FROM friendships JOIN users ON friendships.requester_id=users.id WHERE friendships.addressee_id=$u->{id} AND friendships.status='accepted'");
print '<div class=card><b>Friends ('.scalar(@$accepted).')</b><ul class=clean>';
foreach my $f (@$accepted) {
    print '<li><a href="profile.cgi?sid='.$u->{sid}.'&id='.$f->[0].'">'.html_escape($f->[1]).'</a></li>';
}
print '</ul></div>';
my $pending = db_query("SELECT friendships.id, users.full_name FROM friendships JOIN users ON friendships.addressee_id=users.id WHERE friendships.requester_id=$u->{id} AND friendships.status='pending'");
if (@$pending) {
    print '<div class=card><b>Pending requests</b><ul class=clean>';
    foreach my $p (@$pending) { print '<li>'.html_escape($p->[1]).'</li>'; }
    print '</ul></div>';
}
layout_footer();
