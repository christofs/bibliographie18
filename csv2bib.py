"""
Script to transform data from a CSV file to BibTeX.
""" 

# === Imports === 

from os.path import join
import re
import csv 
import pandas as pd

# === Parameters === 

csvfile = join("xviiie_siecle_bibliographie_complet_1_550_cs.csv")


# === Functions === 

# === Read the CSV file ===

def read_csv(csvfile): 
    with open(csvfile, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep="\t")
    return data


# === Collect individual pieces of information ===

def get_authorinfo(str_author): 
    if type(str_author) == str: 
        info_author = re.sub(" et ", " and ", str_author)
    else: 
        info_author = str(str_author)
    if info_author == "nan": 
        info_author = ""
    return info_author


def get_editorinfo_edvol(str_editor): 
    """
    Transform info on editors of edited volumes or books. 
    Typical entries: 
    - "Albertan-Coppola, Sylviane (édit.)"
    - "Aldcroft, Derek H. et Anthony Sutcliffe (édit.)"
    - "Abdela, Sophie, Simon Dagenais et Julien Perrier-Chartrand (édit.)"
    Due to the inconsistency of the input, some errors are inevitable here. 
    Zotero will flip first and last name correctly on import. 
    """
    if type(str_editor) == str: 
        # Remove parts that are not the names
        info_editor = re.sub(" \(édit\.\)", "", str_editor)
        # Replace "et" separator by standard BibTeX "and"
        info_editor = re.sub(" et ", " and ", info_editor)
        # Replace all but first ", " separator by standard BibTeX "and"
        info_editor = re.sub("(.*?)(, )(.*?)(, )(.*?)(, )(.*?)", "\\1\\2\\3 and \\5 and \\7", info_editor)
        info_editor = re.sub("(.*?)(, )(.*?)(, )(.*?)", "\\1\\2\\3 and \\5", info_editor)
    else: 
        info_editor = str(str_editor)
    if info_editor == "nan": 
        info_editor = ""
    return info_editor


def get_editorinfo_chapter(str_editor): 
    """
    Transform info on editors of edited volumes or books. 
    Typical entries: 
    - "Valentine Zuber, Patrick Cabanel et Raphaël Liogier (édit.)"
    Due to the inconsistency of the input, some errors are inevitable here. 
    Zotero will flip first and last name correctly on import. 
    """
    if type(str_editor) == str: 
        # Remove parts that are not the names
        info_editor = re.sub(" \(édit\.\)", "", str_editor)
        # Replace "et" and "," separator by standard BibTeX "and"
        info_editor = re.sub(" et ", " and ", info_editor)
        info_editor = re.sub(", ", " and ", info_editor)
    else: 
        info_editor = str(str_editor)
    if info_editor == "nan": 
        info_editor = ""
    return info_editor



def get_titleinfo(str_title): 
    if type(str_title) == str: 
        info_title = str_title
    else: 
        info_title = str(str_title)
    # Fix issue with initial lower case
    info_title = re.sub("^la ", "La ", info_title)
    info_title = re.sub("^le ", "Le ", info_title)
    info_title = re.sub("^les ", "Les ", info_title)
    info_title = re.sub("^l'", "L'", info_title)
    return info_title


def get_info_year(str_date): 
    try: 
        info_year = re.findall("\d{4}", str(str_date))[0]
    except: 
        info_year = str(str_date)
    return info_year


def get_info_place(str_place): 
    if type(str_place) == str: 
        info_place = str_place
    else: 
        info_place = "s.l."
    return info_place


def get_info_publisher(str_publisher): 
    if type(str_publisher) == str: 
        info_publisher = str_publisher
    else: 
        info_publisher = "s.e."
    return info_publisher


def get_info_series(str_series): 
    if type(str_series) == str: 
        info_series = str_series
    else: 
        info_series = ""
    return info_series


def get_info_series_number(str_series_number): 
    if type(str_series_number) == str: 
        info_series_number = str_series_number
    elif type(str_series_number) == int: 
        info_series_number = str(str_series_number)
    else: 
        info_series_number = ""
    return info_series_number


def get_info_isbn(str_isbn): 
    if type(str_isbn) == str: 
        info_isbn = str_isbn
    else: 
        info_isbn = ""
    if len(info_isbn) > 10 and len(info_isbn) < 20: 
        info_isbn = re.sub(" ", "-", info_isbn)
    return info_isbn


