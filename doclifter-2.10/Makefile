# Makefile for the doclifter project
VERS=2.10

MANDIR=/usr/share/man/man1
BINDIR=/usr/bin

DOCS    = README COPYING TODO PATCHES \
		doclifter.xml doclifter.1 manlifter.xml manlifter.1
SOURCES = doclifter manlifter Makefile $(DOCS) tests/ doclifter-logo.png

all: doclifter-$(VERS).tar.gz

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

doclifter-$(VERS).tar.gz: $(SOURCES)
	mkdir doclifter-$(VERS)
	cp -r $(SOURCES) doclifter-$(VERS)
	tar -czf doclifter-$(VERS).tar.gz doclifter-$(VERS)
	rm -fr doclifter-$(VERS)
	ls -l doclifter-$(VERS).tar.gz

check:
	@cd tests >/dev/null; make --quiet

PYLINTOPTS = --rcfile=/dev/null --reports=n --include-ids=y --disable="C0103,C0111,C0301,C0302,C0322,C0321,C0324,W0402,W0511,W0141,W0231,W0333,W0631,R0201,R0911,R0912,R0914,R0902,R0903,R0904,R0913,R0914,R0915"
pylint:
	@pylint --output-format=parseable $(PYLINTOPTS) doclifter

pychecker:
	@echo "Expect 4 warnings."
	@ln -f doclifter doclifter.py
	@-pychecker --only --quiet --limit 50 doclifter.py
	@rm -f doclifter.py doclifter.pyc

dist: doclifter-$(VERS).tar.gz

clean:
	rm -f doclifter.html manlifter.html doclifter.1 manlifter.1 *.tar.gz 
	rm -f *.pyc docliftertest.xml foobar* fixed* *~ 
	rm -f SHIPPER.* index.html

release: doclifter-$(VERS).tar.gz doclifter.html manlifter.html
	shipper -u -m -t; make clean

# This is used only for updating the bugs page on my website.
# It won't work for anyone else.
update:
	problemgen.py >bugs.html
	scp -r bugs.html prepatch/ login.ibiblio.org:/public/html/catb/esr/doclifter
