#!/usr/bin/perl
use strict;use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
my $u = current_user($cgi);
if ($u) { print $cgi->redirect('feed.cgi?sid='.$u->{sid}); } else { print $cgi->redirect('login.cgi'); }
