"""
later.
"""
from reddit_analysis.sub_reddit_models import SubRedditAnalyzer
from credentials.mongo_credentials import DB_COLLECTION


def main():
    # right now i am just testing.
    x = SubRedditAnalyzer(DB_COLLECTION)
    x.analyze_submission()


if __name__ == '__main__':
    main()
