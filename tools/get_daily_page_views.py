"""
combines hourly page views into a single csv on S3
"""

import pandas as pd
import urllib
import datetime
import csv

def build_df(year, month, day, hour):
    """
    returns a pandas dataframe with columns:
        project, article, views, content_returned
    based on input date string:
        e.g, "2016", "06", "24", "01"
    files are found at
            https://dumps.wikimedia.org/other/pagecounts-all-sites/2016/2016-05/pagecounts-20160501-000000.gz
    """
    base_url_string = "https://dumps.wikimedia.org/other/pagecounts-all-sites/"
    url_string = base_url_string + "/" + year + "/" + year + "-" + month
    url_string += "/pagecounts-" + year + month + day + "-" + hour + "0000.gz"
    
    file_name = year + month + day + "-" + hour + ".gz"
    
    # download file
    opener = urllib.URLopener()    
    opener.retrieve(url_string, file_name)
    
    # return data frame
    df = pd.read_csv(file_name, compression="gzip", sep=" ", quoting=csv.QUOTE_NONE,
                 error_bad_lines=False, header=None)
    df.columns = ['project', 'article', 'views', 'content_returned']
    # include only en-wiki
    df = df[df['project'] == 'en']
    df = df[['article', 'views']]
    
    return df

def combine_dataframes(df1, df2):
    """
    sums the page views in the given dataframes
        uses an outer join (treating nan as 0)
    returns a new dataframe
        'article', 'views'
    """
    df_combined = df1.merge(df2, left_on='article', right_on='article', how='outer')
    df_combined.fillna(0, inplace=True)
    df_combined['views'] = df_combined['views_x'] + df_combined['views_y']
    df_combined = df_combined[['article', 'views']]
    df_combined = df_combined.drop_duplicates('article')
    
    return df_combined

if __name__ == "__main__":
    # get today's date
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month).zfill(2)
    day = str(now.day - 1).zfill(2)

    # write first data frame to a file
    df1 =  build_df(year, month, day, "00")
    df1.to_csv(year + month + day + "_views.csv")

    hours = [str(h).zfill(2) for h in range(24)]

    for hour1, hour2 in zip(hours[1::2], hours[2::2]):
        print hour2
        df1 = build_df(year, month, day, hour1)
        df2 = build_df(year, month, day, hour2)
        df1_df2 = combine_dataframes(df1, df2)

        # combine with existing views 
        df_existing = pd.read_csv(year + month + day + "_views.csv")
        df_combined = combine_dataframes(df1_df2, df_existing)

        df_combined.to_csv(year + month + day + "_views.csv")

# TODO:
    # clean directory
    # transfer to s3
