"""
Script to perform some basic analysis on the bibliographic data Bibliographie18. 
"""


# === Imports === 

import re 
import seaborn as sns
from matplotlib import pyplot as plt
from os.path import join
from lxml import etree
from io import StringIO, BytesIO
from collections import Counter
import pandas as pd


# === Files and parameters === 

bibdatafile = join("/", "media", "christof", "Data", "Github", "christofs", "bibliographie18", "formats", "bibliographie18_Zotero-RDF.rdf") 

namespaces = {
    "foaf" : "http://xmlns.com/foaf/0.1/",
    "bib" : "http://purl.org/net/biblio#",
    "dc" : "http://purl.org/dc/elements/1.1/"
    }


# === Functions === 

def read_json(bibdatafile): 
    bibdata = etree.parse(bibdatafile)
    return bibdata


def most_frequent_persons(bibdata): 
    print("\npersonnames")

    # Setting things up
    personnames = []

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

    # Find all the instances of persons
    xpath = "//dc:publisher//foaf:name/text()"
    publishernames = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(publishernames))

    # Count the occurrences, find the 10 most frequently mentioned publishers
    publishernames_counts = Counter(publishernames)
    print(len(publishernames_counts))
    publishernames_counts = dict(sorted(publishernames_counts.items(), key = lambda item: item[1], reverse=True)[:11])
    print(publishernames_counts)



def most_frequent_pubyears(bibdata): 
    print("\npublication years")
    # Setting things up
    pubyears = []

    # Find all the instances of persons
    xpath = "//dc:date/text()"
    pubyears = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(pubyears))

    # Count the occurrences, find the 10 most frequently mentioned publishers
    pubyear_counts = Counter(pubyears)
    print(len(pubyear_counts))
    pubyear_counts = dict(sorted(pubyear_counts.items(), reverse=False))
    print(pubyear_counts)

    pubyear_counts = pd.DataFrame.from_dict(pubyear_counts, orient="index").reset_index().rename(mapper={"index":"year", 0 : "count"}, axis="columns")    #pubyear_counts = pubyear_counts[pubyear_counts[0] == 1991]
    pubyear_counts = pubyear_counts[pubyear_counts["year"].str.isnumeric()]
    pubyear_counts.set_index("year", inplace=True)
    pubyear_counts.drop(["134", "1815", "1834", "1891", "1932", "1945", "1957", "1961", "1969", "1973", "1974", "1975", "1978", "1979", "1981", "1982", "1983", "1984"], inplace=True)
    pubyear_counts.drop(["207", "22", "30", "42", "58", "76", "78", "20", "201"], inplace=True)
    pubyear_counts.reset_index(inplace=True)
    print(pubyear_counts.head())


    # Create figure
    plt.figure(figsize=(12,6))
    fig = sns.barplot(data = pubyear_counts, x="year", y="count")
    fig.set_xticklabels(fig.get_xticklabels(), rotation=45)
    plt.savefig("pubyear_counts.png")



# === Main === 

def main(): 
    bibdata = read_json(bibdatafile) 
    #most_frequent_persons(bibdata)
    #most_frequent_publishers(bibdata)
    most_frequent_pubyears(bibdata)

main()
