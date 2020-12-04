'''
This code can be used to extract metadata from a PDF form following the DigLab layout.
Example:

    $ python Extractor.py  --debug -s -o [output file]  [inputfile]


usage:

Extractor.py [-h] [-d] [-o FILE] [-s] [-a DIR] pdf_form

Dump the form contents of a PDF.

positional arguments:
    pdf_form             PDF form to dump the contents of

optional arguments:
    -h, --help           show this help message and exit
    -d, --debug          PDF form to dump the contents of
    -o FILE, --out FILE  Write output to file
    -s, --safe           Safe mode that do not allow overwriting output file
    -a DIR, --ando DIR   Create a directory from the Diglab from

# File: Extractor.py
# Project: DICE
# File Created: Friday, 27th November 2020 9:50:16 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Monday, 30th November 2020 5:15:03 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institue de neurosciences de la Timone
'''

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral, PSKeyword
from pdfminer.utils import decode_text
from argparse import ArgumentParser
import pprint
import json
import os
import datetime



def get_all(data):
        """
        tranform a list of dict to a dict

        Args:
            data ([list]): list of dict , information get from the pdf

        Returns:
            [d]: dictionary

        TODO: maybe do this recursively
        """
        d = dict(data[0])
        for state in data:
            if isinstance(state,list):
                for i in state:
                    d.update(**i)
            else :
                d.update(**state)
        return d

def create_AnDO(dictFromPDF,pathToDir):
    """
    Create directory from PDF information

    Args:
        dictFromPDF (dict): dict with information filled from the PDF
        pathToDir (str): path to directory where the AnDO structure will be created
    """

    dirnames=list()
    dic=get_all(dictFromPDF)
    dirnames.append("exp-"+str(dic["expName"])+"/"+"sub-"+str(dic["guid"])+"/"+'ses-'
                +str(datetime.datetime.strptime(dic["dateSession"], "%d/%m/%Y").strftime("%Y%m%d"))+"_"+str(dic["sesNumber"])+"_"+str(dic["customSesField"])+"/derivatives")
    dirnames.append("exp-"+str(dic["expName"])+"/"+"sub-"+str(dic["guid"])+"/"+'ses-'
                +str(datetime.datetime.strptime(dic["dateSession"], "%d/%m/%Y").strftime("%Y%m%d"))+"_"+str(dic["sesNumber"])+"_"+str(dic["customSesField"])+"/rawdata")
    dirnames.append("exp-"+str(dic["expName"])+"/"+"sub-"+str(dic["guid"])+"/"+'ses-'
                +str(datetime.datetime.strptime(dic["dateSession"], "%d/%m/%Y").strftime("%Y%m%d"))+"_"+str(dic["sesNumber"])+"_"+str(dic["customSesField"])+"/metadata")

    for directory in dirnames:

            try:
                # Create the directories is they do not exist
                os.makedirs(pathToDir+'/'+str(directory))
            except OSError:
                # Error handling when directory already exists
                print("Creation of the directory %s failed, already exist" % directory)
            else:
                print("Successfully created the directory %s " % directory)


def load_fields(field):
    """
   Recursively load form fields

    Args:
        field (list): list of fields fill on the pdf

    Returns:
        dict: dictionary { name of the field : value of the field}

    TODO: Their is no field called child anymore. Keeping it in case of a new structure format, care double check on the Field.get('T')) to remove
    
    """
    form = field.get('Kids', None)
    if form:
       #return [load_fields(resolve1(f)) for f in form]
       pass
    else:
        # Some field types, like signatures, need extra resolving
        key = decode_value(field.get('T')) if (str(field.get('T')) != None) else field.get('T')
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
                if load_fields(resolve1(f)) == None  :
                    continue
                else :
                     res.append( load_fields(resolve1(f)))

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
    parser.add_argument('-s', '--safe', help='Safe mode that do not allow overwriting output file',
        action="store_true",  default=None)
    parser.add_argument('-a', '--ando', help='Create a directory from the Diglab from',
        default=None, metavar='DIR')

    return parser.parse_args()

def main():
    args = parse_cli()
    form =load_form(args.file)
    if args.out:
        if args.safe and os.path.isfile(args.out):
            print("WARNING : safe mode does not allow to overwrite file ")
            exit(1)
        else :
            with open(args.out, 'w') as outfile:
                    json.dump(form , outfile)

    if args.ando:
        create_AnDO(form,args.ando)


    if args.debug:
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(form)

if __name__ == '__main__':
    main()
