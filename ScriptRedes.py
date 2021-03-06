from testcmd import TestsCmd
from getpass import getpass
import logging

logging.basicConfig()
paramiko_logger = logging.getLogger("paramiko.transport")
paramiko_logger.disabled = True

if __name__ == '__main__':
    user = input('Username: ')
    pswd = getpass(prompt='Password: ')
    enable_pswd = getpass(prompt='Enable password (dejar en blanco para usar la misma anterior): ')

    app = TestsCmd(user, pswd, enable_pswd)
    app.cmdloop()
