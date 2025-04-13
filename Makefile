SCRIPT=scripts

.PHONY: clean

PYTHON = python3

plot: $(SCRIPT)/dephasage.py
	$(PYTHON) $^

dim: $(SCRIPT)/dim.py
	$(PYTHON) $^


