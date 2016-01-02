# RedditMail
An even more obscure way to browse (text based) subreddits on Reddit. 
## What it does
The program should run on a server (or a personal computer) and have its own email address to monitor.
The user should send an email from any of their (work email not recommended) email addresses to the address the program is monitoring.
The program parses the email and uses PRAW to get the content the user specified
## How to use
  1. Have an email (gmail preferred) account set up for the program
  2. Set up the login credentials in both the scripts
  3. Run the program
  4. Send an email to the account set up in section 1 with the subject "RedditMail", the body should be in this format: "_SRM_     [subreddit1] [subreddit2]..."
  5. The program should send an email back containing the title of each of the posts, the selftext (if there is any), and a bunch of     comments (better formatting to be added)
