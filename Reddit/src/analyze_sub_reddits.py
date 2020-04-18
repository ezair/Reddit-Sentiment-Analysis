"""
later.
"""
from reddit_analysis.sub_reddit_models import SubRedditAnalyzer
from credentials.mongo_credentials import DB_COLLECTION

import nltk

def main():
    # right now i am just testing.
    x = SubRedditAnalyzer(DB_COLLECTION)
    db = DB_COLLECTION
    y = db.find_one({'submission': 'ca8q81'})
    # print(y)
    # records print out as dicts it appears.
    x.analyze_submission('g3afb8', sorting_type="hot")
    # x.analyze_submission('g3afb8', sorting_type="new")
    # x.analyze_submission('g3afb8', sorting_type="top")

if __name__ == '__main__':
    main()
