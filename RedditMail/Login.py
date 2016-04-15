import RedditMail


def get_info():
    """
    Gets E-mail username and password from the file defined at __log_file__ in __init__.py
    The file should contain the following:
    USERNAME:[USERNAME]
    PASSWORD:[PASSWORD]
    Do not include brackets or use spaces

    Note: The file must be stored as plaintext with no encryption making it insecure.
    :return:
    """
    log_file = RedditMail.__log_file__
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
