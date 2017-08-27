# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = HinetPy
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

translation: gettext
	sphinx-intl update -p _build/gettext -l zh_CN

docs:
	@echo
	@echo "Building Chinese version HTML files."
	sphinx-intl build
	make -e SPHINXOPTS="-D language='zh_CN'" html

	@echo
	@echo "Backup Chinese version HTML files."
	mv _build/html _build/html_zh_CN

	@echo
	@echo "Building English version HTML files."
	make html

	@echo
	@echo "Move Chinese version back."
	mv _build/html_zh_CN _build/html/zh_CN
