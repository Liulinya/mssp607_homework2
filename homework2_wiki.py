# run "pip install cssselect" in bash line
from lxml import html
from wiki_api import page_text
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import requests
import re
import json
import lxml.html
import pandas as pd

# scrape the contents of the list of featured articles
# and return a list of names for all featured articles that are also biographies
def get_featured_biographies():
    bio_article = []
    boolean = False
    for article_name in ls:
        if ('[edit]' in article_name) and ('biographies' in article_name) or ('Biographies' in article_name):
            boolean = True
            continue
        elif ('[edit]' in article_name) and ('autobiographies' in article_name) or ('Autobiographies' in article_name):
            boolean = False
            continue
        elif ('[edit]' in article_name) and ('biographies' not in article_name):
            boolean = False
        
        if boolean:
                bio_article += [article_name]
        else:
            continue
    return bio_article


# scrape all of the individual pages for featured article biography titles in the list created in part 1
# and extract the first paragraph of each biography
def get_first_paragraph(name_list):
    # \d is any number character, 0-9
    # \w is any alphabetical character, A-Z, uppercase or lowercase
    # \s is any space character, including tabs or spaces or other blanks.
    first_paragraph = []
    for name in name_list:
        page = page_text(name, "list")
        life_span_pattern = name + '\s*\('
        for paragraph in page:
            match = re.search(life_span_pattern, paragraph)
            if match:
                first_paragraph.append(paragraph)
                break
    return first_paragraph

# determine the most common gender of pronouns in a given string of any length
def get_pronouns(text_list):
    gender_list = []
    for text in text_list:
        text = "".join(text)
        text.replace("\\u",'') #clean up
        text.replace("\n",'') 
        male = text.count(' he ') + text.count(' He ') + text.count(' his ') + text.count(' His ') + text.count(' him ') + text.count(' Him ')
        female = text.count(' she ') + text.count(' She ') + text.count(' her ') + text.count(' Her ') + text.count(' hers ') + text.count(' Hers ')
        plural = text.count(' they ') + text.count(' They ') + text.count(' them ') + text.count(' Them ') + text.count(' their ') + text.count(' Their ')

        if male > (female or plural): 
            gender_list.append("Male")
        if female > (male or plural): 
            gender_list.append("Female")
        if plural > (male or female): 
            gender_list.append("Plural")
    return gender_list


def additional_analysis():
    pass

def export_dataset(df, format):
    with open(f"export_dataset.{format}", "w", encoding='utf-8') as out_file:  # have the option to export in csv or json format
        # encoding = 'utf-8' because run into error of UnicodeEncodeError: 'gbk' codec can't encode character '\xa0' in position
        if format == "csv":
            out_file.write(df.to_csv())
        elif format == "json":
            out_file.write(df.to_json())

if __name__ == "__main__":
    ls = page_text("Wikipedia:Featured articles", "list")
    ls = ls[40:]
    ls = ls[:-7]
    ls = list(filter(lambda x: x != "",ls))

    name_list=get_featured_biographies()
    print(f"Among {len(ls)} number of featured articles, {len(name_list)/len(ls)*100:.2f}% are biographies.")
    first_para_list = get_first_paragraph(name_list)
    print(f"Among {len(name_list)} number of biographies, {len(first_para_list)/len(name_list)*100:.2f}% can be scraped as first paragraphs.")

    gender_list = get_pronouns(first_para_list)
    female_count = sum(gender == 'Female' for gender in gender_list)
    male_count = sum(gender == 'Male' for gender in gender_list)
    plural_count = sum(gender == 'Plural' for gender in gender_list)
    total_count = int(len(first_para_list))
    other_count = total_count - female_count - male_count - plural_count
    print(f"Among {total_count} number of first paragraphs, {female_count/total_count*100:.2f}% of biographies use she/her;\n{male_count/total_count*100:.2f}% of biographies use he/his;\n{plural_count/total_count*100:.2f}% of biographies use they/them;\n{other_count/total_count*100:.2f}% of biographies fail to parse, or have unclear gender.")
    #export_dataset(df, "csv")

