AnkurTyagi.pdf: template.tex AnkurTyagi.yml
	pandoc $(filter-out $<,$^ ) -o AnkurTyagi.pdf --latex-engine=xelatex --template=$<

clean:
	rm AnkurTyagi.pdf
