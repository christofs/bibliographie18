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



def get_personnames(bibdata): 
    print("\npersonnames")

    # Find all the instances of persons
    personnames = []
    xpath = "//foaf:Person"
    persons = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(persons), "instances of Element 'person'")

    # Get the names (full name or first name, last name) from each person
    for item in persons: 
        if len(item) == 1: 
            personname = item[0].text
            personnames.append(personname)
        elif len(item) == 2: 
            personname = item[0].text + ", " + item[1].text 
            personnames.append(personname)    
    return personnames



def get_number_collaborators(bibdata): 
    """
    Finds out how frequent collaborations (co-authorship, co-editorship) are.
    Number of "Person" elements within "authors" or "editors" element. 
    """
    print("\nNumber of collaborations with specific number of collaborators.")

    # Find all instances of authors
    num_coauthors = []
    xpath = "//bib:authors"
    authors = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(authors), "instances of Element 'authors'")
    num_coauthors = []
    for item in authors:
        #print(item)
        xpath = "rdf:Seq/rdf:li/foaf:Person"
        coauthors = item.xpath(xpath, namespaces=namespaces)
        num_coauthors.append(len(coauthors))
    num_coauthors_counts = Counter(num_coauthors)
    print(num_coauthors_counts)

    # Calculate percentages
    num_coauthors_perc = {}
    total = sum(num_coauthors_counts.values())
    for key,val in num_coauthors_counts.items():
        num_coauthors_perc[key] = str(round(val/total * 100, 3)) + '%'
    print(num_coauthors_perc)

    # Find all instances of editors
    num_coeditors = []
    xpath = "//bib:editors"
    editors = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(editors), "instances of Element 'editors'")
    num_coeditors = []
    for item in editors:
        xpath = "rdf:Seq/rdf:li/foaf:Person"
        coeditors = item.xpath(xpath, namespaces=namespaces)
        num_coeditors.append(len(coeditors))
    num_coeditors_counts = Counter(num_coeditors)
    print(dict(num_coeditors_counts))

    # Calculate percentages
    num_coeditors_perc = {}
    total = sum(num_coeditors_counts.values())
    for key,val in num_coeditors_counts.items():
        num_coeditors_perc[key] = str(round(val/total * 100, 2)) + '%'
    print(num_coeditors_perc)

        


def get_publishers(bibdata): 
    print("\npublisher names")

    # Find all the instances of publisher names
    publishers = []
    xpath = "//dc:publisher//foaf:name/text()"
    publishers = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(publishers))
    return publishers



def most_frequent_personnames(personnames): 
    # Count the occurrences, find the 10 most frequently mentioned persons
    personnames_counts = Counter(personnames)
    print(len(personnames_counts))
    personnames_counts = dict(sorted(personnames_counts.items(), key = lambda item: item[1], reverse=True)[:10])
    print(personnames_counts)
    for item in personnames_counts: 
        print(item)



def most_frequent_publishers(publishers):
    # Count the occurrences, find the 10 most frequently mentioned publishers
    publishernames_counts = Counter(publishers)
    print(len(publishernames_counts))
    publishernames_counts = dict(sorted(publishernames_counts.items(), key = lambda item: item[1], reverse=True)[:11])
    print(publishernames_counts)



def get_pubyears(bibdata): 
    print("\npublication years")
    # Setting things up
    pubyears = []

    # Find all the instances of persons
    xpath = "//dc:date/text()"
    pubyears = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(pubyears), "instances")

    # Count the occurrences, find the 10 most frequently mentioned publishers
    pubyear_counts = Counter(pubyears)
    print(len(pubyear_counts), "types")
    pubyear_counts = dict(sorted(pubyear_counts.items(), reverse=False))
    #print(pubyear_counts)

    # Filter data to clean it
    pubyear_counts = pd.DataFrame.from_dict(pubyear_counts, orient="index").reset_index().rename(mapper={"index":"year", 0 : "count"}, axis="columns")    #pubyear_counts = pubyear_counts[pubyear_counts[0] == 1991]
    pubyear_counts = pubyear_counts[pubyear_counts["year"].str.isnumeric()]
    pubyear_counts.set_index("year", inplace=True)
    # Remove erroneous years (to be corrected in the data)
    pubyear_counts.drop(["134", "207", "22", "30", "42", "58", "76", "78", "20", "201"], inplace=True)
    # Remove less relevant years (optional, of course)
    pubyear_counts.drop(["1815", "1834", "1891", "1932", "1945", "1957", "1961", "1969", "1973", "1974", "1975", "1978", "1979", "1981", "1982", "1983", "1984"], inplace=True)
    pubyear_counts.reset_index(inplace=True)
    #print(pubyear_counts.head())
    return pubyear_counts



