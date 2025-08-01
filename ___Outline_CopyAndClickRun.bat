mkdir _outline
for %%i in (*.pdf) do gswin64 -dSAFER -dBATCH -sDEVICE=pdfwrite -sFONTPATH=%windir%/fonts -dEmbedAllFonts=true  -dNoOutputFonts -o ".\_outline\%%i" ".\%%i"
