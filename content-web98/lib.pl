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
    print "<style>
body{font-family:Verdana,Arial,Helvetica,sans-serif;font-size:12px;background:#e7e9f5;color:#111;margin:0;padding:0;}
.wrap{width:760px;margin:0 auto;padding:8px;}
a{color:#1d2d5f;text-decoration:none;}
a:hover{text-decoration:underline;}
.nav{background:#3b5998;color:#fff;padding:6px 8px;margin:0 -8px 12px -8px;}
.nav a{color:#fff;font-weight:bold;margin-right:12px;}
.navtbl td{font-size:12px;}
.card{background:#fff;border:1px solid #b3b7d6;padding:8px;margin-bottom:10px;}
.meta{color:#555;font-size:11px;}
textarea,input{font-family:Verdana,Arial;font-size:12px;}
.btn{background:#d8dfea;border:1px solid #5973a9;padding:3px 7px;text-decoration:none;color:#1d2d5f;font-weight:bold;}
.layout{width:100%;border-collapse:collapse;}
.sidebar{width:180px;vertical-align:top;padding-right:10px;}
.main{vertical-align:top;}
ul.clean{margin:4px 0 0 14px;padding:0;}
ul.clean li{margin-bottom:4px;}
</style>";
    print "</head><body><div class=\"wrap\">";
    if ($u) {
        print "<div class=nav><table class=navtbl width=100% cellspacing=0 cellpadding=0><tr><td><b>$SITE_NAME</b> &nbsp; <a href='feed.cgi?sid=$u->{sid}'>Home</a> <a href='profile.cgi?sid=$u->{sid}&id=$u->{id}'>Profile</a> <a href='friends.cgi?sid=$u->{sid}'>Friends</a> <a href='people.cgi?sid=$u->{sid}'>People</a> <a href='messages.cgi?sid=$u->{sid}'>Inbox</a></td><td align=right class=meta>Signed in as " . html_escape($u->{full_name}) . " | <a href='logout.cgi?sid=$u->{sid}'>Logout</a></td></tr></table></div>";
    } else {
        print "<div class=nav><b>$SITE_NAME</b></div>";
    }
}

sub layout_footer {
    print "<div class=meta>Dial-up friendly build. ~50KB/page.</div></div></body></html>";
}

1;
