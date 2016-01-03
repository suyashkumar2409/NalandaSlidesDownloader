__author__ = 'Suyash Kumar'

from bs4 import BeautifulSoup
import requests
import os
import shutil
import time

def correctify(string):
    pos = string.index("(")
    return string[:pos]+"/"

def makeDirectory(path):
    if not os.path.exists(path):
        #os.mkdir(path)
        os.makedirs(path)


def downloadSlide(path,response,name):
    with open(path+name, "wb") as code:
        code.write(response.content)

def login():
    loginUrl = "http://nalanda.bits-pilani.ac.in/login/index.php"
    curses = requests.session()

    loginInfo = {"username":"f2014053","password":"hhelibebcnofne10"}
    response = curses.post(loginUrl,data = loginInfo)

    parser = BeautifulSoup(response.content,'html.parser')

    return [parser,curses]

def scrape(parser,curses,path):
    for each in parser.select(".course_title"):
        #print(each.text)
        subj_a = each.find_all("a")[0]

#        print(subj_a.text)

        subj_title = subj_a["title"]

        subj_title = correctify(subj_title)

        subj_link = subj_a["href"]

        print(subj_link)

        makeDirectory(path+str(subj_title))
        print(path+str(subj_title))
        subjPage = curses.get(subj_link)

        subjParser = BeautifulSoup(subjPage.content,"html.parser")

        for slide in subjParser.find_all("li",{"class":"activity resource modtype_resource"}):
            slide_a = slide.find_all("a")[0]

            slide_title = slide_a.text
            slide_href = slide_a["href"]

            slidePage = curses.get(slide_href)

            slidePageParser = BeautifulSoup(slidePage.content,"html.parser")
            pdfUrl_a = slidePageParser.find_all("object")[0].find_all("a")[0]

            pdfResponse = curses.get(pdfUrl_a["href"])

            name=pdfUrl_a.text

            print(name)
           # time.sleep(10)
            downloadSlide(path+subj_title,pdfResponse,name)






def main():

    root = "C:/testing/"

    temp = "dpn"+"/"
    makeDirectory(temp)

    root = root +temp

    folderName = "NalandaSlides/"

    makeDirectory(root+folderName)


    [parser,curses] = login()

    scrape(parser,curses,root+folderName)


main()