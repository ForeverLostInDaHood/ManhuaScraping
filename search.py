import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def print_list(liste):
    for element in liste:
        print(element + "\n")
    print("-----------------------------------------------------------------------------------------------------")


def builder_kiss(site, name, num):
    name = name.split()  # name writen with spaces between words
    adress = site + "/manga/" + name[0]
    for el in name[1:]:
        adress += "-" + el  # replace spaces with '-'
    return (adress, adress + "/chapter-" + num)


def builder_asura(site, name, num):
    name = name.split()
    adress = site + "/manga/" + name[0]
    link_ch = site + "/" + name[0]
    for el in name[1:]:
        adress += "-" + el
        link_ch += "-" + el
    return (adress, link_ch + "-chapter-" + num)


def manhua_list():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--enable-javascript")

    driver = webdriver.Firefox(options=options)

    sites = {"https://1stkissmanga.io": 0, "https://asura.gg": 1}

    on_hiatus = []
    available = []
    not_available = []

    with open("sites.csv", "r") as f:
        for line in f:
            site, name, num = line.split(";")
            num = num[:-1]

            if sites[site] == 0:
                adresse, chap_link = builder_kiss(site, name, str(int(num)+1))
            elif sites[site] == 1:
                adresse, chap_link = builder_asura(site, name, str(int(num)+1))
            else:
                print("error, can't access website")

            driver.get(adresse)
            text = driver.page_source

            hiatus = "chapter-" + num + "-5"
            precedent = "chapter-"+str(int(num) - 1)
            next = "chapter-"+str(int(num) + 1)

            if next in text:
                available.append(chap_link)
            else:
                if hiatus in text:
                    on_hiatus.append(name)

                elif precedent in text:
                    not_available.append(name + " " + next)
                else:
                    print("Error : can't found the current chapter nor the next one")

    print("available : \n")
    print_list(available)
    print("On hiatus : \n")
    print_list(on_hiatus)
    print("Not available : \n")
    print_list(not_available)

    driver.close()