def get_info_issn(str_issn):
    if type(str_issn) == str:
        info_issn = str_issn
    else: 
        info_issn = ""
    return info_issn


def get_info_url(str_url): 
    if type(str_url) == str: 
        info_url = str_url
    else: 
        info_url = ""
    info_url = re.sub("<", "", info_url)
    info_url = re.sub(">", "", info_url)
    return info_url


def get_info_abstract(str_abstract): 
    if type(str_abstract) == str: 
        info_abstract = str_abstract
        # Don't use "<" and ">" to mark urls. 
        info_abstract = re.sub("[<>]", "", info_abstract)
    else: 
        info_abstract = ""
    return info_abstract


def get_info_submitter(str_submitter): 
    if type(str_submitter) == str: 
        info_submitter = str_submitter
    else: 
        info_submitter = ""
    return info_submitter


def get_info_bookpages(str_bookpages): 
    if type(str_bookpages) == str: 
        try: 
            info_bookpages = re.findall("(\d+) p.", str_bookpages)[0]
        except: 
            info_bookpages = str_bookpages
    else: 
        info_bookpages = ""
    return info_bookpages


def get_info_language(info_title): 
    from lingua import Language, LanguageDetectorBuilder
    languages = [Language.ENGLISH,
                 Language.FRENCH,
                 Language.GERMAN,
                 Language.SPANISH,
                 Language.ITALIAN,
                 Language.PORTUGUESE,
                 Language.DUTCH,
                 Language.SWEDISH,
                 ]
    detector = LanguageDetectorBuilder.from_languages(*languages).build()
    confidence_values = detector.compute_language_confidence_values(info_title)
    languages = [language for language, value in confidence_values]
    values = [value for language, value in confidence_values]
    confidence_values_dict = dict(zip(languages, values))
    max_language = max(confidence_values_dict, key=confidence_values_dict.get)
    #print(max_language.name.title(), info_title)
    info_language = max_language.name.title()
    return info_language


def build_info_idno(idno, info_author, info_title, info_year): 
    short_author = re.split(",", info_author)[0].lower()
    short_author = re.sub(" ", "", short_author)
    short_year = re.sub("\D", "", info_year)
    info_idno = str(short_author) + "_" + str(short_year)
    return info_idno


def get_journaltitleinfo(str_journaltitle):
    if type(str_journaltitle) == str: 
        info_journaltitle = str_journaltitle
    else: 
        info_journaltitle = ""
    return info_journaltitle

def get_info_articlepages(str_pages): 
    try: 
        info_articlepages = re.findall("\d+[-–]+\d+", str_pages)[0]
        info_articlepages = re.sub("(\d+)[-–]+(\d+)", "\\1--\\2", info_articlepages)
    except:
        if type(str_pages) == str:  
            info_articlepages = str_pages
        else: 
            info_articlepages = ""
    return info_articlepages


def get_info_volume(str_volume): 
    if type(str_volume) == str: 
        info_volume = str_volume
    else: 
        info_volume = ""
    return info_volume


def get_info_issue(str_issue): 
    if type(str_issue) == str: 
        info_issue = str_issue
    else: 
        info_issue = ""
    return info_issue


def get_info_thesistype(str_thesistype): 
    if type(str_thesistype) == str: 
        info_thesistype = str_thesistype
    else: 
        info_thesistype = ""
    return info_thesistype


def get_info_mediatype(str_mediatype): 
    if type(str_mediatype) == str: 
        info_mediatype = str_mediatype
    else: 
        info_mediatype = ""
    return info_mediatype




# === Build BibTeX entries ===

