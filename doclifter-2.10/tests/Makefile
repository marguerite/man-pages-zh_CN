# Regression tests for doclifter

TESTLOADS := $(shell ls *.man | sed '/.man/s///')

test: regress
	@echo "No output (other than a testfile stem name) is good news."

rebuild:
	@for file in $(TESTLOADS); do \
	    echo "Remaking $${file}.chk"; \
	    ../doclifter <$${file}.man >$${file}.chk 2>&1; \
	done
regress:
	@for file in $(TESTLOADS); do \
	    echo $${file}; \
	    if ../doclifter <$${file}.man >/tmp/regress$$; \
	    then diff -u /tmp/regress$$ $${file}.chk; \
	    else echo "*** Nonzero return status on $${file}!"; exit 1; fi \
	done
	@rm -f /tmp/regress
