import RedditMail
"""
Function to return a list that contains the emails login info.
The file should contain the following:
USERNAME:[USERNAME]
PASSWORD:[PASSWORD]

Replace the brackets with the correct info
Note: The function currently does not account for encrypted strings or ciphers like base64 so it's insecure.
"""


def getInfo():
    log_file = RedditMail.__log_file__  # Replace this with the file to open
    user_name = ''
    password = ''

    with open(log_file) as x:
        data = x.readlines()
    for x in data:
        d = x.split(":")
        if d[0] == "USERNAME":
            user_name = (d[1])
            user_name = user_name.strip()
        elif d[0] == "PASSWORD":
            password = str(d[1])
            password = password.strip()
    return user_name, password
