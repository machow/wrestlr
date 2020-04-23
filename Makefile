all: docs

docs: README.md

README.md: README.Rmd
	rm -f README_files/*
	jupytext --from Rmd --to ipynb --output - $^ \
		| jupyter nbconvert --stdin --to markdown --execute --output $@
	
