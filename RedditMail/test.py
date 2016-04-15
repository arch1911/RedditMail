'''
test scripts
'''

import RedditMail
import praw

import re
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
            try:
                content.append("<b><h2>"+str(submission)+"</h2></b>\n")
                if self_text is True:
                    content.append("<p>"+str(submission.selftext)+"</p>\n")
                submission.replace_more_comments(limit=2, threshold=10)
                if wants_comments is True:
                    # go through the comments in the current submission
                    for comment in r.get_submission(submission.permalink).comments:
                        try:
                            content.append("<h3>"+str(comment.author)+"</h3>")  # h3h3
                            content.append("<p><h4> "+str(comment.body)+"</h4></p> ")
                        except AttributeError:
                            pass
            except Exception:
                print(Exception)
    content.append("</body></html>")
    for stuff in content:
        return_string += str(stuff) + "\n\n"
    return return_string


# TODO:
"""
syntax
!redditmail !subreddits:-subreddit1,subreddit2,subreddit3,...- !nocomments !noselftext !numcomments:-num- !numsubmissions:-num- !sortby:-sorting- !redditmail
"""


def test(data):
    comments = True
    self_text = True
    if "!redditmail" in str(data):
        commands = str(data).split("!redditmail")
        print(commands[1])
        # Get the subreddits
        if "!subreddits" in commands[1]:
            # get everything between the brackets
            x = re.search(r'!subreddits-(.*)-', commands[1]).group(1)
            print("Subreddits: ", x)
            # Convert the string to a list of subreddits
            sub_list = x.split(',')[:5]
        else:
            # defaults to Askreddit
            sub_list = "askreddit"
        # set the sorting
        if "!sortby" in commands[1]:
            x = re.search(r'!sortby:-(.*)-', commands[1]).group(1)
            print("Sorting by: ", x)
            sorting = x
        else:
            sorting = "top"
        # Set the number of posts to get
        if "!numposts" in commands[1]:
            x = re.search(r'!numposts-(.*)-', commands[1]).group(1)
            print("num posts: ", x)
            number = x
        else:
            number = 5
        # If the user doesn't want to view comments
        if '!nocomments' in commands[1]:
            comments = False
        if '!noselftext' in commands[1]:
            self_text = False
        if '!numcomments' in commands[1]:
            x = re.search(r'!numcomments(.*)-', commands[1]).group(1)
            print("num comments: ", x)
            number = x
        return get_posts(sub_list, int(number), sorting, comments, self_text)  # number


def __main__():
    submission = get_posts(['runescape'], 2, 'top', True, True)
    print(submission)


def __console__():
    command = ''
    while command is not 'STOP':
        print("Enter command: ")
        command = input(command)
        print(command)
        print(test(command))

__console__()
