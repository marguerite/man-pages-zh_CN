#!/usr/bin/env python
import string, buglist, smtplib, time, hashlib
import email.mime.multipart, email.mime.text

def send(contact, msg):
    "Send a message."
    try:
        server = smtplib.SMTP('localhost')
        #server.set_debuglevel(1)
        server.sendmail("esr@thyrsus.com", [contact], msg)
        server.quit()
        print contact, "OK"
    except smtplib.SMTPServerDisconnected:
        print "*** Disconnected while mailing", contacr
    except smtplib.SMTPSenderRefused:
        print "*** Host refused sender for", contact
    except smtplib.SMTPRecipientsRefused:
        print "*** Recipient address refused for", contact
    except smtplib.SMTPDataError:
        print "*** Message data refused for", contact
    except smtplib.SMTPConnectError:
        print "*** Connection refused for", contact
    except smtplib.SMTPHeloError:
        print "*** HELO refused for", contact

def hashkey(patch):
    body = "\n".join(patch.split('\n')[2:])	# Trim off the header lines
    m = hashlib.md5()
    m.update(body)
    return m.digest()

def mailall(filter, hook):
    duplicates = {}
    for contact in bugs.maildict:
        if not contact or contact.startswith("http"):
            continue
        template = '''\
This is automatically generated email about markup problems in a man
page for which you appear to be responsible.  If you are not the right
person or list, please tell me so I can correct my database.

See http://catb.org/~esr/doclifter/bugs.html for details on how and
why these patches were generated.  Feel free to email me with any
questions.  Note: These patches do not change the modification date of
any manual page.  You may wish to do that by hand.

I apologize if this message seems spammy or impersonal. The volume of
markup bugs I am tracking is over five hundred - there is no real
alternative to generating bugmail from a database and template.
'''
        reminder = '''
My records indicate that you have accepted this patch, so this is just
a reminder.
'''
        unique = {}
        pagelist = []
        page_to_problems = {}
        for (status, pages, problems) in bugs.maildict[contact]:
            if 'y' in status or 'r' in status or 'g' in status:
                continue
            if filter(status, pages, problems, contact):
                # Setup
                for page in pages.split(","):
                    pagelist.append(page)
                    duplicates[page] = []
                    page_to_problems[page] = problems
        # Enable duplicate detection
        for page in pagelist:
            patch = buglist.pagetofile(page.strip())
            if patch is None:
                # Meant to generate a unique cookie
                body = str(time.time())
            else:
                d = hashkey(patch)
                if d in unique:
                    if not d in duplicates:
                        duplicates[d] = []
                    duplicates[d].append(page)
                else:
                    unique[d] = page
        # Now generate explanations
        explanations = []
        for page in unique.values():
            patch = buglist.pagetofile(page.strip())
            d = hashkey(patch)
            explanation =  "Problems with " + page + ":\n"
            if d in duplicates:
                explanation += "\n(Identical patches should apply to: %s)\n" \
                               % (" ".join(duplicates[d],))
            if 'p' in status:
                explanation += reminder
            if page.endswith("pm"):
                explanation += "\n(May reflect bugs in POD).\n"
            explanation += "\n"
            patch = buglist.pagetofile(page.strip())
            # Patch might have its own header comment.
            if patch.startswith("---"):
                for letter in page_to_problems[page]:
                    if not letter.isalnum():
                        sys.stderr.write("Problem with %s\n" % page)
                    else:
                        explanation += "%s\n" % (bugs.codes[letter])
            d = hashkey(patch)
            if patch:
                this =  explanation + patch
            else:
                this += explanation + "(No patch.)\n"
            explanations.append(this)
        if explanations:
            pagelist = ", ".join(pagelist)
            if len(pagelist) > 100:
                pagelist = "several man pages you maintain"
            body = template \
                  + "\n--\n                             Eric S. Raymond\n"
            msg = email.mime.multipart.MIMEMultipart()
            msg["To"] = contact
            msg["Subject"] = "Problems in " + pagelist
            msg.attach(email.mime.text.MIMEText(body))
            for x in explanations:
                msg.attach(email.mime.text.MIMEText(x))
            apply(hook, (contact, str(msg) + "\n"))

if __name__ == '__main__':
    import getopt, re, sys

    bugs = buglist.Buglist()
    selector = None
    pagefilter = None
    codefilter = None
    addressfilter = None
    hook = lambda contact, msg: sys.stdout.write(msg)
    (options, arguments) = getopt.getopt(sys.argv[1:], "a:c:mp:s:")
    for (switch, val) in options:
        if switch == '-s':	# Select on given status code
            selector = val
        elif switch == '-p':	# Filter on given regexp matching pages
            pagefilter = val
        elif switch == '-a':	# Filter on given regexp matching addressees
            addressfilter = val
        elif switch == '-c':	# Filter on given regexp matching problems
            codefilter = val
        elif switch == '-m':	# Actually send mail
            hook = send
    if selector:
        selector = re.compile(selector)
    if pagefilter:
        pagefilter = re.compile(pagefilter)
    if addressfilter:
        addressfilter = re.compile(addressfilter)
    if codefilter:
        codefilter = re.compile(codefilter)

    def filter(status, pages, problems, contact):
        if selector and not selector.search(status):
            return False
        if pagefilter and not pagefilter.search(pages):
            return False
        if addressfilter and not addressfilter.search(contact):
            return False
        if codefilter and not codefilter.search(contact):
            return False
        return True

    mailall(filter, hook)
