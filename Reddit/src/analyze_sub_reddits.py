"""
@Author Eric Zair
@File reddit_post_collector.py
@Description: This is a simple test program that is used to show off the
              power behind the SubredditAnalyzer object :)
"""
from reddit_analysis.comment_analysis import SubredditAnalyzer
from credentials.mongo_credentials import DB_COLLECTION


# Simple example of how to use the SubredditAnalyzer object for a subreddit.
def test_subreddit_call(analyzer):
   anylsis_results = analyzer.analyze_subreddit('battlestations', sorting_type='top',
                                                display_all_submission_results=True,
                                                display_all_comment_results=True,
                                                max_number_of_comments_to_analyze=10,
                                                max_number_of_submissions_to_analyze=10)


# Simple example of how to use the SubredditAnalyzer object for a submission.
def test_submission_call(analyzer):
    # Testing, testing, 1 2 3.
    test = analyzer.analyze_submission('ca8q81',
                                       sorting_type='top',
                                       display_all_comment_results=True,
                                       max_number_of_comments_to_analyze=0)


# Simple method to show how the analyzer method can be used in different ways.
def compare_subreddit_sorting_type_results(subreddit, number_of_comments=0,
                                           number_of_submissions=0):
    analyzer = SubredditAnalyzer(DB_COLLECTION)

    top_analysis_results = analyzer.analyze_subreddit(subreddit, sorting_type='top',
                                                      max_number_of_comments_to_analyze=\
                                                          number_of_comments,
                                                      max_number_of_submissions_to_analyze=\
                                                          number_of_submissions)
    top_analysis_results['sorting_type'] = 'top'

    new_analysis_results = analyzer.analyze_subreddit(subreddit, sorting_type='new',
                                                      max_number_of_comments_to_analyze=\
                                                          number_of_comments,
                                                      max_number_of_submissions_to_analyze=\
                                                          number_of_submissions)
    new_analysis_results['sorting_type'] = 'new'

    hot_analysis_results = analyzer.analyze_subreddit(subreddit, sorting_type='hot',
                                                      max_number_of_comments_to_analyze=\
                                                          number_of_comments,
                                                      max_number_of_submissions_to_analyze=\
                                                          number_of_submissions)
    hot_analysis_results['sorting_type'] = 'hot'

    all_results = [top_analysis_results, new_analysis_results, hot_analysis_results]

    most_positive_result = sorted(all_results, key=lambda k: k['positive'], reverse=True)[0]
    most_negative_result = sorted(all_results, key=lambda k: k['negative'], reverse=True)[0]

    print(f"\nTop analysis results: {top_analysis_results}")
    print(f"New analysis results: {new_analysis_results}")
    print(f"Hot analysis results: {hot_analysis_results}\n")

    print(f"The most positive result is \"{most_positive_result['sorting_type']}\" "
          f"with a score of {most_positive_result['positive']}")

    print(f"The most negative result is \"{most_negative_result['sorting_type']}\" "
          f"with a score of {most_negative_result['negative']}")


def main():
    reddit_analyzer = SubredditAnalyzer(DB_COLLECTION)

    # test_subreddit_call(reddit_analyzer)
    # test_submission_call(reddit_analyzer)

    # Let's compare some results from a very positive reviewed subreddit.
    # compare_subreddit_sorting_type_results('battlestations', number_of_comments=10,
    #                                        number_of_submissions=10)

    # Now, let's comare results on a much more negative subreddit.
    # NOTICE: The results are MUCH higher for negativity and MUCH lower for positivity.
    # compare_subreddit_sorting_type_results('holdmyfeedingtube', number_of_comments=10,
    #                                        number_of_submissions=10)


if __name__ == '__main__':
    main()
