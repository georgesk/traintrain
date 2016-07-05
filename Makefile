TEX_SOURCES = $(shell ls collection/*.tex)

HTML_TARGETS = $(patsubst collection/%.tex, html_collection/%.html, $(TEX_SOURCES))

all: $(HTML_TARGETS)

init:
	# découpe les questions qui sont dans les sous-répertoires
	# autres que *collection* et les enregistre dans
	# collection/
	./decoupeWagons.py
	find collection/ -name "*.png" -o -name "*.jpg" -o -name "*.gif" -o -name "*.pdf" -o -name "*.eps" -exec cp {} html_collection/ \;
	# crée l'index de nos données pour la recherche
	index++ -c train.conf collection

html_collection/%.html : collection/%.tex
	@echo -n "$< ==> $@ ... "
	@ rm -f logfile.log
	@./tex2html $<  >> logfile.log
	@echo [Done]

clean:
	rm -f html_collection/file*
	rm -f logfile.log

distclean: clean
	find . -type -d -name decoupe | xargs rm -rf
	rm -f html_collection/*.html html_collection/img* html_collection/#*
	rm -f collection/*

