'''
# File: Extractor.py
# Project: DICE
# File Created: Thursday, 26th November 2020 2:47:01 pm
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Thursday, 26th November 2020 2:47:47 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institut de neurosciences de la Timone
'''


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral, PSKeyword
from pdfminer.utils import decode_text
from argparse import ArgumentParser
import pprint
import json


def load_fields(field):
    """
   Recursively load form fields

    Args:
        field (list): list of fields fill on the pdf

    Returns:
        dict: dictionary { name of the field : value of the field}
    """
    form = field.get('Kids', None)
    if form:
        return [load_fields(resolve1(f)) for f in form]
    else:
        # Some field types, like signatures, need extra resolving
        key = decode_value(field.get('T')) if not (field.get('T') is None) else field.get('T')
        value = resolve1(field.get('V'))
        dictionary_value = {key : value}
        for _ in dictionary_value :
            dictionary_value[_] = decode_value(dictionary_value[_])
            # if there is a list in value of the dictionary
            if isinstance(dictionary_value[_], list):
                    dictionary_value[_]=[decode_value(x) for x in dictionary_value[_]]
        return(dictionary_value)

def decode_value(value):
    """
    Decode bytes to string

    Args:
        value (byte): bytes to decode

    Returns:
        str: bytes decoded to str
    """
    # decode bytes
    if isinstance(value, bytes):
        value = decode_text(value)
    return value


def load_form(file):
    """
    Args:
        file (path): path to the PDF file

    Raises:
        ValueError: No AcroForm Found

    Returns:
         list: list of dict {name : values} from the pdf
    """
    with open(file, 'rb') as fp:
            parser = PDFParser(fp)
            pp = pprint.PrettyPrinter(indent=2)
            doc = PDFDocument(parser)
            res = resolve1(doc.catalog)

            if 'AcroForm' not in res:
                raise ValueError("No AcroForm Found")

            fields = resolve1(doc.catalog['AcroForm'])['Fields']  # may need further resolving
            res=list()
            for f in fields:
                res.append(load_fields(resolve1(f)).copy())

    return res


def parse_cli():
    """Load command line arguments"""
    parser = ArgumentParser(description='Dump the form contents of a PDF.')
    parser.add_argument('-d','--debug',action="store_true",
        help='PDF form to dump the contents of')
    parser.add_argument('file', metavar='pdf_form',
        help='PDF form to dump the contents of')
    parser.add_argument('-o', '--out', help='Write output to file',
        default=None, metavar='FILE')

    return parser.parse_args()

def main():
    args = parse_cli()
    form =load_form(args.file)
    if args.out:
        with open(args.out, 'w') as outfile:
                json.dump(form , outfile)

    if args.debug:
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(form)

if __name__ == '__main__':
    main()
