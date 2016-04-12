
'''
    Returns the Reddit content via email
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
__author__ = 'Luke Zambella'

import praw
import smtplib
from email.mime.text import MIMEText
import sys
from RedditMail.GetMail import getInfo


import praw
import smtplib
from email.mime.text import MIMEText
import sys


VERSION = 3.0
user_agent = "RedditMail"
connection = praw.Reddit(user_agent=user_agent)

# I can't find a way to differentiate child comments from parents
class redditMail():

    # send the mail
    def sendMail(list, receiver): # def sendMail(content, receiver)
        logIn = getInfo()
        with open("[LOGIN FILE]") as x:
            data = x.readlines()
            for x in data:
                d = x.split(":")
            if d[0] == "USERNAME":
                userName = (d[1])
                userName = userName.strip()
            elif d[0] == "PASSWORD":
                password = str(d[1])
                password = password.strip()
        userName = "redditmail058@gmail.com"
        msg = MIMEText(list, 'html')
        msg['Subject'] = "Reddit"
        msg['From'] = "[MAIL NAME]"
        msg['To'] = receiver # Get the sent email

        mail = smtplib.SMTP("smtp.gmail.com","587") ### SMTB server, change this to match yours
        mail.ehlo()
        mail.starttls()
        mail.login(userName, password)

        print("Attempting to send email...")
        mail.sendmail(userName, receiver, msg.as_string())
        mail.close()
        print("Email sent")
        return True

    def getPosts(subreddits, posts, sort_by):
        content = []
        toString = ""
        print(subreddits)
        content.append("RedditMail "+str(VERSION)+"\n")
        content.append("<html>\n")
        content.append("<body>\n")
        # go through every subreddit the user wants
        for subreddit in subreddits:
            if "top" in sort_by:
                submissions = connection.get_subreddit(subreddit).get_top_from_day(limit=posts)
            elif "new" in sort_by:
                submissions = connection.get_subreddit(subreddit).get_new(limit=posts)
            content.append("<hl>"+subreddit+"</hl>\n")
            # go through the submissions in that subreddit (Currently limted)
            for submission in submissions:
                content.append("<b><h2>"+str(submission)+"</h2></b>\n")
                content.append("<p>"+str(submission.selftext)+"</p>\n")
                submission.replace_more_comments(limit=2, threshold=10)
                comments = praw.helpers.flatten_tree(submission.comments)
                # go through the comments in the current submission
                for x in comments:
                    content.append("<h3>"+str(x.author)+"</h3>")
                    content.append("<p><h4> "+str(x.body)+"</h4></p>")
        content.append("</body></html>")
        for stuff in content:
            toString += str(stuff) + "\n\n"
        return toString
