#pip install PyPDF2
import os
from PyPDF2 import PdfReader, PdfWriter

fileName = "test_pdf-file"

range3ToDau="2-4,7,10-12"
rangeKienTruc="2-4,7,10-12"
rangeKetCau="2-4,7,10-12"
rangeDien="2-4,7,10-12"
rangeGio="2-4,7,10-12"
rangeNuoc="2-4,7,10-12"

#outDir3ToDau=".\\0 3ToDau\\"
#outDirKienTruc=".\\1 KienTruc\\"
#outDirKetCau=".\\2 KetCau\\"
#outDirDien=".\\3 Dien\\"
#outDirGio=".\\4 Gio\\"
#outDirNuoc=".\\5 Nuoc\\"

outDir3ToDau="./0 3ToDau/"
outDirKienTruc="./1 KienTruc/"
outDirKetCau="./2 KetCau/"
outDirDien="./3 Dien/"
outDirGio="./4 Gio/"
outDirNuoc="./5 Nuoc/"





def parse_ranges(s):
    """Parse '2-4,7,10-12' into list of (start, end) tuples, 1-based."""
    result = []
    for part in s.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            result.append((start, end))
        else:
            n = int(part)
            result.append((n, n))
    return result

def pdf_split_ranges(filename, rangeString, outDir):
    reader = PdfReader(f"{fileName}.pdf")

    ranges = parse_ranges(rangeString)

    os.makedirs(outDir, exist_ok=True)

    # Split PDF for each range
    for start, end in ranges:
        writer = PdfWriter()
        # PDF pages are 0-based
        for i in range(start-1, end):
            if 0 <= i < len(reader.pages):
                writer.add_page(reader.pages[i])

        output_name = f"{outDir}{fileName}[{start}-{end}].pdf"
        with open(output_name, "wb") as f:
            writer.write(f)
        print(f"Created: {output_name}")


pdf_split_ranges(fileName, range3ToDau, outDir3ToDau)
pdf_split_ranges(fileName, rangeKienTruc, outDirKienTruc)
pdf_split_ranges(fileName, rangeKetCau, outDirKetCau)
pdf_split_ranges(fileName, rangeDien, outDirDien)
pdf_split_ranges(fileName, rangeGio, outDirGio)
pdf_split_ranges(fileName, rangeNuoc, outDirNuoc)

print("DONE!!!!!!!!!!!!!!!!!!!!!!!")
