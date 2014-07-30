# Makefile for the doclifter project
VERSION=$(shell sed <doclifter -n -e '/^version *= *\(.*\)/s//\1/p')

PREFIX=/usr
MANDIR=$(PREFIX)/share/man/man1
BINDIR=$(PREFIX)/bin

DOCS    = README COPYING TODO PATCHES \
		doclifter.xml doclifter.1 manlifter.xml manlifter.1
SOURCES = doclifter manlifter Makefile $(DOCS) tests/ doclifter-logo.png

all: doclifter-$(VERSION).tar.gz

install: doclifter.1
	cp doclifter $(BINDIR)
	gzip <doclifter.1 >$(MANDIR)/doclifter.1.gz
	rm doclifter.1

doclifter.1: doclifter.xml
	xmlto man doclifter.xml

manlifter.1: manlifter.xml
	xmlto man manlifter.xml

doclifter.html: doclifter.xml
	xmlto xhtml-nochunks doclifter.xml

manlifter.html: manlifter.xml
	xmlto xhtml-nochunks manlifter.xml

doclifter-$(VERSION).tar.gz: $(SOURCES)
	mkdir doclifter-$(VERSION)
	cp -r $(SOURCES) doclifter-$(VERSION)
	tar -czf doclifter-$(VERSION).tar.gz doclifter-$(VERSION)
	rm -fr doclifter-$(VERSION)
	ls -l doclifter-$(VERSION).tar.gz

doclifter-$(VERSION).md5: doclifter-$(VERSION).tar.gz
	@md5sum doclifter-$(VERSION).tar.gz >doclifter-$(VERSION).md5

check:
	@cd tests >/dev/null; make --quiet

PYLINTOPTS = --rcfile=/dev/null --reports=n \
	--msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
	--dummy-variables-rgx='^_|^dummy'
SUPPRESSIONS = "C0103,C0111,C0301,C0302,C0322,C0321,C0324,C1001,W0110,W0120,W0201,W0402,W0511,W0141,W1401,W0231,W0333,W0631,R0201,R0911,R0912,R0914,R0902,R0903,R0904,R0913,R0914,R0915"
pylint:
	@pylint $(PYLINTOPTS) --disable=$(SUPPRESSIONS) doclifter

pychecker:
	@echo "Expect 4 warnings."
	@ln -f doclifter doclifter.py
	@-pychecker --only --quiet --limit 50 doclifter.py
	@rm -f doclifter.py doclifter.pyc

dist: doclifter-$(VERSION).tar.gz

clean:
	rm -f doclifter.html manlifter.html doclifter.1 manlifter.1
	rm -f *.pyc docliftertest.xml foobar* fixed* *~ bugs.html
	rm -f index.html *.tar.gz *.md5

release: doclifter-$(VERSION).tar.gz doclifter-$(VERSION).md5 doclifter.html manlifter.html
	shipper version=$(VERSION) | sh -e -x

# This is used only for updating the bugs page on my website.
# It won't work for anyone else.
update:
	problemgen.py >bugs.html
	scp -r bugs.html prepatch/ login.ibiblio.org:/public/html/catb/esr/doclifter
