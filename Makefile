all: docs

docs: README.md

README.md: README.Rmd
	jupytext --from Rmd --to ipynb --output - $^ \
		| jupyter nbconvert --stdin --to markdown --execute --output $@
	
