#!/usr/bin/perl
use strict;
use lib '.';
use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
my $u = require_login($cgi);
my $rows = db_query("SELECT messages.id, users.full_name, messages.body, DATE_FORMAT(messages.created_at,'%b %e %H:%i'), users.id FROM messages, users WHERE messages.sender_id=users.id AND recipient_id=$u->{id} ORDER BY messages.id DESC LIMIT 20");
layout_header('Inbox', $u);
print '<div class=card><b>Inbox</b><ul>';
foreach my $r (@$rows) {
    my ($id,$from,$body,$ts,$sid) = @$r;
    print '<li><a href="sendmessage.cgi?sid='.$u->{sid}.'&to='.$sid.'">'.html_escape($from).'</a>: '.html_escape($body).' <span class=meta>'.$ts.'</span></li>';
}
print '</ul></div>';
layout_footer();
