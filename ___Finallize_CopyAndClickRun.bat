mkdir _finallize
for %%i in (*.pdf) do gswin64 -dSAFER -dBATCH -sDEVICE=pdfwrite -sFONTPATH=%windir%/fonts -dEmbedAllFonts=true  -o ".\_finallize\%%i" ".\%%i"
