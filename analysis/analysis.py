"""
Script to perform some basic analysis on the bibliographic data Bibliographie18. 
"""


# === Imports === 

import re 
import seaborn as sns
from os.path import join
from lxml import etree
from io import StringIO, BytesIO
from collections import Counter


# === Files and parameters === 

bibdatafile = join("/", "media", "christof", "Data", "Github", "christofs", "bibliographie18", "formats", "bibliographie18_Zotero-RDF.rdf") 


# === Functions === 

def read_json(bibdatafile): 
    bibdata = etree.parse(bibdatafile)
    return bibdata


def most_frequent_persons(bibdata): 
    print("\npersonnames")
    # Setting things up
    personnames = []
    namespaces = {"foaf" : "http://xmlns.com/foaf/0.1/",
                  "bib" : "http://purl.org/net/biblio#"}

    # Find all the instances of persons
    xpath = "//foaf:Person"
    persons = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(persons))

    # Get the names (full name or first name, last name) from each person
    for item in persons: 
        if len(item) == 1: 
            personname = item[0].text
            personnames.append(personname)
        elif len(item) == 2: 
            personname = item[0].text + ", " + item[1].text 
            personnames.append(personname)    

    # Count the occurrences, find the 10 most frequently mentioned persons
    personnames_counts = Counter(personnames)
    print(len(personnames_counts))
    personnames_counts = dict(sorted(personnames_counts.items(), key = lambda item: item[1], reverse=True)[:10])
    print(personnames_counts)
    for item in personnames_counts: 
        print(item)


def most_frequent_publishers(bibdata): 
    print("\npublisher names")
    # Setting things up
    publishernames = []
    namespaces = {
        "foaf" : "http://xmlns.com/foaf/0.1/",
        "bib" : "http://purl.org/net/biblio#",
        "dc" : "http://purl.org/dc/elements/1.1/"
        }

    # Find all the instances of persons
    xpath = "//dc:publisher//foaf:name/text()"
    publishernames = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(publishernames))

    # Count the occurrences, find the 10 most frequently mentioned publishers
    publishernames_counts = Counter(publishernames)
    print(len(publishernames_counts))
    publishernames_counts = dict(sorted(publishernames_counts.items(), key = lambda item: item[1], reverse=True)[:11])
    print(publishernames_counts)



# === Main === 

def main(): 
    bibdata = read_json(bibdatafile) 
    most_frequent_persons(bibdata)
    most_frequent_publishers(bibdata)

main()
