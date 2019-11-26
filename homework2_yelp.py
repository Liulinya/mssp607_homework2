import re
import pandas as pd
from pandas.io.json import json_normalize

# These methods are used to convert large JSON files into Pandas dataframes.
def fetch_yelp1(takeout_file):
    yelp = None
    with open(takeout_file) as in_file:
        raw = pd.read_json(in_file)
        businesses = raw["businesses"]
        yelp = json_normalize(businesses)
        print(yelp.shape)
        print(yelp.columns)
    return yelp

def fetch_yelp2(takeout_file):
    yelp = None
    with open(takeout_file) as in_file:
        raw = pd.read_json(in_file)
        reviews = raw["reviews"]
        yelp = json_normalize(reviews)
        print(yelp.shape)
        print(yelp.columns)
    return yelp

# This function takes as input a dataframe of Yelp businesses and a column name.
# For each star count 1.0-5.0 (unit: 0.5), it prints the percentage of restaurants receive that score on average
#
# This function does not return any values.        
def q1_yelp_means_by_stars(df, col):
    group_count = df.groupby(col).count()
    group_total = df.count().loc["name"]
    group_means = df.groupby(col).mean()
    for group in group_means.index.unique():
        count_stars = group_count.loc[group,"name"]
        print(f"{count_stars/group_total*100:.2f}% of restaurants receive the star {group}.")

# This function takes as input a dataframe of Yelp reviews and a column name.
# For each star count 1.0-5.0 (unit: 1.0), it prints the average word count of reviews that give each star count
#
# This function does not return any values.        
def q1_yelp_word_count(df, col):
    group_means = df.groupby(col).text.apply(lambda x: x.str.split().str.len().mean())
    count = 0
    for group in group_means:
        count += 1.0
        print(f"The average word count of reviews is {group:.2f} for the {count} star.")

# These following three functions take zip code as an input.
# It returns whether the zip code belongs to a specific region.
#
# Philadelphia ZIP codes begin with 19xxx, Pittsburgh ZIP codes begin 15xxx. The rest of Pennsylvania ZIP codes begin with 16, 17, or 18. 
def q2_check_philly_zip(code):
    code = str(code)
    zip_pattern = "19\d\d\d"
    zip_regex = re.compile(zip_pattern)
    zip_exists = re.search(zip_regex, code)
    return zip_exists
def q2_check_pitts_zip(code):
    code = str(code)
    zip_pattern = "15\d\d\d"
    zip_regex = re.compile(zip_pattern)
    zip_exists = re.search(zip_regex, code)
    return zip_exists
def q2_check_rest_zip(code):
    code = str(code)
    zip_pattern = "1[6,7,8]\d\d\d"
    zip_regex = re.compile(zip_pattern)
    zip_exists = re.search(zip_regex, code)
    return zip_exists

# This function should define a way to test whether a given review text is positive or negative, 
# using the tools from regular expressionso that we've learned up until this point.
def review_sentiment(review):
    positive_words = "(good|great|amazing|delicious|fabulous)"
    negative_words = "(bad|terrible|disgusting|gross|rude)"

    not_prefix = "[^(not)]\s"
    positive_pattern = re.compile(f"{not_prefix}{positive_words}")
    negative_pattern = re.compile(f"{not_prefix}{negative_words}")

    positive_mentions = re.findall(positive_pattern, review)
    negative_mentions = re.findall(negative_pattern, review)

    if len(positive_mentions) > len(negative_mentions):
        return "Positive"
    elif len(negative_mentions) > len(positive_mentions):
        return "Negative"
    else:
        return "Unknown"

# This function takes as input a dataframe of Yelp reviews and a column name.
# It prints the maximum value and their star indexes of each sentiment.
#
# This function does not return any values.
def q3_sentiment_count_by_stars(df, col):
    group_count_percent = df.groupby([col,'sentiment']).size().unstack().apply(lambda x: 100 * x / float(x.sum()))
    print(group_count_percent)
    
    max_negative_index = group_count_percent.idxmax(axis = 0)['Negative']
    max_negative_value = group_count_percent.loc[:, "Negative"].max()
    print(f"Review star {max_negative_index} has the highest number of negative reviews, which occupies {max_negative_value:.2f}% among star 1-5.")
   
    max_positive_index = group_count_percent.idxmax(axis = 0)['Positive']
    max_positive_value = group_count_percent.loc[:, "Positive"].max()
    print(f"Review star {max_positive_index} has the highest number of positive reviews, which occupies {max_positive_value:.2f}% among star 1-5.")
        
    max_unknown_index = group_count_percent.idxmax(axis = 0)['Unknown']
    max_unknown_value = group_count_percent.loc[:, "Unknown"].max()
    print(f"Review star {max_unknown_index} has the highest number of unknown reviews, which occupies {max_unknown_value:.2f}% among star 1-5.")

if __name__ == "__main__":
    takeout_filename1 = "Homework 2/PA_businesses.json"
    takeout_filename2 = "Homework 2/PA_reviews_full.json"
    takeout1 = fetch_yelp1(takeout_filename1)
    takeout2 = fetch_yelp2(takeout_filename2)

    # Get q1 averages for any given column of our dataframe
    q1_yelp_means_by_stars(takeout1, "stars")
    q1_yelp_word_count(takeout2, "stars")

    # Check q2's three regions as well as prints number of reviews and the mean score of reviews for each region
    test_strings = takeout1["postal_code"].dropna()
    philly_zip_count = 0
    philly_review_sum = 0
    pitts_zip_count = 0
    pitts_review_sum = 0
    rest_zip_count = 0
    rest_review_sum = 0
    for code in test_strings:
        philly = q2_check_philly_zip(code)
        pitts = q2_check_pitts_zip(code)
        rest = q2_check_rest_zip(code)
        if philly:
            philly_zip_count += 1
            philly_review_sum += takeout1["review_count"].sum()
        elif pitts:
            pitts_zip_count += 1
            pitts_review_sum += takeout1["review_count"].sum()
        elif rest:
            rest_zip_count += 1
            rest_review_sum += takeout1["review_count"].sum()
    try:
        print(f"Philly has {philly_review_sum} number of reviews and the mean score of reviews is {philly_review_sum/philly_zip_count}.")
    except ZeroDivisionError:
        print("Philly has none number of reviews and the mean score of reviews is zero.")
    print(f"Pitts has {pitts_review_sum} number of reviews and the mean score of reviews is {pitts_review_sum/pitts_zip_count}.")
    print(f"Rest of Pennsylvania has {rest_review_sum} number of reviews and the mean score of reviews is {rest_review_sum/rest_zip_count}.")

    # Simple automated definition yesterday in yelp_menu.py based on a pair of 
    # regexes, assigns "Positive", "Negative", or "Unknown"
    takeout2["sentiment"] = takeout2.loc[:, "text"].apply(review_sentiment)
    # Get q3 review sentiment for any given column of our dataframe
    q3_sentiment_count_by_stars(takeout2, "stars")