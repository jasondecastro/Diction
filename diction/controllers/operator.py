#-------------------------------------------------------------------------------
# Name:        diction
# Purpose:     operating system emulator/linux-like environment
#
# Author:      Jason Decastro
#
# Created:     07/08/2013
# Copyright:   (c) Diction 2013
# Licence:     GNU/Diction
#-------------------------------------------------------------------------------

#MODULES NECESSARY
import getpass, time, subprocess, sqlite3, datetime

#DATABASE CONNECTION
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users
                  (username text, password text, last_login text)""")

#SYSTEM VARIABLES
OS_NAME = "Diction"
OS_VER = "1.02" #change to int later
DOC_URL = "http://help.diction.com" #once diction.com is actually bought

#COPYLEFT NOTICE
copyleft = '''The programs included with the Diction system are free software;
Diction comes with ABSOLUTELY NO WARRANTY.'''

#--------------------------------LOGIN STUFF------------------------------------

users = dict()
last_login = list()

class Login():
    #PROMPT THE OPERATOR TO LOGIN
    def login(self):
        self.usr = input("usr> ")
        self.pwd = getpass.getpass("pwd> ")
        users.update({'user':self.usr, 'password':self.pwd})
        self.check_login()

    #TEST THE LOGIN DETAILS INPUTTED BY THE OPERATOR
    def check_login(self):
        if len(self.usr) and len(self.pwd) > 0:
            cursor.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (self.usr, self.pwd))
            data = cursor.fetchone()

            if data is None:
                time.sleep(1)
                print("-" * 20)
                self.login()
            else:
                timer = datetime.datetime.now()
                time_at_login = str(timer.strftime("%Y-%m-%d %H:%M"))
                cursor.execute("UPDATE users SET last_login = '%s' WHERE username = '%s'" % (time_at_login, self.usr))
                conn.commit()
                time.sleep(2)
                obj = Welcome()
                obj.welcome()

#----------------------------INSIDE DICTION-------------------------------------

class Welcome(Login):
    #THIS IS THE WELCOME MESSAGE. INSIDE OF IT IS THE COPYLEFT NOTICE.
    def welcome(self):
        cursor.execute("SELECT last_login FROM users WHERE username = '"+ users['user'] +"'")
        data = cursor.fetchone()
        print()
        print("Last login: %s" % data) #PUT DATA THERE <
        print("Welcome to %s %s (GNU/Diction)\n" % (OS_NAME, OS_VER))
        print(" * Documentation:  %s\n" % DOC_URL)
        print('71 updates are available.')
        print()
        print(copyleft)
        print()

        obj = Kernel()
        obj.kernel(Kernel.help_info, Kernel.commands, Kernel.create_commands)


#figured user operations could fit in this box
class Users(Login):
    def create_user(self):
        print()
        new_usr = input("new usr>")
        new_pwd = getpass.getpass("new pwd>")
        new_pwd2 = getpass.getpass("re-check new pwd>")

        if new_pwd == new_pwd2:
            cursor.execute("INSERT INTO 'users' (username, password) VALUES ('%s', '%s')" % (new_usr, new_pwd))
            conn.commit()

            cursor.execute("SELECT * FROM 'users' WHERE username = '%s' AND password = '%s'" % (new_usr, new_pwd))
            new_acc = cursor.fetchone()

            if new_acc is None:
                print()
                print("Failure!")
                krnl_obj = Kernel()
                krnl_obj.kernel(Kernel.help_info, Kernel.commands, Kernel.create_commands)

            else:
                print()
                print("User account '%s' successfully created." % new_usr)
                krnl_obj = Kernel()
                krnl_obj.kernel(Kernel.help_info, Kernel.commands, Kernel.create_commands)

#-----------------------REALLY COMPLICATED AND LONG KERNEL CODE-----------------
class Kernel(Login):
    #LIST OF COMMANDS:
    commands = ['help', 'create', 'logout']
    create_commands = ['user']
    help_info = '''
Diction 1.02 is an operating system emulator for educational purposes.
Below is a list of commands you are currently able to use:

    ---help (which is this one)
    ---create (allows you to create a new account)
    ---logout (allows you to logout of the current account)

    '''


    #THIS IS WHERE THE OPERATOR CAN ENTER STUFF AND SHIT.
    def kernel(self, help_info, commands, create_commands):
        obj = Login()


        kernel_input = None

        while kernel_input is not commands[0] or commands[1]:
            kernel_input = input(users['user'] + "@" + OS_NAME.lower() + ">")

            #long operation ahead!
            if kernel_input == commands[0]:
                print(help_info)
                kernel_input
            elif kernel_input == commands[1]:
                print("Create: user")
                create_input = input("create>")
                if create_input == create_commands[0]:
                    usr_obj = Users()
                    usr_obj.create_user()
                else:
                    kernel_input
            elif kernel_input == commands[2]:
                logout_obj = Logout()
                logout_obj.logout()
            else:
                kernel_input
#---------------------------------LOGOUT STUFF----------------------------------

class Logout(Login):
    #logging out!
    def logout(self):
        print()
        print("-" * 40)
        print()
        main()

#----------------------CALL EVERYTHING ABOVE------------------------------------

#THIS FUNCTION IS WHERE I CAN CHANGE THINGS ON HOW THE PROGRAM STARTS AND SUCH.
def main():
    obj = Login()
    obj.login()

#WE ARE NOW GOING TO CALL THE FUNCTION ABOVE IF THIS PROGRAM IS BEING RAN.
if __name__ == '__main__':
    main()