def build_book_bibtex(
    info_type,
    info_idno,
    info_author,
    info_title,
    info_year,
    info_place,
    info_publisher,
    info_series,
    info_series_number,
    info_abstract,
    info_url,
    info_submitter,
    info_bookpages,
    info_isbn,
    info_language
    ): 
    bibtex = "@" + str(info_type) + "{" + str(info_idno) + ","\
             + "\n  author       = {" + str(info_author) + "},"\
             + "\n  title        = {" + str(info_title) + "},"\
             + "\n  address      = {" + str(info_place) + "},"\
             + "\n  publisher    = {" + str(info_publisher) + "},"\
             + "\n  series       = {" + str(info_series) + "},"\
             + "\n  number       = {" + str(info_series_number) + "},"\
             + "\n  year         = {" + str(info_year) + "},"\
             + "\n  isbn         = {" + str(info_isbn) + "},"\
             + "\n  abstract     = {" + str(info_abstract) + "},"\
             + "\n  url          = {" + str(info_url) + "},"\
             + "\n  pages        = {" + str(info_bookpages) + "},"\
             + "\n  language     = {" + str(info_language) + "},"\
             + "\n  extra        = {" + str(info_submitter) + "},"\
             + "\n}\n\n"
    return bibtex


def build_editedvol_bibtex(
    info_type,
    info_idno,
    info_editor,
    info_booktitle,
    info_year,
    info_place,
    info_publisher,
    info_series,
    info_series_number,
    info_abstract,
    info_url,
    info_submitter,
    info_bookpages,
    info_isbn,
    info_language
    ): 
    bibtex = "@" + str(info_type) + "{" + str(info_idno) + ","\
             + "\n  editor       = {" + str(info_editor) + "},"\
             + "\n  title        = {" + str(info_booktitle) + "},"\
             + "\n  address      = {" + str(info_place) + "},"\
             + "\n  publisher    = {" + str(info_publisher) + "},"\
             + "\n  series       = {" + str(info_series) + "},"\
             + "\n  number       = {" + str(info_series_number) + "},"\
             + "\n  year         = {" + str(info_year) + "},"\
             + "\n  isbn         = {" + str(info_isbn) + "},"\
             + "\n  abstract     = {" + str(info_abstract) + "},"\
             + "\n  url          = {" + str(info_url) + "},"\
             + "\n  pages        = {" + str(info_bookpages) + "},"\
             + "\n  language     = {" + str(info_language) + "},"\
             + "\n  extra        = {" + str(info_submitter) + "},"\
             + "\n}\n\n"
    return bibtex




def build_article_bibtex(
        info_type, 
        info_idno, 
        info_author, 
        info_title, 
        info_journaltitle, 
        info_volume, 
        info_issue, 
        info_articlepages, 
        info_year, 
        info_abstract,
        info_url,
        info_submitter,
        info_language
        ): 
    bibtex = "@" + str(info_type) + "{" + str(info_idno) + ","\
             + "\n  author       = {" + str(info_author) + "},"\
             + "\n  title        = {" + str(info_title) + "},"\
             + "\n  journal      = {" + str(info_journaltitle) + "},"\
             + "\n  volume       = {" + str(info_volume) + "},"\
             + "\n  number       = {" + str(info_issue) + "},"\
             + "\n  year         = {" + str(info_year) + "},"\
             + "\n  abstract     = {" + str(info_abstract) + "},"\
             + "\n  url          = {" + str(info_url) + "},"\
             + "\n  pages        = {" + str(info_articlepages) + "},"\
             + "\n  language     = {" + str(info_language) + "},"\
             + "\n  extra        = {" + str(info_submitter) + "},"\
             + "\n}\n\n"
    return bibtex



def build_chapter_bibtex(
    info_type, 
    info_idno, 
    info_author, 
    info_editor,
    info_chaptertitle, 
    info_booktitle, 
    info_year, 
    info_place,
    info_publisher,
    info_series,
    info_series_number,
    info_abstract,
    info_url,
    info_submitter,
    info_bookpages,
    info_isbn,
    info_language
    ): 
    bibtex = "@" + str(info_type) + "{" + str(info_idno) + ","\
             + "\n  author       = {" + str(info_author) + "},"\
             + "\n  editor       = {" + str(info_editor) + "},"\
             + "\n  title        = {" + str(info_chaptertitle) + "},"\
             + "\n  book         = {" + str(info_booktitle) + "},"\
             + "\n  address      = {" + str(info_place) + "},"\
             + "\n  publisher    = {" + str(info_publisher) + "},"\
             + "\n  series       = {" + str(info_series) + "},"\
             + "\n  number       = {" + str(info_series_number) + "},"\
             + "\n  year         = {" + str(info_year) + "},"\
             + "\n  isbn         = {" + str(info_isbn) + "},"\
             + "\n  abstract     = {" + str(info_abstract) + "},"\
             + "\n  url          = {" + str(info_url) + "},"\
             + "\n  pages        = {" + str(info_bookpages) + "},"\
             + "\n  language     = {" + str(info_language) + "},"\
             + "\n  extra        = {" + str(info_submitter) + "},"\
             + "\n}\n\n"
    return bibtex


