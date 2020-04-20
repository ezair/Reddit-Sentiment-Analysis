"""
later.
"""
from reddit_analysis.sub_reddit_models import SubRedditAnalyzer
from credentials.mongo_credentials import DB_COLLECTION


def main():
    # This just a test example program currently.
    analyzer = SubRedditAnalyzer(DB_COLLECTION)
    db = DB_COLLECTION
    
    # Testing for a single submission.
    submission_record = db.find_one({'submission': 'ca8q81'})
    y = analyzer.analyze_submission('g3afb8', sorting_type="hot", display_all_comment_results=True)
    print("\nIn a cleaner way to show results:")
    for key in y:
        print("{}: %{}".format(key, round(y[key] * 100, 2)))
    
    # Testing for a whole subreddit.
    z = analyzer.analyze_subreddit('dankmemes', sorting_type="hot",
                                    display_all_comment_results=True)
    for key in z:
        print("\nCleaner print out for a whole subreddit: ")
        print("{}: %{}".format(key, round(z[key] * 100, 2)))
    

if __name__ == '__main__':
    main()
