#!/usr/bin/perl
use strict;use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
my $u = current_user($cgi);
if ($u) { db_do("DELETE FROM sessions WHERE id='".$u->{sid}."'"); }
my $cookie = $cgi->cookie(-name=>'sid',-value=>'',-expires=>'-1d');
print $cgi->redirect(-uri=>'login.cgi', -cookie=>$cookie);
