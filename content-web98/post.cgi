#!/usr/bin/perl
use strict;use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
my $u = require_login($cgi);
my $body = $cgi->param('body') || '';
if ($body) {
    my $sql = sprintf "INSERT INTO posts (user_id,body,created_at) VALUES (%d,'%s','%s')", $u->{id}, sql_str($body), now_ts();
    db_do($sql);
}
print $cgi->redirect('feed.cgi?sid='.$u->{sid});
