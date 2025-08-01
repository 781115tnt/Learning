@echo on

for %%i in (*.pdf) do java -jar c:\_ThanhBinh\PDFBox\pdfbox-app-2.0.34.jar PDFSplit -split 2 "%%i"

