#!/usr/bin/env python
# Generate the bug summary page
# All the distro-dependent stuff is imported from buglist.

import string, buglist, time

bugs = buglist.Buglist()

old_accepted = 479	# Represents patches formerly tagged 'y'.
buglist.total += old_accepted

applied = len(bugs.pagelist(include="npr"))
pending = len(bugs.pagelist(include="n*"))
accepted = old_accepted + len(bugs.pagelist(include="yp"))
rejected = len(bugs.pagelist(include="r"))
ok = (buglist.total - buglist.already) - buglist.errors - applied

def percent(x):
    return x * 100.0 / (buglist.total - buglist.already)

print '''<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<link rev="made" href="mailto:esr@snark.thyrsus.com" />
<link rel="stylesheet" href="/~esr/sitestyle.css" type="text/css" />
<meta name="description" content="" />
<meta name="keywords" content="" />
<meta name="MSSmartTagsPreventParsing" content="TRUE" />
<title>Manual page glitches</title>
</head>
<body>

<div id="Header">
<table width="100%%" cellpadding="0" summary="Canned page header">
<tr>
<td>Manual page glitches</td>
<td align="right">%s</td>
</tr>
</table>
</div>

<div id="Menu">
	<hr/>
	<a href="/~esr" title="My home page">Home Page</a><br />
	<a href="/~esr/whatsnew.html" title="New on this site">What is New</a><br />
	<a href="/~esr/sitemap.html" title="Map of the site">Site Map</a><br />
	<a href="/~esr/software.html" title="Software I maintain">Software</a><br />
	<a href="/~esr/projects.html" title="My projects">Projects</a><br />
	<a href="/~esr/faqs/" title="My FAQ documents">HOWTOs</a><br />
	<a href="/~esr/writings/" title="Essays and ruminations">Essays</a><br />
	<a href="/~esr/personal.html" title="Portrait of the author">Personal</a><br />
	<a href="http://www.ibiblio.org/esrblog/">Weblog</a><br/>
        <a href="/~esr/netfreedom/">Freedom!</a><br />
	<a href="/~esr/guns/">Firearms!</a><br />
	<hr/>
    <p>
      <a href="http://validator.w3.org/check/referer"><img
          src="http://www.w3.org/Icons/valid-xhtml10"
          alt="Valid XHTML 1.0!" height="31" width="88" /></a>
    </p>

</div>

<div id="Content">

<p>I maintain a man-page-to-DocBook converter, <a
href="index.html">doclifter</a>. A side effect of this program is that
it serves as a validator for the correctness and portability of the
markup used on Unix manual pages.  I test it by running it against all
the manual pages in a full %s; there are %d of these on my development
machine, of which %d already have DocBook masters.  It converts %d
(%02.2f%%) of the remaining %d into valid XML-DocBook.</p>

<p>Most of the remaining %02.2f%% of errors happen because groff(1)
and its kin have weak-to-nonexistent validity checking.  Often,
doclifter fails because of outright errors in macro usage that groff
does not catch.  Sometime it fails on constructions that are legal but
perverse.  Very occasionally it throws an error because a man page is
correct but has a structure that cannot be translated to DocBook.  I
keep a database of patches for such problems, and periodically
try to push fix patches out to the manual-page maintainers.</p>

<p>Even if you do not care about DocBook, this cleanup work benefits
all third-party manual page viewers, including the GNOME and KDE
documentation browsers; groff constructions that confuse doclifter
are very likely to produce visible problems on these.</p>

<p>The table below is a listing of the %d (%02.2f%%) pages on which
doclifter fails, but the failure can be prevented with a fix patch to
the manual page source.  %d pages (%02.2f%%) remain intractable,
generally due to markup problems more severe than a point patch can
address.  I am working with the individual projects responsible to get
those cleaned up.</p>

<p>It is likely that you are reading this because you have received
email telling you that patches are associated with your name or list
address.  Please consider incorporating them, or equivalents, in your
next release.  Also, please write back and tell me what you plan to do
so I can keep my database up-to-date.</p>

<p>If you are not already considering it, please think about moving
the documentation masters of your project to DocBook (or some format
from which you can generate DocBook). If everybody moved to using
DocBook as a common exchange format, it would become much easier to
support unified browsing of all system documentation with Web-like
hypertext capabilities, automatic indexing, and rich search
facilities.</p>

<p>Tools to generate man pages, HTML, and PostScript from DocBook
files are open-source and generally available.  My program, doclifter,
should make moving your manual-page masters to DocBook a fairly
painless process.</p>

<p>Many major open source projects (including the Linux kernel, the
Linux Documentation Project, X.org, GNOME, KDE, and FreeBSD) have
already moved to DocBook or are in the process of doing so.</p>

<p>(Individual entries for accepted patches are no longer shown.) </p>

<p>Summary: %d patches pending, %d accepted, %d rejected.</p>

<p>Status codes are as follows:</p>

<br />

<table width='100%%' border='1'>
<tr><td>n</td>
<td>No response yet.</td>
</tr>

<tr><td>p</td>
<td>Maintainer has informed me that this is fixed in the masters, but
I have not seen the fix yet.</td>
</tr>

<tr><td>y</td>
<td>Accepted</td>
</tr>

<tr><td>r</td>
<td>Rejected</td>
</tr>

<tr><td>s</td>
<td>Superseded (page lifts correctly without the patch)</td>
</tr>

<tr><td>[0-9]+</td>
<td>number of mailings sent</td>
</tr>

<tr><td>b</td>
<td>Address is blocked</td>
</tr>
</table>

<br />

<p>Problem codes are explained after the table.</p>

<br clear='left'/>

<table width='100%%' border='1'>
<tr><td><b>Patch:</b></td><td><b>Problem code:</b></td><td>Status:</td></tr>
''' % (time.strftime("%d %b %Y", time.gmtime()),
       buglist.distro, buglist.total, buglist.already,
       ok, percent(ok),
       buglist.total - buglist.already,
       100.00 - percent(ok),
       applied, percent(applied),
       buglist.errors, percent(buglist.errors),
       pending, accepted, rejected)

for line in bugs.lines:
    (status, pages, problems, mailto) = map(string.strip, line.split("|"))
    if 'g' in status:
        continue
    mailto = mailto.replace("<", "&lt;").replace(">", "&gt;").replace("@", "&#x40;")
    problems = " ".join(map(lambda x: "<a href='#%s'>%s</a>" % (x,x), problems))
    pages = "<br />\n".join(map(lambda x: "<a href='prepatch/%s.patch'>%s</a>" % (x,x), pages.split(",")))+"<br />\n"
    if 'p' in status or 'y' in status or 's' in status:
        status = "<font color='green'>" + status + "</font>"
    print "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (pages,problems,status)
print "</table>\n\n<h1>Error codes:</h1>\n<dl>\n"

items = bugs.codes.items()
items.sort()
for (key, value) in items:
    print "<dt><a name='%s'>%s</a></dt>" % (key, key)
    print "<dd>%s</dd>" % value

print '''
</dl>

</div>
<hr />
</body>
</html>

<!--
Local Variables:
compile-command: "(cd ~/WWW; upload doclifter/problems.html)"
End:
-->
'''

