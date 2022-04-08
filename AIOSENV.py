import os
import manuals

HEADER = '\x1b[6;30;42m' + "          Welcome to AIOS Alpha v0.0.2         " + '\x1b[0m\n'
FILENAME_RESTRICTIONS = ['/', '\\', '?', '%', '*', ':', '|', '"', '\'', '<', '>', '.']
DEFAULT_DIR = ["bin", "boot", "cdrom", "dev", "etc", "lib", "media", "mnt", "opt", "proc", "root", "run", "sbin", "srv", "sys", "tmp", "usr", "var"]

class User:

    def __init__(self, name, admin=False, password=None):
        self.name = name
        self.admin = admin
        self.password = password

class Folder:

    def __init__(self, name, owner, parent, root, home, removable):
        self.name = name
        self.owner = owner
        self.parent = parent
        self.root = root
        self.home = home
        self.contents = []
        self.removable = removable


class File:

    def __init__(self, name, owner, parent, removable, executable, write):
        self.name = name
        self.owner = owner
        self.parent = parent
        self.removable = removable
        self.executable = executable
        self.write = write
        self.contents = "print(\"Hello World!\")"
        self.perm_str = "-r--"


class Env:

    def __init__(self, usr, admin):
        self.usr = usr
        self.users = [usr]
        self.root = Folder("/", usr, None, True, False, False)
        self.cwd = self.root
        self.admin = admin
        self.active = True

    def clear(self):
        #os.system('cls||clear')
        os.system('clear')
        print(HEADER)

    def pwd(self):
        cwd_str = self.cwd.name
        if self.cwd.root:
            print("/")
            return
        temp_wd = self.cwd.parent
        while(temp_wd.root != True):
            cwd_str = "{}/{}".format(temp_wd.name, cwd_str)
            temp_wd = temp_wd.parent
        print("/{}".format(cwd_str))

    def ret_wd(self):
        cwd_str = self.cwd.name
        if self.cwd.root:
            return "/ "
        elif self.cwd.home:
            return "~/ "
        temp_wd = self.cwd.parent
        while(temp_wd.root != True and temp_wd.home != True):
            cwd_str = "{}/{}".format(temp_wd.name, cwd_str)
            temp_wd = temp_wd.parent
        if temp_wd.home:
            return "~/{} ".format(cwd_str)
        else:
            return "/{} ".format(cwd_str)

    def cd(self, args=None):
        if args is None:
            print("\033[94mToo few arguments\033[0m")
        elif len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        elif args[0] == "..":
            if self.cwd.root != True:
                self.cwd = self.cwd.parent
        elif args[0] == ".":
            pass
        elif args[0] == "~":
            for i in range(len(self.root.contents)):
                if self.root.contents[i].home:
                    self.cwd = self.root.contents[i]
                    break
        elif args[0] == "/":
            self.cwd = self.root
        else:
            for i in range(len(self.cwd.contents)):
                if self.cwd.contents[i].name == args[0] and type(self.cwd.contents[i]) is Folder:
                    self.cwd = self.cwd.contents[i]
                    return
                if self.cwd.contents[i].name == args[0]:
                    print("\033[94mNot a directory\033[0m")
                    return
            print("\033[94mNo such file or directory\033[0m")

    def mkdir(self, args):
        if len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        else:
            for i in FILENAME_RESTRICTIONS:
                if i in args[0]:
                    print("\033[94mERROR: Directory name cannot reserved characters\033[0m")
                    return
            for i in self.cwd.contents:
                if(i.name == args[0]):
                    print("\033[94mERROR: Directory already exists\033[0m")
                    return
            folder = Folder(args[0], self.usr, self.cwd, False, False, True)
            self.cwd.contents.append(folder)

    def touch(self, args):
        if len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        else:
            for i in FILENAME_RESTRICTIONS:
                if i in args[0]:
                    print("\033[94mERROR: File name cannot reserved characters\033[0m")
                    return
            for i in self.cwd.contents:
                if(i.name == args[0]):
                    print("\033[94mERROR: File already exists\033[0m")
                    return
            new_file = File(args[0], self.usr.name, self.cwd, True, False, True)
            self.cwd.contents.append(new_file)

    def ls(self, args=None):
        # TODO: Add ability to cd multiple directories separated by // or with ../ or ../../, etc
        if args is None:
            for i in self.cwd.contents:
                if(type(i) == Folder):
                    print("\033[95m{}\033[0m".format(i.name), end="  ")
                elif(type(i) == File):
                    if(i.executable):
                        print("\033[32m{}\033[0m".format(i.name), end="  ")
                    else:
                        print(i.name, end="  ")
                else:
                    print(i.name, end="  ")
            if self.cwd.contents:
                print("")
        elif len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        else:
            if args[0] == "-l":
                for i in self.cwd.contents:
                    if(type(i) == Folder):
                        print("\033[95m{0: <15}\033[0m drwx  {1: <7}".format(i.name, self.usr.name))
                    elif(type(i) == File):
                        if(i.executable):
                            print("\033[32m{0: <15}\033[0m {1: <4}  {2: <7}".format(i.name, i.perm_str, self.usr.name))
                        else:
                            print("{0: <15} {1: <4}  {2: <7}".format(i.name, i.perm_str, self.usr.name))
                    else:
                        print("{0: <15} -r--  {1: <7}".format(i.name, self.usr.name))
                return
            else:
                print("\033[94mIncorrect format\033[0m")

    def chmod(self, args):
        if len(args) > 2:
            print("\033[94mToo many arguments\033[0m")
        elif len(args) < 1:
            print("\033[94mToo few arguments\033[0m")
        else:
            for i in range(len(self.cwd.contents)):
                if self.cwd.contents[i].name == args[1] and type(self.cwd.contents[i]) is File:
                    if args[0] == "+w":
                        self.cwd.contents[i].write = True
                        self.cwd.contents[i].perm_str = self.cwd.contents[i].perm_str[:2] + 'w' + self.cwd.contents[i].perm_str[3:]
                    elif args[0] == "+x":
                        self.cwd.contents[i].executable = True
                        self.cwd.contents[i].perm_str = self.cwd.contents[i].perm_str[:3] + 'x' + self.cwd.contents[i].perm_str[4:]
                    elif args[0] == "-w":
                        self.cwd.contents[i].write = False
                        self.cwd.contents[i].perm_str = self.cwd.contents[i].perm_str[:2] + '-' + self.cwd.contents[i].perm_str[3:]
                    elif args[0] == "-x":
                        self.cwd.contents[i].executable = False
                        self.cwd.contents[i].perm_str = self.cwd.contents[i].perm_str[:3] + '-' + self.cwd.contents[i].perm_str[4:]
                    else:
                        print("\033[94mIncorrect format\033[0m")
                    return
            print("\033[94mFile does not exist\033[0m")

    def python(self, args):
        if len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        else:
            for i in range(len(self.cwd.contents)):
                if self.cwd.contents[i].name == args[0] and type(self.cwd.contents[i]) is File:
                    if self.cwd.contents[i].executable:
                        exec(self.cwd.contents[i].contents)
                    else:
                        print("\033[94mFile is not executable\033[0m")
                    return

    def anote(self, args):
        if len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        else:
            for i in range(len(self.cwd.contents)):
                if self.cwd.contents[i].name == args[0] and type(self.cwd.contents[i]) is File:
                    if self.cwd.contents[i].write:
                        # TODO: EDIT TEXT
                        print("\033[94mFile is not writable\033[0m")
                    else:
                        print("\033[94mFile is not writable\033[0m")
                    return

    def rm(self, args):
        if len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        else:
            if args[0] == '*':
                self.cwd.contents.clear()
            else:
                for i in range(len(self.cwd.contents)):
                    if self.cwd.contents[i].name == args[0]:
                        self.cwd.contents.remove(self.cwd.contents[i])
                        return
                print("\033[94mFile or directory does not exist\033[0m")

    def man(self, args=None):
        if args is None:
            pass
        elif len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        else:
            if args[0] == "man":
                CUR_MAN = manuals.MAN_MAN
            elif args[0] == "ls":
                CUR_MAN = manuals.MAN_LS
            elif args[0] == "pwd":
                CUR_MAN = manuals.MAN_PWD
            else:
                print("\033[94mCannot find manual for {}\033[0m".format(args[0]))
                return
            print("\33[1mNAME\33[0m \n     {} \n".format(CUR_MAN[0]))
            print("\33[1mSYNOPSIS\33[0m \n     {} \n".format(CUR_MAN[1]))
            print("\33[1mDESCRIPTION\33[0m \n     {} \n".format(CUR_MAN[2]))
            print("\33[1mOPTIONS\33[0m \n     {} \n".format(CUR_MAN[3]))

    def su(self, args):
        if len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        else:
            for i in self.users:
                if i.name == args[0]:
                    if i.password == "":
                        self.usr = i
                    elif i.password == input("Enter password for {}: ".format(i.name)):
                        self.usr = i
                    else:
                        print("\033[94mIncorrect password\033[0m")
                    return
            print("\033[94mUser {} does not exist\033[0m".format(args[0]))

    def useradd(self, args=None):
        if args is None:
            print("\033[94mToo few arguments\033[0m")
        elif len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        else:
            for i in self.users:
                if i.name == args[0]:
                    print("\033[94mUser {} already exists\033[0m".format(i.name))
                    return
            self.users.append(User(args[0], False, input("Enter new password for {}: ".format(args[0]))))

    # TODO: Password changes applicable only to admins
    def passwd(self, args=None):
        if args is None:
            print("\033[94mToo few arguments\033[0m")
        elif len(args) > 1:
            print("\033[94mToo many arguments\033[0m")
        else:
            for i in self.users:
                if i.name == args[0]:
                    i.password = input("Enter new password for {}: ". format(i.name))
                    return
            print("\033[94mUser {} does not exist\033[0m".format(args[0]))

    def diag(self):
        for i in self.users:
            print(i.name)
            print(i.password)
        print(self.usr.name)

    def exit(self):
        print("Exiting demo shell...")
        self.active = False
