# Regression tests for doclifter
TESTDIRPARENT=/tmp
UTILBINDIR=..

TESTLOADS := $(shell ls *.man | sed '/.man/s///')

test: regress
	@echo "No output (other than a testfile stem name) is good news."

rebuild:
	@for file in $(TESTLOADS); do \
	    echo "Remaking $${file}.chk"; \
	    $(UTILBINDIR)/doclifter <$${file}.man >$${file}.chk 2>&1; \
	done
regress:
	@for file in $(TESTLOADS); do \
	    echo $${file}; \
	    if $(UTILBINDIR)/doclifter <$${file}.man >$(TESTDIRPARENT)/regress$$; \
	    then diff -u $${file}.chk $(TESTDIRPARENT)/regress$$; \
	    else echo "*** Nonzero return status on $${file}!"; exit 1; fi \
	done
	@rm -f $(TESTDIRPARENT)/regress
