"""
later.
"""
from reddit_analysis.comment_analysis import SubRedditAnalyzer
from credentials.mongo_credentials import DB_COLLECTION


def test_subreddit_call(analyzer):
    hmft_anylsis_results = analyzer.analyze_subreddit('amitheasshole',
                                                      display_all_submission_results=True,
                                                      display_all_comment_results=True,
                                                      max_number_of_submissions_to_analyze=0,
                                                      max_number_of_comments_to_analyze=0)


def test_submission_call(analyzer):
    # Testing, testing, 1 2 3.
    test = analyzer.analyze_submission('ca8q81',
                                       sorting_type='top',
                                       display_all_comment_results=True,
                                       max_number_of_comments_to_analyze=0)


def main():
    # This just a test example program currently.
    reddit_analyzer = SubRedditAnalyzer(DB_COLLECTION)

    test_subreddit_call(reddit_analyzer)
    #test_submission_call(reddit_analyzer)    

if __name__ == '__main__':
    main()
