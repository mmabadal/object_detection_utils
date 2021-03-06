

import os
import re
import glob
import sys
import argparse
import pandas as pd
import xml.etree.ElementTree as ET

'''
call:
python xml_to_txt.py --path_in a/b --path_out c/d

'''


def xml_to_txt(xml_file):

    values = list()

    tree = ET.parse(xml_file)
    root = tree.getroot()
    for instance in root.findall('object'):

        if instance[0].text == "P. noctiluca" or instance[0].text == "pelagia":
            type = "noctiluca"
        elif instance[0].text == "R. pulmo":
            type = "pulmo"
        elif instance[0].text == "C. tuberculata" or instance[0].text == "C. tuberculata ":
            type = "tuberculata"
        else:
            print("salgo con: " + str(instance[0].text))

        value = (type,                        # class
                 str(instance[4][0].text),    # left
                 str(instance[4][1].text),    # top
                 str(instance[4][2].text),    # right
                 str(instance[4][3].text))    # bottom

        values.append(value)

    return values


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_in', help='xml input directory.')
    parser.add_argument('--path_out', help='txt output directory.')
    parsed_args = parser.parse_args(sys.argv[1:])

    dir_in = parsed_args.path_in
    dir_out = parsed_args.path_out

    for file in os.listdir(dir_in):

        if re.search("\.(xml)$", file):  # if the file is an image
            image_path = os.path.join(dir_in, file)
            instances = xml_to_txt(image_path)

            name_out = os.path.splitext(file)[0] + ".txt"

            file_out = os.path.join(dir_out, name_out)


            with open(file_out, 'w') as f:
                for instance in instances:
                    f.write(instance[0] + " " +
                            instance[1] + " " +
                            instance[2] + " " +
                            instance[3] + " " +
                            instance[4] + "\n")

    print('Successfully converted xml to txt.')

main()


