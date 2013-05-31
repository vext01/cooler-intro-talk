all:
	pdflatex talk
	pkill -HUP mupdf