def build_thesis_bibtex(
        info_type, 
        info_idno, 
        info_author,
        info_booktitle, 
        info_year, 
        info_place,
        info_university,
        info_thesistype,
        info_series,
        info_series_number,
        info_abstract,
        info_url,
        info_submitter,
        info_bookpages,
        info_isbn,
        info_language
    ): 
    bibtex = "@" + str(info_type) + "{" + str(info_idno) + ","\
             + "\n  author       = {" + str(info_author) + "},"\
             + "\n  title        = {" + str(info_booktitle) + "},"\
             + "\n  address      = {" + str(info_place) + "},"\
             + "\n  university   = {" + str(info_university) + "},"\
             + "\n  type         = {" + str(info_thesistype) + "},"\
             + "\n  series       = {" + str(info_series) + "},"\
             + "\n  number       = {" + str(info_series_number) + "},"\
             + "\n  year         = {" + str(info_year) + "},"\
             + "\n  isbn         = {" + str(info_isbn) + "},"\
             + "\n  abstract     = {" + str(info_abstract) + "},"\
             + "\n  url          = {" + str(info_url) + "},"\
             + "\n  pages        = {" + str(info_bookpages) + "},"\
             + "\n  language     = {" + str(info_language) + "},"\
             + "\n  extra        = {" + str(info_submitter) + "},"\
             + "\n}\n\n"
    return bibtex




def build_internet_bibtex(
        info_type, 
        info_idno, 
        info_author,
        info_title,
        info_journaltitle, 
        info_year, 
        info_volume,
        info_issue,
        info_series,
        info_series_number,
        info_mediatype, 
        info_abstract,
        info_url,
        info_submitter,
        info_isbn,
        info_issn,
        info_articlepages,
        info_language
        ): 
    bibtex = "@" + str(info_type) + "{" + str(info_idno) + ","\
             + "\n  author       = {" + str(info_author) + "},"\
             + "\n  title        = {" + str(info_title) + "},"\
             + "\n  journal      = {" + str(info_journaltitle) + "},"\
             + "\n  volume       = {" + str(info_volume) + "},"\
             + "\n  issue        = {" + str(info_issue) + "},"\
             + "\n  year         = {" + str(info_year) + "},"\
             + "\n  series       = {" + str(info_series) + "},"\
             + "\n  number       = {" + str(info_series_number) + "},"\
             + "\n  abstract     = {" + str(info_mediatype) + " | " + str(info_abstract) + "},"\
             + "\n  url          = {" + str(info_url) + "},"\
             + "\n  pages        = {" + str(info_articlepages) + "},"\
             + "\n  language     = {" + str(info_language) + "},"\
             + "\n  isbn         = {" + str(info_isbn) + "},"\
             + "\n  issn         = {" + str(info_issn) + "},"\
             + "\n  extra        = {" + str(info_submitter) + "},"\
             + "\n}\n\n"
    return bibtex



def build_dataset_bibtex(
        info_type, 
        info_idno, 
        info_author,
        info_title,
        info_place,
        info_publisher,
        info_year, 
        info_series,
        info_series_number,
        info_abstract,
        info_url,
        info_submitter,
        info_isbn,
        info_issn,
        info_language
        ):
    bibtex = "@" + str(info_type) + "{" + str(info_idno) + ","\
             + "\n  author       = {" + str(info_author) + "},"\
             + "\n  title        = {" + str(info_title) + "},"\
             + "\n  address      = {" + str(info_place) + "},"\
             + "\n  publisher    = {" + str(info_publisher) + "},"\
             + "\n  year         = {" + str(info_year) + "},"\
             + "\n  series       = {" + str(info_series) + "},"\
             + "\n  number       = {" + str(info_series_number) + "},"\
             + "\n  abstract     = {" + str(info_abstract) + "},"\
             + "\n  url          = {" + str(info_url) + "},"\
             + "\n  language     = {" + str(info_language) + "},"\
             + "\n  isbn         = {" + str(info_isbn) + "},"\
             + "\n  issn         = {" + str(info_issn) + "},"\
             + "\n  extra        = {" + str(info_submitter) + "},"\
             + "\n}\n\n"
    return bibtex



