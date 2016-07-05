TEX_SOURCES = $(shell ls collection/*.tex)

HTML_TARGETS = $(patsubst collection/%.tex, html_collection/%.html, $(TEX_SOURCES))

all: $(HTML_TARGETS)

init:
	# découpe les questions qui sont dans les sous-répertoires
	# autres que *collection* et les enregistre dans
	# collection/
	./decoupeWagons.py
	# crée l'index de nos données pour la recherche
	index++ -c train.conf collection

html_collection/%.html : collection/%.tex
	@echo -n "$< ==> $@ ... "
	./tex2html $<
	@echo [Done]

clean:
	rm -f html_collection/file*

distclean: clean
	rm -f html_collection/*.html collection/*.tex
