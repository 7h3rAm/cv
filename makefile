all: priyam ankur

priyam: PriyamTyagi.tex PriyamTyagi.yml
	@echo "building PriyamTyagi.pdf..."
	@pandoc -f markdown $(filter-out $<,$^ ) -o PriyamTyagi.pdf --pdf-engine=xelatex --template=$< 2>&1 | grep -Ev "(underbar|underline).*changed|current package is valid" || true

ankur: AnkurTyagi.tex AnkurTyagi.yml
	@echo "building AnkurTyagi.pdf..."
	@pandoc -f markdown $(filter-out $<,$^ ) -o AnkurTyagi.pdf --pdf-engine=xelatex --template=$< 2>&1 | grep -Ev "(underbar|underline).*changed|current package is valid" || true

clean:
	rm PriyamTyagi.pdf AnkurTyagi.pdf
