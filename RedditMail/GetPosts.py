import RedditMail
import praw
"""
This function gets content from reddit
"""

user_agent = "RedditMail"
connection = praw.Reddit(user_agent=user_agent)


def get_posts(subreddits, posts, sort_by, comments):
    """
    Get content from reddit formatted with bad html and return it as a giant string
    Args:
        subreddits (string list): subreddits to get content from
        posts (int): amount of posts to get
        sort_by (string): sort the content before pulling it
        comments (boolean): if the user wants comments or not
    """
    content = []
    return_string = ""
    print(subreddits)
    content.append("RedditMail "+str(RedditMail.__version__)+"\n")
    content.append("<html>\n")
    content.append("<body>\n")
    # go through every subreddit the user wants
    for subreddit in subreddits:
        if "top" == sort_by:
            submissions = connection.get_subreddit(subreddit).get_top_from_day(limit=posts)
        elif "new" == sort_by:
            submissions = connection.get_subreddit(subreddit).get_new(limit=posts)
        elif 'top_all' == sort_by:
            submissions = connection.get_subreddit(subreddit).get_top_from_all(limit=posts)
        else:
            submissions = connection.get_subreddit(subreddit).get_top_from_day(limit=posts)
        content.append("<hl>"+subreddit+"</hl>\n")
        # go through the submissions in that subreddit (Currently limted)
        for submission in submissions:
            content.append("<b><h2>"+str(submission)+"</h2></b>\n")
            content.append("<p>"+str(submission.selftext)+"</p>\n")
            submission.replace_more_comments(limit=2, threshold=10)
            if comments:
                content_comments = praw.helpers.flatten_tree(submission.comments)
                # go through the comments in the current submission
                for comment in content_comments:
                    content.append("<h3>"+str(comment.author)+"</h3>")  # h3h3
                    content.append("<p><h4> "+str(comment.body)+"</h4></p> ")
    content.append("</body></html>")
    for stuff in content:
        return_string += str(stuff) + "\n\n"
    return return_string
