mkdir _cmyk
for %%i in (*.pdf) do gswin64 -dSAFER -dBATCH -sDEVICE=pdfwrite -sFONTPATH=%windir%/fonts -dEmbedAllFonts=true  -sColorConversionStrategy=CMYK -o ".\_cmyk\%%i" ".\%%i"