# === Get the information for different types of items ===

def create_book_bibtex(idno, itemdata):
    info_type = "book"
    info_author = get_authorinfo(itemdata["authors"])
    info_title = get_titleinfo(itemdata["title-book"])
    info_year = get_info_year(itemdata["date"])
    info_place = get_info_place(itemdata["publication-place"])
    info_publisher = get_info_publisher(itemdata["publisher"])
    info_series = get_info_series(itemdata["series"])
    info_series_number = get_info_series_number(itemdata["series-number"])
    info_abstract = get_info_abstract(itemdata["summary"])
    info_url = get_info_url(itemdata["url"])
    info_submitter = get_info_submitter(itemdata["submitter"])
    info_isbn = get_info_isbn(itemdata["isbn"])
    info_bookpages = get_info_bookpages(itemdata["pages"])
    info_idno = build_info_idno(idno, info_author, info_title, info_year)
    info_language = get_info_language(info_title)
    bibtex = build_book_bibtex(
        info_type, 
        info_idno, 
        info_author, 
        info_title, 
        info_year, 
        info_place,
        info_publisher,
        info_series,
        info_series_number,
        info_abstract,
        info_url,
        info_submitter,
        info_bookpages,
        info_isbn,
        info_language
        )
    return bibtex


def create_article_bibtex(idno, itemdata):
    info_type = "article"
    info_author = get_authorinfo(itemdata["authors"])
    info_title = get_titleinfo(itemdata["title-chapter-article"])
    info_journaltitle = get_journaltitleinfo(itemdata["journal-title"])
    info_year = get_info_year(itemdata["date"])
    info_abstract = get_info_abstract(itemdata["summary"])
    info_url = get_info_url(itemdata["url"])
    info_submitter = get_info_submitter(itemdata["submitter"])
    info_articlepages = get_info_articlepages(itemdata["pages"])
    info_volume = get_info_volume(itemdata["volume"])
    info_issue = get_info_issue(itemdata["issue"])
    info_idno = build_info_idno(idno, info_author, info_title, info_year)
    info_language = get_info_language(info_title)
    bibtex = build_article_bibtex(
        info_type, 
        info_idno, 
        info_author, 
        info_title, 
        info_journaltitle, 
        info_volume, 
        info_issue, 
        info_articlepages, 
        info_year, 
        info_abstract,
        info_url,
        info_submitter,
        info_language
        )
    return bibtex


def create_chapter_bibtex(idno, itemdata):
    info_type = "incollection"
    info_author = get_authorinfo(itemdata["authors"])
    info_editor = get_editorinfo_chapter(itemdata["editors"])
    info_chaptertitle = get_titleinfo(itemdata["title-chapter-article"])
    info_booktitle = get_titleinfo(itemdata["title-book"])
    info_year = get_info_year(itemdata["date"])
    info_place = get_info_place(itemdata["publication-place"])
    info_publisher = get_info_publisher(itemdata["publisher"])
    info_series = get_info_series(itemdata["series"])
    info_series_number = get_info_series_number(itemdata["series-number"])
    info_abstract = get_info_abstract(itemdata["summary"])
    info_url = get_info_url(itemdata["url"])
    info_submitter = get_info_submitter(itemdata["submitter"])
    info_isbn = get_info_isbn(itemdata["isbn"])
    info_bookpages = get_info_bookpages(itemdata["pages"])
    info_idno = build_info_idno(idno, info_author, info_chaptertitle, info_year)
    info_language = get_info_language(info_chaptertitle)
    bibtex = build_chapter_bibtex(
        info_type, 
        info_idno, 
        info_author, 
        info_editor,
        info_chaptertitle, 
        info_booktitle, 
        info_year, 
        info_place,
        info_publisher,
        info_series,
        info_series_number,
        info_abstract,
        info_url,
        info_submitter,
        info_bookpages,
        info_isbn,
        info_language
        )
    return bibtex


