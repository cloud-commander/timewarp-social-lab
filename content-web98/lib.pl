#!/usr/bin/perl
use strict;
use CGI qw(:standard);
use POSIX qw(strftime);
require 'config.pl';

sub db_query {
    my ($sql) = @_;
    my @rows;
    my $cmd = "mysql -h $DB_HOST -u $DB_USER -p$DB_PASS --batch --skip-column-names $DB_NAME -e \"$sql\"";
    open(my $fh, "$cmd |") or return [];
    while (my $line = <$fh>) {
        chomp $line;
        push @rows, [ split(/\t/, $line, -1) ];
    }
    close $fh;
    return \@rows;
}

sub db_do {
    my ($sql) = @_;
    system("mysql", "-h", $DB_HOST, "-u", $DB_USER, "-p$DB_PASS", $DB_NAME, "-e", $sql);
}

sub sql_str {
    my ($s) = @_;
    $s = '' unless defined $s;
    $s =~ s/\\/\\\\/g;
    $s =~ s/'/\\'/g;
    return $s;
}

sub html_escape {
    my $s = shift;
    $s = '' unless defined $s;
    return CGI::escapeHTML($s);
}

sub rand_sid {
    my $raw = '';
    for (1..4) { $raw .= pack('N', int(rand(0xffffffff))); }
    return unpack('H*', $raw);
}

sub now_ts { strftime('%Y-%m-%d %H:%M:%S', localtime); }

sub current_user {
    my $cgi = shift;
    my $sid = $cgi->cookie('sid') || $cgi->param('sid') || '';
    return undef unless $sid;
    my $rows = db_query("SELECT users.id, users.username, users.full_name FROM sessions JOIN users ON sessions.user_id=users.id WHERE sessions.id='" . $sid . "' AND sessions.expires_at > NOW() LIMIT 1");
    return undef unless @$rows;
    return { sid => $sid, id => $rows->[0]->[0], username => $rows->[0]->[1], full_name => $rows->[0]->[2] };
}

sub require_login {
    my $cgi = shift;
    my $u = current_user($cgi);
    unless ($u) {
        print $cgi->redirect('login.cgi');
        exit;
    }
    return $u;
}

sub layout_header {
    my ($title, $u) = @_;
    print "Content-Type: text/html\n\n";
    print "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n";
    print "<html><head><title>" . html_escape($title) . "</title>";
    print "<style>body{font-family:Arial,Helvetica,sans-serif;font-size:12px;background:#f0f0f0;color:#000;margin:8px;}a{color:#003399;} .nav{background:#003399;color:#fff;padding:4px;} .card{background:#fff;border:1px solid #999;padding:6px;margin-bottom:8px;} .meta{color:#555;font-size:11px;} textarea,input{font-family:Arial;font-size:12px;} .btn{background:#c0c0c0;border:2px outset #fff;padding:2px 6px;text-decoration:none;color:#000;} </style>";
    print "</head><body>";
    if ($u) {
        print "<div class=nav><b>$SITE_NAME</b> &middot; Logged in as " . html_escape($u->{full_name}) . " | <a href='feed.cgi?sid=$u->{sid}'>Feed</a> | <a href='profile.cgi?sid=$u->{sid}&id=$u->{id}'>Profile</a> | <a href='friends.cgi?sid=$u->{sid}'>Friends</a> | <a href='messages.cgi?sid=$u->{sid}'>Inbox</a> | <a href='logout.cgi?sid=$u->{sid}'>Logout</a></div>";
    } else {
        print "<div class=nav><b>$SITE_NAME</b></div>";
    }
}

sub layout_footer {
    print "<div class=meta>Dial-up friendly build. ~50KB/page.</div></body></html>";
}

1;
