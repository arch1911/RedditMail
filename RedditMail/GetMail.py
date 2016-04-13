import RedditMail.SendMail
import imaplib
import re
from RedditMail.Login import getInfo
from RedditMail.GetPosts import get_posts


def run():
    IMAPServer = RedditMail.__imapserver__
    ''' Get the Emails login info from a file '''
    logIn_info = getInfo()
    mail = imaplib.IMAP4_SSL(IMAPServer)
    mail.login(logIn_info[0], logIn_info[1])
    comments = True
    number = 0
    subList = []
    sorting = ''
    try:
        mail.list()
        mail.select("inbox")  # connect to inbox.
        result, data = mail.search(None, "ALL")
        ids = data[0]  # data is a list.
        id_list = ids.split()  # ids is a space separated string
        for latest_email_id in id_list:
            result, data = mail.fetch(latest_email_id, "(RFC822)")  # fetch the email body (RFC822) for the given ID
            # Get sender's email
            resp, datan = mail.fetch(latest_email_id, '(BODY.PEEK[HEADER.FIELDS (From Subject)] RFC822.SIZE)')
            split = str(datan).split("<")
            toSend = split[1].split(">")
            print(str(toSend[0]))

            # Parse the HTML code for what I'm looking for.
            if 'Subject: RedditMail' in str(data):
                print("Latest email is RedditMail command, running program...")
                # get the number of posts, subreddits, and sorting
                if "_SRM_" in str(data):
                    commands = str(data).split("_SRM_")

                    # List the subreddits that were found
                    print(commands[1])

                    # Get the subreddits
                    if "subreddits: " in commands[1]:
                        # get everything between the brackets
                        x = re.search(r'subreddits(.*)end_subreddits', commands[1]).group(1)
                        print("Subreddits: ", x)
                        # Convert the string to a list of subreddits
                        subList = x.split()
                    else:
                        # defaults to Askreddit if there are no subreddits typed in
                        subList = "askreddit"

                    # set the sorting
                    if "sort by" in commands[1]:
                        x = re.search(r'sort(.*)end_sort', commands[1]).group(1)
                        print("Sorting by: ", x)
                        sorting = x
                    else:
                        sorting = "top"
                    # Set the number of posts to get
                    if "number " in commands[1]:
                        x = re.search(r'number(.*)end_number', commands[1]).group(1)
                        print("num posts: ", x)
                        number = x
                    else:
                        number = 5
                    # If the user doesn't want to view comments
                    if 'nocomments' in commands[1]:
                        comments = False
                # runs the getPosts function which returns the string to send then sends the mail
                n = get_posts(subList, int(number), sorting, comments)
                RedditMail.SendMail.send_mail(n, toSend[0])

            else:
                print("Email not a RedditMail command")
            # Try and delete the email
            mail.store(latest_email_id, '+FLAGS', '\\Deleted')
            mail.expunge()
    except:
        print("Inbox empty or another error")


def main():
    print("RedditMail ", str(RedditMail.__version__))
    print("")
    run()
    print("Done")