def create_editedvol_bibtex(idno, itemdata): 
    info_type = "book"
    info_editor = get_editorinfo_edvol(itemdata["authors"]) # Editors are listed as "authors" in CSV (!)
    info_booktitle = get_titleinfo(itemdata["title-book"]) 
    info_year = get_info_year(itemdata["date"])
    info_place = get_info_place(itemdata["publication-place"])
    info_publisher = get_info_publisher(itemdata["publisher"])
    info_series = get_info_series(itemdata["series"])
    info_series_number = get_info_series_number(itemdata["series-number"])
    info_abstract = get_info_abstract(itemdata["summary"])
    info_url = get_info_url(itemdata["url"])
    info_submitter = get_info_submitter(itemdata["submitter"])
    info_isbn = get_info_isbn(itemdata["isbn"])
    info_bookpages = get_info_bookpages(itemdata["pages"])
    info_idno = build_info_idno(idno, info_editor, info_booktitle, info_year)
    info_language = get_info_language(info_booktitle)
    bibtex = build_editedvol_bibtex(
        info_type, 
        info_idno, 
        info_editor,
        info_booktitle, 
        info_year, 
        info_place,
        info_publisher,
        info_series,
        info_series_number,
        info_abstract,
        info_url,
        info_submitter,
        info_bookpages,
        info_isbn,
        info_language
        )
    return bibtex



def create_thesis_bibtex(idno, itemdata): 
    info_type = "phdthesis"
    info_author = get_authorinfo(itemdata["authors"]) 
    info_booktitle = get_titleinfo(itemdata["title-thesis"]) 
    info_year = get_info_year(itemdata["date"])
    info_place = get_info_place(itemdata["publication-place"])
    info_university = get_info_publisher(itemdata["publisher"])
    info_series = get_info_series(itemdata["series"])
    info_series_number = get_info_series_number(itemdata["series-number"])
    info_abstract = get_info_abstract(itemdata["summary"])
    info_thesistype = get_info_thesistype(itemdata["thesis-type"])
    info_url = get_info_url(itemdata["url"])
    info_submitter = get_info_submitter(itemdata["submitter"])
    info_isbn = get_info_isbn(itemdata["isbn"])
    info_bookpages = get_info_bookpages(itemdata["pages"])
    info_idno = build_info_idno(idno, info_author, info_booktitle, info_year)
    info_language = get_info_language(info_booktitle)
    bibtex = build_thesis_bibtex(
        info_type, 
        info_idno, 
        info_author,
        info_booktitle, 
        info_year, 
        info_place,
        info_university,
        info_thesistype,
        info_series,
        info_series_number,
        info_abstract,
        info_url,
        info_submitter,
        info_bookpages,
        info_isbn,
        info_language
        )
    return bibtex


def create_internet_bibtex(idno, itemdata): 
    info_type = "article"
    info_author = get_authorinfo(itemdata["authors"]) 
    info_title = get_titleinfo(itemdata["title-internet"]) 
    info_journaltitle = get_journaltitleinfo(itemdata["journal-title"])
    info_year = get_info_year(itemdata["date"])
    info_volume = get_info_volume(itemdata["volume"])
    info_issue = get_info_issue(itemdata["issue"])
    info_series = get_info_series(itemdata["series"])
    info_series_number = get_info_series_number(itemdata["series-number"])
    info_mediatype = get_info_mediatype(itemdata["media-type"])
    info_abstract = get_info_abstract(itemdata["summary"])
    info_url = get_info_url(itemdata["url"])
    info_submitter = get_info_submitter(itemdata["submitter"])
    info_isbn = get_info_isbn(itemdata["isbn"])
    info_issn = get_info_issn(itemdata["issn"])
    info_articlepages = get_info_articlepages(itemdata["pages"])
    info_idno = build_info_idno(idno, info_author, info_title, info_year)
    info_language = get_info_language(info_title)
    bibtex = build_internet_bibtex(
        info_type, 
        info_idno, 
        info_author,
        info_title,
        info_journaltitle, 
        info_year, 
        info_volume,
        info_issue,
        info_series,
        info_series_number,
        info_mediatype, 
        info_abstract,
        info_url,
        info_submitter,
        info_isbn,
        info_issn,
        info_articlepages,
        info_language
        )
    return bibtex



