#-------------------------------------------------------------------------------
# Name:        os_emulator
# Purpose:
#
# Author:      Jason Decastro
#
# Created:     07/09/2013
# Copyright:   (c) Jason Decastro 2013
# Licence:     GNU/Diction 3.0.0-12-generic i686
#-------------------------------------------------------------------------------

'''

A login.
A shell system.
A explorer system (If done well enough, you can disable your own explorer process at startup and execute your own.)
A desktop window.
A web browser. (A project in and of itself.)
A plain text editor. (Another individual project.)
A control panel/system configuration set of utilities.

'''

import getpass, time, subprocess

class User:
    users = {'admin' : 'admin'}
    OS_NAME = "Diction"
    OS_VER = 1.02
    DOC_URL = "http://help.diction.com"

    def login(self):
        self.usr = input("usr> ")
        self.pwd = getpass.getpass("pwd> ")
        self.check_login()

    def check_login(self):
        if len(self.usr) and len(self.pwd) > 0:
            try:
                if self.pwd in User.users[self.usr]:
                    time.sleep(2)
                    self.welcome()
            except KeyError:
                time.sleep(1)
                print("-" * 20)
                self.login()
    def welcome(self):
        print()
        print("Last login: ")
        print("Welcome to %s %f (GNU/Diction 3.0.0-12-generic i686)" % (self.OS_NAME, self.OS_VER))
        print()
        print(" * Documentation:  %s" % self.DOC_URL)
        print()
        print("278 packages can be updated.")
        print("71 updates are security updates.")
        print()
        print()
        print()
        print("The programs included with the %s system are free software;" % self.OS_NAME)
        print("the exact distribution terms for each program are described in the")
        print("individual files in /usr/share/doc/*/copyright.")
        print()
        print("%s comes with ABSOLUTELY NO WARRANTY, to the extent permitted by" % self.OS_NAME)
        print("applicable law.")
        print()
        self.menu()

    def menu(self):
        kernel_input = input(self.usr + "@" + self.OS_NAME.lower() + ":")
        if 'task' in kernel_input:
            cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            for processes in proc.stdout:
                print(processes)

def main():
    user = User()
    user.login()

if __name__ == '__main__':
    main()