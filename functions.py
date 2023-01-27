from search import *
import os


def choice():

    txt = input("What do you want to do? \n     -add a manhua : writes -m\n     -you have finished \
reading a chapter : writes -c\n     -update your manhua list : writes -l\n     -quit : writes -q\n?")
    if txt == "-m":
        add_manhua()
    elif txt == "-c":
        add_chapter()
    elif txt == "-l":
        print("\nProgram is processing...\nIt takes approximatly 2s per manhua in your csv file!\n")
        manhua_list()
    elif txt == "-q":
        return
    else:
        choice()


########################################################################################################
#                                        Add manhua section                                            #
########################################################################################################
def add_manhua():
    name = input("\nWhat is the name of the manhua you want to add?\n?")
    link = input(
        "On which website is it available?\nWrites 0 if 1stkissmanga.io and 1 if asurascan.gg\n?")
    chap = input("What is the latest chapter you read?\?")

    website = ["https://1stkissmanga.io", "https://asura.gg"]

    if link != "0" and link != "1":
        print("\n\n\nI didn't understand which website you want\n")
        add_manhua()
    if os.path.isfile("sites.csv"):
        with open("sites.csv", "a") as f:
            f.write("\n" + website[int(link)] + ";" + name + ";" + chap)
    else:
        with open("sites.csv", "w") as f:
            f.write(website[int(link)] + ";" + name + ";" + chap)

    print("\nYou have successfully added the manhua \""+name +
          "\" chap " + chap + " from " + website[int(link)])
    and_now()


def and_now():
    what_to_do = input("\nWhat do you want to do now?\n   - continue : writes -c\n   - return to main menu : writes \
-m\n   - quit program : writes -q\n?")
    if what_to_do == "-c":
        add_manhua()
    if what_to_do == "-m":
        choice()
    if what_to_do == "-q":
        return
    else:
        and_now()

########################################################################################################
#                                     Increase chapter section                                         #
########################################################################################################


def add_chapter():
    instruction = input("\nWrites the name of the manhua you have finished reading and press enter.\n\
If you want to return to the main menu, writes -m\nIf you want to quit, writes -q\nWrites -? xxx to \
display all manhua in your list starting with xxx\n?")

    if instruction[:2] == "-q":
        return
    elif instruction[:2] == "-?":
        if instruction[3:] != "":
            print_manhua(instruction[3:])
        add_chapter()
    elif instruction[:2] == "-m":
        choice()
    else:
        if instruction != "":
            incr_manhua(instruction)
        add_chapter()


def incr_manhua(text):
    find_it = False
    idx = 0
    idx_line = -1
    with open("sites.csv", "r") as f:
        for line in f:
            list_line = line.split(";")
            name = list_line[1]
            if name == text:
                idx_line = idx
                find_it = True
            idx += 1

    if (find_it and idx_line != -1):
        update_file = ""
        with open("sites.csv", "r+") as f:
            for line in f:
                list_line = line.split(";")
                name = list_line[1]
                if name == text:
                    previous_num = list_line[2]
                    list_line[2] = str(int(previous_num)+1)
                    print("\nPreviously at chap " + str(previous_num) +
                          "\nNow at chap "+list_line[2])
                    line = ';'.join(list_line)
                    line += "\n"
                update_file += line
            f.seek(0)
            f.truncate()
            f.write(update_file)


def print_manhua(text):
    print("-------------------------------------------------------")
    with open("sites.csv", "r") as f:
        for line in f:
            list_line = line.split(";")
            name = list_line[1]
            if name[:len(text)] == text:
                print(name)
                print("-------------------------------------------------------")
    print("\n")
