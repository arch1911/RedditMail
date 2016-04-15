import RedditMail
import praw


user_agent = "RedditMail"
r = praw.Reddit(user_agent=user_agent)


def get_posts(subreddits, posts, sort_by, wants_comments, self_text):
    """
    Get content from reddit formatted with bad html and return it as a giant string
    Args:
        subreddits (string list): subreddits to get content from
        posts (int): amount of posts to get
        sort_by (string): sort the content before pulling it
        wants_comments (boolean): if the user wants comments or not
        self_text (boolean): If the user wants self text to be included
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
            submissions = r.get_subreddit(subreddit).get_top_from_day(limit=posts)
        elif "new" == sort_by:
            submissions = r.get_subreddit(subreddit).get_new(limit=posts)
        elif 'top_all' == sort_by:
            submissions = r.get_subreddit(subreddit).get_top_from_all(limit=posts)
        else:
            submissions = r.get_subreddit(subreddit).get_top_from_day(limit=posts)
        content.append("<hl>"+subreddit+"</hl>\n")

        # go through the submissions in that subreddit (Currently limted)
        for submission in submissions:
            content.append("<b><h2>"+str(submission)+"</h2></b>\n")
            if self_text is True:
                content.append("<p>"+str(submission.selftext)+"</p>\n")
            submission.replace_more_comments(limit=2, threshold=10)
            if wants_comments is True:
                # go through the comments in the current submission
                for comment in r.get_submission(submission.permalink).comments:
                    content.append("<h3>"+str(comment.author)+"</h3>")  # h3h3
                    content.append("<p><h4> "+str(comment.body)+"</h4></p> ")
    content.append("</body></html>")
    for stuff in content:
        return_string += str(stuff) + "\n\n"
    return return_string
