###############################################
###                                         ###
###      ANNEXE INTERACTIVE VIRTUAL OS      ###
###         v 0.0.2 by Brett Martin         ###
###                                         ###
###############################################
import os
import AIOSENV as ae


# TODO: In C implementation, be sure to remove os modules
#os.system('cls||clear')
os.system('clear')
print(ae.HEADER)

# USER SELECT PROMPT
sel = input("LOAD EXISTING USER? (y/n): ")

if(sel == 'y'):
    usr = ae.User("admin", True) #TODO: Add user select functionality
else:
    usr = ae.User(input("Select username: "), True, "")

# CLEAR SCREEN AND DISPLAY THE HEADER TEXT
#os.system('cls||clear')
os.system('clear')
print(ae.HEADER)

# CREATE DEFAULT OS ENVIRONMENT
env = ae.Env(usr, True)

# CREATE DEFAULT FOLDERS FOR NEW ENVIRONMENT
for i in ae.DEFAULT_DIR:
    new_dir = ae.Folder(i, usr, env.root, False, False, True)
    env.root.contents.append(new_dir)
home = ae.Folder("home", usr, env.root, False, True, False)
env.root.contents.append(home)

# Used for current command
method = None

# START SHELL COMMAND LOOP
while(env.active):

    cmd = input("\033[91m{}@aios:\033[0m \033[33m{}$\033[0m ".format( env.usr.name, env.ret_wd() ))
    args = cmd.split()
    # print(args) # For testing purposes only

    try:
        method = getattr(env, args[0])
        if len(args) == 1:
            method()
        else:
            method(args[1:])
    except:
        print("\033[94mPlease enter a valid command\033[0m")
