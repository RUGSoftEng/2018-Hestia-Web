## To use this document generator, you require:
##      - pandoc
##      - some latex installation that pandoc may leverage
##
## Additionally, we rely on some features related to table generation from the deprecated markdown_github format (as opposed to gfm)
## so ignore the deprecated WARNING.


cd architecture
pandoc --from=markdown_github -o HestiaWeb_architecture.pdf  HestiaWeb_architecture.md

cd ..

cd requirements
cat HestiaWeb_requirements.md | sed 's/\[x\]/\$\\checkmark\$/g'| sed 's/\[ \]/\$\\square\$/g' | pandoc --from=markdown_github+tex_math_dollars --mathjax -o HestiaWeb_requirements.pdf


