#!/usr/bin/env python
import string, os, sys, os.path

subdir = "prepatch"

distro = "Xubuntu 14.10 with some extras"
future = "next Ubuntu release"
total = 10915	# Total in -S report
already = 962	# Non-troff masters (NOP in 0S report)
errors = 12	# Status codes 1-6

class Buglist:
    def __init__(self, filename="PATCHES"):
        file = open(filename)

        self.codes = {}
        while True:
            line = file.readline()
            if line == "%%\n":
                break
            if line[0] == "#":
                continue
            if not line[0].isspace():
                key = line[0]
                self.codes[key] = ""
                line = line[1:]
            self.codes[key] += line.strip() + "\n"

        self.maildict = {}
        self.lines = []
        self.fields = []
        self.typeseen = {}
        self.promised = 0
        while True:
            line = file.readline()
            if not line:
                break
            self.lines.append(line)
            fields = line.split("|")
            try:
                (status, pages, problems, mailto) = map(string.strip, fields)
                if 'p' in status:
                    self.promised += len(pages.split(","))
            except:
                print line
                sys.exit(1)
            for c in problems:
                self.typeseen[c] = True
            self.fields.append(map(string.strip, fields))
            if mailto not in self.maildict:
                self.maildict[mailto] = []
            self.maildict[mailto].append((status, pages, problems))
        file.close()

    def pagelist(self, include="", exclude=""):
        lst = []
        for (status, pages, problems, mailto) in self.fields:
            addit = not include
            for c in include:
                if c in status:
                    addit = True
                    break
            for c in exclude:
                if c in status:
                    addit = False
                    break
            if addit:
                lst += map(string.strip, pages.split(","))
        lst.sort()
        return lst

def filestem(x):
    if x.endswith(".patch"):
        return x[:-6]
    elif x.endswith(".correction"):
        return x[:-11]
    else:
        return x

def pagetofile(page):
    page = os.path.join(subdir, page)
    if os.path.exists(page + ".patch"):
        fp = open(page + ".patch")
        txt = fp.read()
        fp.close()
    # manlifter doesn't pick up corrections
    elif os.path.exists(page + ".correction"):
        fp = open(page + ".correction")
        txt = fp.read()
        fp.close()
    else:
        txt = None
    return txt

if __name__ == '__main__':
    import sets, getopt
    (options, arguments) = getopt.getopt(sys.argv[1:], "e:")
    error_type_filter = None
    for (opt, val) in options:
        if opt == '-e':
            error_type_filter = val

    bugs = Buglist()
    if error_type_filter:	# report on what entries contain specified code
        for (status, pages, problems, mailto) in bugs.fields:
            if error_type_filter in problems:
                print "|".join((status, pages, problems, mailto))
    else:
        # Default action is to sanity-check the database
        files = sets.Set(map(lambda x: filestem(x), os.listdir(subdir)))
        pages = sets.Set(bugs.pagelist())
        unresolved = sets.Set(bugs.pagelist(exclude='y*'))
        counts = {}
        for page in pages:
            counts[page] = counts.get(page, 0) + 1
        duplicates = filter(lambda x: counts[x] > 1, pages)
        if duplicates:
            print "Duplicates:", duplicates
        print "%d unresolved patches, %d promised, %d total, %d files." %(len(unresolved), bugs.promised, len(pages), len(files))
        if files - pages:
            print "These files have no buglist entry:", files - pages
        if unresolved - files:
            print "These bugs have no filelist entry:", unresolved - files
        if files != unresolved:
            print "Leftovers:", " ".join(files - unresolved)
        nonbugs = []
        for c in bugs.codes.keys():
            if not c in bugs.typeseen:
                nonbugs.append(c)
        if nonbugs:
            print "These bug types no longer occur: ", ", ".join(nonbugs)
        available = map(lambda x: x, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        for c in bugs.codes.keys():
            available.remove(c)
        if available:
            print "These bug keys are available: ", ", ".join(available)

