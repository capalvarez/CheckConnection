from testcmd import TestsCmd
from getpass import getpass


if __name__ == '__main__':
    user = input('Username: ')
    pswd = getpass(prompt='Password: ')

    app = TestsCmd(user, pswd)
    app.cmdloop()
