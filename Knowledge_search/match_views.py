"""
reads fln csv data and matches page views
"""

import pandas as pd
import urllib
import re

def convert_title(title):
    """returns url formatted title based on display title"""
    try: 
        split_case = ' '.join([x.strip() for x in re.findall('[A-Z][^A-Z]*', title)])
        correct_case = split_case.lower()
        url_encoded = urllib.quote(correct_case, safe=' ')
        url_title = url_encoded.replace(" ", "_")
        return url_title
    except TypeError:
        # skip titles interpreted as dates or floats
        return " "

def check_index(title):
    return title in clean_views_df.index

def get_views(title):
    if title in clean_views_df.index:
        return clean_views_df.loc[title]['views'] 
    return 0

if __name__ == "__main__":
    # load data
    views_path = "/Users/mark/Desktop/temp_data/20160613_views.csv"
    views_df = pd.read_csv(views_path, encoding='utf-8', 
            usecols=['article', 'views'], index_col="article")

    fln_path = "/Users/mark/Desktop/temp_data/fln.csv"
    fln_df = pd.read_csv(fln_path, index_col=":START_ID(Article)", 
            usecols=[":START_ID(Article)"])

    # clean titles and duplicates in views data
    views_df['lower_title'] = views_df.index.str.lower()
    dd_views = pd.DataFrame(views_df.groupby(['lower_title'])['views'].transform('sum'))
    dd_views['lower_title'] = dd_views.index.str.lower()
    dd_views = dd_views.drop_duplicates(['lower_title'])
    dd_views.columns = ['views', 'lower_title']
    clean_views_df = dd_views.set_index(["lower_title"])

    # match page view data
    fln_df['lower_title'] = fln_df.index.map(convert_title)
    fln_df['views'] = fln_df['lower_title'].map(get_views)

    # save 
    fln_df['views'].to_csv("fln_views.csv", encoding='utf-8', index=True, header=True)

