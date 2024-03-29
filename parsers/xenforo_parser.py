# -*- coding: utf-8 -*-
import re
import os
import json
import codecs
import pathlib

from xml.etree import ElementTree


def clean_html(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def parse_one_file(filename):
    """
    Parses localization values given a file
    :param filename: configurations file path
    :return: dict of key (English term) -> value (given language term)
    """
    with codecs.open(filename, "r", encoding='utf-8', errors='ignore') as f:
        tree = ElementTree.parse(f)

    d = {}
    for node in tree.iter('phrase'):
        if node.attrib['title'] is None:
            continue
        cleaned_key = clean_html(node.attrib['title'])
        if node.text is None:
            continue
        cleaned_value = clean_html(node.text)
        d[cleaned_key] = cleaned_value
    return d


def get_all_files(directoryname):
    """
    Gets all configurations files inside a directory, parses them using parse_one_file function
    :param directoryname: directory
    :return: dumps localization dictionaries in JSON format
    """
    for path, subdirs, files in os.walk(directoryname):
        localization_values = {}
        language = os.path.basename(path)
        for name in files:
            file_name = pathlib.PurePath(path, name)
            localization_values.update(parse_one_file(file_name))
        print(len(localization_values))
        with open(language.lower()+'.json', 'w', encoding='utf-16') as f:
            json.dump(localization_values, f, ensure_ascii=False)


if __name__ == "__main__":
    path = 'Forums/xenforo'
    get_all_files(path)
