#/bin/env python3

import sys
import pandas as pd

LETTER_LAST_ROW = 233
NUMBERS_LAST_ROW = 134
UPPERCASE_COLUMN = 7
LOWERCASE_COLUMN = 17
NUMBERS_COLUMN = 27
ROW_PER_LETTER = 8

ch_enabled = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'W', 'Y',
               #'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
               'e', 'h', 'l', 'o', 'z',
               #'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               ':', ' ', '.' ] #, '?', '!' ]



def load_file(filename, default_width=6, widths={'1':4, 'I':4, 'i':4, 'l':4, 'j':5, ':':2, '.':2}, height=6):

    df = pd.read_excel(filename, header=None, dtype=str, keep_default_na=False)

    chr_data = {}
    data = []
    j = 0

    ch = 65 # A
    for i in range(0, LETTER_LAST_ROW):
        if not df.iloc[i].iloc[UPPERCASE_COLUMN]:
            continue
        data.append(df.iloc[i].iloc[UPPERCASE_COLUMN])
        j += 1
        if j == ROW_PER_LETTER:
            name = chr(ch)
            width = default_width
            if chr(ch) in widths:
                width = widths[chr(ch)]
            chr_data[chr(ch)] = { 'name':name, 'data':data, 'width':width, 'height':height}
            data = []
            j = 0
            ch += 1
    ch = 97 # a
    for i in range(0, LETTER_LAST_ROW):
        if not df.iloc[i].iloc[LOWERCASE_COLUMN]:
            continue
        data.append(df.iloc[i].iloc[LOWERCASE_COLUMN])
        j += 1
        if j == ROW_PER_LETTER:
            name = chr(ch)
            width = default_width
            if chr(ch) in widths:
                width = widths[chr(ch)]
            chr_data[chr(ch)] = { 'name':name, 'data':data, 'width':width, 'height':height}
            data = []
            j = 0
            ch += 1
    ch = 48 # 0
    for i in range(0, NUMBERS_LAST_ROW):
        hdata = df.iloc[i].iloc[NUMBERS_COLUMN]
        if not hdata:
            continue
        data.append(hdata)
        j += 1
        if j == ROW_PER_LETTER:
            width = default_width
            if 48 <= ch and ch <= 57:
                name = '_' + chr(ch)
                c = chr(ch)
            elif ch == 58:
                name = 'Colon'
                c = chr(ch)
            elif ch == 59:
                name = 'Space'
                c = ' '
            elif ch == 60:
                name = 'DecimalPlace'
                c = '.'
            elif ch == 61:
                name = 'QuestionMark'
                c = '?'
            elif ch == 62:
                name = 'ExclamationMark'
                c = '!'
            width = default_width
            if c in widths:
                width = widths[c]
            chr_data[c] = { 'name':name, 'data':data, 'width':width, 'height':height}
            data = []
            j = 0
            ch += 1
    return chr_data



if __name__ == '__main__':
    filename = sys.argv[1]

    chr_data = load_file(filename)

    height = 6
    width = 5

    i = 0
    AsciiChars = ''
    tableOfAsciiChars = ''
    for c in ch_enabled:
        if c in chr_data:
            i += 1
            data = ''.join([f', 0x{h}' for h in chr_data[c]["data"]][0:height])
            #data = ''.join([', 0x%02X' % (int(h, 16) >> 1) for h in chr_data[c]["data"]][1:height])

            AsciiChars += f'const char {chr_data[c]["name"]}_{width}x{height}[10] = {{ 6, {chr_data[c]["width"]}{data} }}; // {i}\n'
            tableOfAsciiChars += f'    {chr_data[c]["name"]}_{width}x{height}, // {i}\n'
            chr_data[c]['index'] = i
        else:
            print('error')
            exit(1)
    tableOfAsciiChars = f'const char * const tableOfAsciiChars[{i}] = {{\n'+ tableOfAsciiChars + '};\n'

    
    # Ascii_installed
    ascii_installed = 'const char Ascii_installed[0x80-0x20] = // Starts at 0x20, ends at 0x7f\n{\n'
    for i in range(0x20, 0x80):
        hex_value = '0x' + hex(i).upper()[2:]
        index = 0
        if chr(i) in ch_enabled:
            index = chr_data[chr(i)]['index']
        name = chr(i)
        if name == ' ':
            name = 'space'
        if i == 0x7F:
            name = 'del'
            if ' ' in ch_enabled:
                index = chr_data[' ']['index']
        ascii_installed += f'    {index}, // {name} {hex_value}\n'
    ascii_installed += '};\n'

    print(ascii_installed)
    print(AsciiChars)
    print(tableOfAsciiChars)

