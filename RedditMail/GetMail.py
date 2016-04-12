__author__ = "Luke Zambella"
import RedditMail.SendMail
import imaplib
import re
from RedditMail.Login import getInfo
'''
    Copyright (C) 2015 Luke Zambella

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

STATUS = False
VERSION = 3.0


def run():
    # Change these so that it gets it from a file instead
    userName = ""
    password = ""
    IMAPServer = "imap.gmail.com" # Change this to match your email's imap server

    ''' Get the Emails login info from a file '''
    logIn_info = getInfo()
    mail = imaplib.IMAP4_SSL(IMAPServer)
    mail.login(userName, password)
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
                    print(commands[1]) # List the subreddits that were found

                    # Get the subreddits
                    if "subreddits: " in commands[1]:
                        x = re.search(r'subreddits(.*)end_subreddits', commands[1]).group(1)  # get everything between the brackets
                        print("Subreddits: ", x)
                        subList = x.split()       # Convert the string to a list of subreddits separated by a space
                    else:
                        subList = "askreddit" # defaults to Askreddit if there are no subreddits typed in

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
                # if no input was in the body the default email would contain 5 of the top askreddit threads (personal choice)

                # runs the getPosts function which returns the string to send then sends the mail
                n = RedditMail.SendMail.redditMail.getPosts(subList, int(number), sorting)
                RedditMail.SendMail.redditMail.sendMail(n, toSend[0])

            else:
                print("Email not a RedditMail command")
            # Try and delete the email
            mail.store(latest_email_id, '+FLAGS', '\\Deleted')
            mail.expunge()
    except:
        print("Inbox empty or another error")


def main():
    print("RedditMail ", str(VERSION))
    print("")
    STATUS = True
    run()
    print("Done")

if __name__ == "__main__":
    main()
