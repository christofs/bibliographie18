"""
Script to perform some basic analysis on the bibliographic data Bibliographie18. 
"""


# === Imports === 

import re 
import seaborn as sns
from matplotlib import pyplot as plt
from os.path import join
from os.path import realpath, dirname
import os
from lxml import etree
from io import StringIO, BytesIO
from collections import Counter
import pandas as pd



# === Files and parameters === 

wdir  = realpath(dirname(__file__))
bibdatafile = join(wdir, "..", "formats", "bibliographie18_Zotero-RDF.rdf") 
#bibdatafile = join(wdir, "..", "formats", "bibliographie18_Zotero-RDF_TEST.rdf") 

namespaces = {
    "foaf" : "http://xmlns.com/foaf/0.1/",
    "bib" : "http://purl.org/net/biblio#",
    "dc" : "http://purl.org/dc/elements/1.1/",
    "z" : "http://www.zotero.org/namespaces/export#",
    "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    }



# === Functions === 

def read_json(bibdatafile): 
    bibdata = etree.parse(bibdatafile)
    return bibdata



def get_titles(bibdata): 
    print("\nTitles")

    # Find all "title" elements in the dataset 
    # All titles
    xpath = "//dc:title/text()"
    # Only primary titles (books, articles, chapters, not journal names)
    ##xpath = "//bib:Article/dc:title/text()"
    titles = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(titles), "titles")
    return titles



def get_titlewords(titles): 
    print("\nWords in titles")
    titlewords = []
    for title in titles: 
        titlewords.extend(re.split("\W+", title))
    titlewords_counts = dict(Counter(titlewords))
    titlewords_counts = dict(sorted(titlewords_counts.items(), key = lambda item: item[1], reverse=True)[:50])
    stopwords = ["de", "et", "la", "des", "du", "the", "", "and", "of"]
    for key in stopwords: 
        titlewords_counts.pop(key)
    print(titlewords_counts)




# === Main === 

def main(): 
    bibdata = read_json(bibdatafile)
    titles = get_titles(bibdata)
    titlewords = get_titlewords(titles)

main()
