__author__ = 'Luke Zambella'

'''
Function to return a list that contains the emails login info.
The file should contain the following:
USERNAME:[USERNAME]
PASSWORD:[PASSWORD]

Replace the brackets with the correct info
Note: The function currently does not account for encrypted strings or ciphers like base64 so it's insecure.
'''


def getInfo():
    logFile = ''  # Replace this with the file to open
    userName = ''
    password = ''

    with open(logFile) as x:
        data = x.readlines()
    for x in data:
        d = x.split(":")
        if d[0] == "USERNAME":
            userName = (d[1])
            userName = userName.strip()
        elif d[0] == "PASSWORD":
            password = str(d[1])
            password = password.strip()
    return {userName, password}