def create_dataset_bibtex(idno, itemdata): 
    info_type = "dataset"
    info_author = get_authorinfo(itemdata["authors"]) 
    info_title = get_titleinfo(itemdata["title-book"]) 
    info_place = get_info_place(itemdata["publication-place"])
    info_publisher = get_info_publisher(itemdata["publisher"])
    info_series = get_info_series(itemdata["series"])
    info_series_number = get_info_series_number(itemdata["series-number"])
    info_year = get_info_year(itemdata["date"])
    info_abstract = get_info_abstract(itemdata["summary"])
    info_isbn = get_info_isbn(itemdata["isbn"])
    info_issn = get_info_issn(itemdata["issn"])
    info_url = get_info_url(itemdata["url"])
    info_submitter = get_info_submitter(itemdata["submitter"])
    info_language = get_info_language(info_title)
    info_idno = build_info_idno(idno, info_author, info_title, info_year)
    bibtex = build_dataset_bibtex(
        info_type, 
        info_idno, 
        info_author,
        info_title,
        info_place,
        info_publisher,
        info_year, 
        info_series,
        info_series_number,
        info_abstract,
        info_url,
        info_submitter,
        info_isbn,
        info_issn,
        info_language
        )
    return bibtex


# === Save BibTeX in the end ===

def save_bibtex(bibtex, bibtex_file): 
    with open(bibtex_file, "a", encoding="utf8") as outfile: 
        outfile.write(bibtex)


# === Main === 

def main(): 
    data = read_csv(csvfile)
    #print(data.head())
    print("Size of the dataset (rows, columns):", data.shape)
    #print(data.columns)
    counter = 0
    counter_book, counter_editedvol, counter_article, counter_chapter, counter_thesis, counter_internet, counter_dataset = 0,0,0,0,0,0,0
    for item in data.iterrows():
        if counter < 70000:
            info_idno = item[0]
            itemdata = item[1]
            if itemdata[0] == "1Livre":
                bibtex = create_book_bibtex(info_idno, itemdata)
                bibtex_file = "bibtex/bib18e-books.bib"
                save_bibtex(bibtex, bibtex_file)
                counter +=1
                counter_book +=1
            if itemdata[0] == "2Collectif":
                bibtex = create_editedvol_bibtex(info_idno, itemdata)
                bibtex_file = "bibtex/bib18e-editedvol.bib"
                save_bibtex(bibtex, bibtex_file)
                counter +=1
                counter_editedvol +=1
            elif itemdata[0] == "3Chapitre":
                bibtex = create_chapter_bibtex(info_idno, itemdata)
                bibtex_file = "bibtex/bib18e-chapters.bib"
                save_bibtex(bibtex, bibtex_file)
                counter +=1
                counter_chapter +=1
            elif itemdata[0] == "4Article":
                bibtex = create_article_bibtex(info_idno, itemdata)
                bibtex_file = "bibtex/bib18e-articles.bib"
                save_bibtex(bibtex, bibtex_file)
                counter +=1
                counter_article +=1
            elif itemdata[0] == "6Thèse":
                bibtex = create_thesis_bibtex(info_idno, itemdata)
                bibtex_file = "bibtex/bib18e-theses.bib"
                save_bibtex(bibtex, bibtex_file)
                counter +=1
                counter_thesis +=1
            elif itemdata[0] == "7Internet":
                bibtex = create_internet_bibtex(info_idno, itemdata)
                bibtex_file = "bibtex/bib18e-internet.bib"
                save_bibtex(bibtex, bibtex_file)
                counter +=1
                counter_internet +=1
            elif itemdata[0] == "8Cédérom":
                bibtex = create_dataset_bibtex(info_idno, itemdata)
                bibtex_file = "bibtex/bib18e-datasets.bib"
                save_bibtex(bibtex, bibtex_file)
                counter +=1
                counter_dataset +=1
        else: 
            pass
    print("\n", str(counter), "references have been processed in total.")
    print(str(counter_book), "books,",
          str(counter_thesis), "theses,",
          str(counter_editedvol), "edited volumes,",
          str(counter_article), "articles,",
          str(counter_chapter), "chapters,",
          str(counter_internet), "online articles,",
          str(counter_dataset), "datasets.")
main()