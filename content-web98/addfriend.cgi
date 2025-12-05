#!/usr/bin/perl
use strict;use CGI qw(:standard);
require 'lib.pl';
my $cgi = CGI->new;
my $u = require_login($cgi);
my $target = int($cgi->param('id') || 0);
if ($target && $target != $u->{id}) {
    my $exists = db_query("SELECT status FROM friendships WHERE (requester_id=$u->{id} AND addressee_id=$target) OR (requester_id=$target AND addressee_id=$u->{id}) LIMIT 1");
    if (@$exists) {
        if ($exists->[0]->[0] eq 'pending' && db_query("SELECT 1 FROM friendships WHERE requester_id=$target AND addressee_id=$u->{id} AND status='pending'")->@*) {
            db_do("UPDATE friendships SET status='accepted' WHERE requester_id=$target AND addressee_id=$u->{id}");
            db_do("INSERT INTO friendships (requester_id,addressee_id,status,created_at) VALUES ($u->{id},$target,'accepted',NOW())");
        }
    } else {
        db_do("INSERT INTO friendships (requester_id,addressee_id,status,created_at) VALUES ($u->{id},$target,'pending',NOW())");
    }
}
print $cgi->redirect('profile.cgi?sid='.$u->{sid}.'&id='.$target);
