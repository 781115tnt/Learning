
set outdir=.\_out
mkdir "%outdir%"

@echo on
for %%i in (*.tif *.png *.jpg *.jpeg) do convert "%%i" -level 30%%,90%% -colors 64 -define png:color-type=3 "%outdir%\%%~ni.png"
