"""
Scripts to perform some analyses of the bibliographic data Bibliographie18. 
This script focuses on aspects of collaboration, like co-authorship or co-editorship. 
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

def read_xml(bibdatafile): 
    bibdata = etree.parse(bibdatafile)
    return bibdata



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



def network_coeditors(bibdata): 
    """
    Builds the data for a network of people having collaborated as editors. 
    """
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
        coeditors.append(coeditors_names)

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
    #print(ccc.head())
    print(ccc.shape, "shape of dataframe")
    with open(join(wdir, "data", "coeditor-counts_full.csv"), "w", encoding="utf8") as outfile: 
        ccc.to_csv(outfile, sep=";")

    # Filter the DataFrame to make it manageable for visualization
    # Determine the top N most frequent co-editors
    coeditors_top = list(set(list(ccc.head(20).loc[:,"coeditor1"]) +\
        list(ccc.head(20).loc[:,"coeditor2"])))
    #print(coeditors_top)
    print(len(coeditors_top), "number of top co-editors")
    # Filter the DataFrame to include just the collaborations involving at least one of the top co-editors. 
    # The resulting DataFrame will have all collaborations between the top co-editors and their co-editors. 
    ccc_filtered = ccc[(ccc["coeditor1"].isin(coeditors_top)) |\
                       (ccc["coeditor2"].isin(coeditors_top))]
    print(ccc_filtered.shape, "shape of dataframe of top co-editors and their co-editors.")
    # Simplify the labels 
    #ccc_filtered = ccc_filtered.replace(' .*?]', '',regex=True).astype(str)
    ccc_filtered['coeditor1'] =  [re.sub(r', .*','', str(x)) for x in ccc_filtered['coeditor1']]
    ccc_filtered['coeditor2'] =  [re.sub(r', .*','', str(x)) for x in ccc_filtered['coeditor2']]
    print(ccc_filtered.head())
    with open(join(wdir, "data", "coeditor-counts_top.csv"), "w", encoding="utf8") as outfile: 
        ccc_filtered.to_csv(outfile, sep=";")



# === Main === 

def main(): 
    bibdata = read_xml(bibdatafile)
    get_number_collaborators(bibdata)
    network_coeditors(bibdata)

main()
