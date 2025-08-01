@echo off
chcp 65001
echo "Batch chuyển 1bit TIF sang Gray TIFF"

set outdir=.\_out
mkdir "%outdir%"

@echo on
for %%i in (*.tif) do convert "%%i" -set colorspace Gray -separate -average "%outdir%\%%i"