def visualize_pubyears(pubyear_counts):
    plt.figure(figsize=(12,6))
    fig = sns.barplot(data = pubyear_counts, x="year", y="count")
    fig.set_xticklabels(fig.get_xticklabels(), rotation=45)
    plt.savefig(join(wdir, "figures", "pubyear_counts.png"))



def get_pubtypes(bibdata): 
    print("\nPublication types")

    # Find all the instances of publication types
    pubtypes = []
    xpath = "//z:itemType/text()"
    pubtypes = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(pubtypes), "instances of publication type")
    return pubtypes



def most_frequent_pubtypes(pubtypes): 
    # Count the occurrences, find the 10 most frequently mentioned persons
    pubtypes_counts = Counter(pubtypes)
    print(len(pubtypes_counts), "types of publication types")
    pubtypes_counts = dict(sorted(pubtypes_counts.items(), key = lambda item: item[1], reverse=True)[:10])
    print(pubtypes_counts)




def network_coeditors(bibdata): 
    # Find all instances of editors
    xpath = "//bib:editors"
    editors = bibdata.xpath(xpath, namespaces=namespaces)
    print(len(editors), "instances of Element 'editors'")

    # Collect the names of each person within each editors element
    coeditors = []
    for item in editors:
        xpath = "rdf:Seq/rdf:li/foaf:Person"
        coeditors_elements = item.xpath(xpath, namespaces=namespaces)
        coeditors_names = []
        # Get the names (full name or first name, last name) from each person
        for item in coeditors_elements: 
            if len(item) == 2: 
                coeditors_names.append(item[0].text + ", " + item[1].text)
        #print(coeditors_names)
        coeditors.append(coeditors_names)
    #print(all_coeditors)

    # Establish the count of each collaboration between editors
    import itertools 
    all_coeditor_combinations = []
    for item in coeditors: 
        coeditor_combinations = list(itertools.combinations(item, 2))
        coeditor_combinations = [tuple(sorted(item)) for item in coeditor_combinations]
        for coedcomb in coeditor_combinations: 
            all_coeditor_combinations.append(coedcomb)
    ccc = dict(Counter(all_coeditor_combinations)) # ccc = coeditor_combinations_count

    # Transform to a DataFrame
    ccc = pd.DataFrame.from_dict(ccc, orient="index", columns=["count"])
    ccc = ccc.reset_index()
    ccc_split = pd.DataFrame(ccc["index"].tolist())
    ccc_merged = ccc_split.merge(ccc, left_index=True, right_index=True)
    ccc = ccc_merged.drop(["index"], axis=1)
    ccc = ccc.rename({0 : "coeditor1", 1 : "coeditor2"}, axis=1)
    ccc = ccc.sort_values(by="count", ascending=False)
    print(ccc.head())
    with open(join(wdir, "coeditor-counts.csv"), "w", encoding="utf8") as outfile: 
        ccc.to_csv(outfile, sep=";")









        








    

# === Main === 

def main(): 
    bibdata = read_json(bibdatafile)
    #pubtypes = get_pubtypes(bibdata)
    #most_frequent_pubtypes(pubtypes)
    #pubyear_count = get_pubyears(bibdata)
    #visualize_pubyears(pubyear_count)
    #personnames = get_personnames(bibdata)
    #most_frequent_personnames(personnames)
    #get_number_collaborators(bibdata)
    network_coeditors(bibdata)
    #publishers = get_publishers(bibdata)
    #most_frequent_publishers(publishers)


main()
