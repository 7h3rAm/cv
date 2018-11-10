all: priyam ankur

priyam: PriyamTyagi.tex PriyamTyagi.yml
	pandoc $(filter-out $<,$^ ) -o PriyamTyagi.pdf --latex-engine=xelatex --template=$<

ankur: AnkurTyagi.tex AnkurTyagi.yml
	pandoc $(filter-out $<,$^ ) -o AnkurTyagi.pdf --latex-engine=xelatex --template=$<

clean:
	rm PriyamTyagi.pdf AnkurTyagi.pdf
