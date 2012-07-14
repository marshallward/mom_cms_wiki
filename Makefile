RSTDOC = mom.txt
HTMLDOC = tmp.html
WIKIDOC = wiki.txt

.PHONY: makewiki
makewiki: ${RSTDOC}
	rst2html ${RSTDOC} > ${HTMLDOC}
	pandoc -f html -t mediawiki -o ${WIKIDOC} ${HTMLDOC}
	rm ${HTMLDOC}
	python mw2wt.py ${WIKIDOC}
	mv ${WIKIDOC}~ ${WIKIDOC}

.PHONY: clean
clean:
	rm ${HTMLDOC} ${WIKIDOC} ${WIKIDOC}~
