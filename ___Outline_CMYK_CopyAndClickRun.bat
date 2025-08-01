mkdir _outline_cmyk
for %%i in (*.pdf) do gswin64 -dSAFER -dBATCH -sDEVICE=pdfwrite  -sFONTPATH=%windir%/fonts -dEmbedAllFonts=true  -sColorConversionStrategy=CMYK -dNoOutputFonts -o ".\_outline_cmyk\%%i" ".\%%i"
