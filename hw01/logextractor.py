# -*- coding: utf-8 -*-
import sys
import re
import xlsxwriter


def parseFile(filename):
    pattern = r'[\s=\b]+'
    data = {}
    with open(filename, 'rb') as file:
        for line in file:
            str = line.decode()
            if 'Isotropic' in str:
                elements = re.split(pattern, str.strip())
                elements.remove('Isotropic')
                elements.remove('Anisotropy')
                if elements[1] not in data.keys():
                    data[elements[1]] = []
                data[elements[1]].append(elements)
    return data


def saveToExcel(filename, data):
    wb = xlsxwriter.Workbook(filename)
    for atom in data.keys():
        ws = wb.add_worksheet(name=atom)
        options = {
            'data':
            data[atom],
            'columns': [{
                'header': 'No.'
            }, {
                'header': 'Atom'
            }, {
                'header': 'Isotropic'
            }, {
                'header': 'Anisotropy'
            }]
        }
        ws.add_table(0, 0, len(data[atom]), len(data[atom][0]) - 1, options)


if __name__ == "__main__":
    logFilename = sys.argv[1]
    if len(sys.argv) > 2:
        excelFilename = sys.argv[2]
    else:
        excelFilename = logFilename.replace('.log', '.xlsx')
    data = parseFile(logFilename)
    saveToExcel(excelFilename, data)
