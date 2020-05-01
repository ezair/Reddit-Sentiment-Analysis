"""
later.
"""
from reddit_analysis.sub_reddit_models import SubRedditAnalyzer
from credentials.mongo_credentials import DB_COLLECTION


def main():
    # This just a test example program currently.
    analyzer = SubRedditAnalyzer(DB_COLLECTION)
    hmft_anylsis_results = analyzer.analyze_subreddit('holdmyfeedingtube', sorting_type="top",
                                                      display_all_submission_results=True,
                                                      display_all_comment_results=True,
                                                      max_number_of_submissions_to_analyze=4)
    for key in hmft_anylsis_results:
        print("\nCleaner print out for a whole subreddit: ")
        print("{}: %{}".format(key, round(hmft_anylsis_results[key] * 100, 2)))
    

if __name__ == '__main__':
    main()
