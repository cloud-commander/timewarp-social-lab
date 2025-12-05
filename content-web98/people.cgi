#!/usr/bin/perl
use strict;
use lib '.';
use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
my $u = require_login($cgi);
my $q = $cgi->param('q') || '';

my $sql = "SELECT id, full_name, school, class_year, dorm, concentration FROM users";
if ($q) {
    my $qs = sql_str($q);
    $sql .= " WHERE full_name LIKE '%$qs%' OR dorm LIKE '%$qs%' OR concentration LIKE '%$qs%'";
}
$sql .= " ORDER BY created_at DESC LIMIT 25";
my $rows = db_query($sql);

layout_header('People', $u);
print '<div class=card><b>Browse people</b><form method="get" action="people.cgi"><input type="hidden" name="sid" value="'.html_escape($u->{sid}).'"/><input name="q" value="'.html_escape($q).'" size="26"> <input type="submit" value="Search" class="btn"></form><div class=meta>Showing latest 25 profiles.</div></div>';

foreach my $r (@$rows) {
    my ($id,$name,$school,$year,$dorm,$conc) = @$r;
    print '<div class=card><a href="profile.cgi?sid='.$u->{sid}.'&id='.$id.'"><b>'.html_escape($name).'</b></a>';
    print ' <span class=meta>'.html_escape($school);
    if ($year) { print " '".html_escape($year % 100); }
    print '</span>';
    print '<div class=meta>';
    print html_escape($dorm) if $dorm;
    print ' &middot; ' if $dorm && $conc;
    print html_escape($conc) if $conc;
    print '</div>';
    print '</div>';
}

layout_footer();
