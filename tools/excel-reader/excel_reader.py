#!/usr/bin/env python3
"""Simple Excel and CSV reader without external dependencies."""

import csv
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {
    'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
}


def column_index(cell_ref: str) -> int:
    """Convert column letters to zero-based index."""
    col = ''.join(ch for ch in cell_ref if ch.isalpha())
    idx = 0
    for ch in col:
        idx = idx * 26 + (ord(ch.upper()) - 64)
    return idx - 1


def read_xlsx(path: str) -> None:
    """Read an .xlsx file and print its contents."""
    with zipfile.ZipFile(path) as z:
        shared_strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            root = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in root.findall('.//main:si', NS):
                text = ''.join(t.text or '' for t in si.findall('.//main:t', NS))
                shared_strings.append(text)

        sheets = [n for n in z.namelist() if n.startswith('xl/worksheets/sheet')]
        for sheet in sorted(sheets):
            print(f"# Sheet: {sheet.split('/')[-1]}")
            xml_bytes = z.read(sheet)
            root = ET.fromstring(xml_bytes)
            data = root.find('main:sheetData', NS)
            if data is None:
                continue
            for row in data.findall('main:row', NS):
                cells = []
                last_idx = -1
                for c in row.findall('main:c', NS):
                    ref = c.attrib.get('r', '')
                    idx = column_index(ref)
                    # fill blanks if needed
                    while last_idx + 1 < idx:
                        cells.append('')
                        last_idx += 1
                    t = c.attrib.get('t')
                    v_elem = c.find('main:v', NS)
                    val = ''
                    if v_elem is not None and v_elem.text is not None:
                        val = v_elem.text
                        if t == 's':
                            try:
                                val = shared_strings[int(val)]
                            except (ValueError, IndexError):
                                pass
                    cells.append(val)
                    last_idx = idx
                print('\t'.join(cells))
            print()


def read_csv(path: str) -> None:
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print('\t'.join(row))


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: excel_reader.py <file.xlsx|file.csv>")
        return
    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        return
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        read_csv(path)
    elif ext in ('.xlsx', '.xls'):  # .xls treated same as .xlsx here
        read_xlsx(path)
    else:
        print(f"Unsupported file type: {ext}")


if __name__ == '__main__':
    main()
