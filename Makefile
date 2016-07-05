TEX_SOURCES = $(shell ls collection/*.tex)

HTML_TARGETS = $(patsubst collection/%.tex, html_collection/%.html, $(TEX_SOURCES))

all: $(HTML_TARGETS)

init:
	./decoupeWagons.py

html_collection/%.html : collection/%.tex
	@echo -n "$< ==> $@ ... "
	./tex2html $<
	@echo [Done]

clean:
	rm -f html_collection/file*

distclean: clean
	rm -f html_collection/*.html collection/*.tex
