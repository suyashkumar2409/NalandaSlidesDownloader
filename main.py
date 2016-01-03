__author__ = 'Suyash Kumar'

from bs4 import BeautifulSoup
import requests
import os


root = r'C:\Users\Suyash Kumar\Desktop\NalandaSlides'


def correctify(string):
    pos = string.index("(")-1
    return "/"+string[:pos]

def makeDirectory(path):
    try:
        if not os.path.exists(path):
            #os.mkdir(path)
            os.mkdir(path)
    except:
        print(path+" could not be created")



def downloadSlide(path,curses,pdfUrl_a,name):
    try:
        name = "/"+name
        if not os.path.exists(path+name):
            response = curses.get(pdfUrl_a["href"])
            with open(path+name, "wb") as code:
                code.write(response.content)

            print(name[1:]+" downloaded.")
        else:
            print(name[1:]+" already present.")
    except:
        print(name[1:]+" of "+path+" directory could not be downloaded")

def login():
    loginUrl = "http://nalanda.bits-pilani.ac.in/login/index.php"
    curses = requests.session()

    username = input("Enter username")
    password = input("Enter password")
    loginInfo = {"username":username,"password":password}
    response = curses.post(loginUrl,data = loginInfo)

    try:
        parser = BeautifulSoup(response.content,'html.parser')
    except:
        pass

    return [parser,curses]

def scrape(parser,curses,path):
    yesmax = input("Do you want to download every slide of every subject?(yes/no)")
    for each in parser.select(".course_title"):
        #print(each.text)
        subj_a = each.find_all("a")[0]

#        print(subj_a.text)

        subj_title = subj_a["title"]

        subj_title = correctify(subj_title)

        subj_link = subj_a["href"]

        #print(subj_link)


        #print(path+str(subj_title))
        subjPage = curses.get(subj_link)
        #print(subj_title)


        try:
            subjParser = BeautifulSoup(subjPage.content,"html.parser")
        except:
            pass

        if yesmax=="no":
            yes = input("Downloading "+subj_title[1:]+", should it be downloaded?")

        if yesmax=="no" and yes=="no":
            continue
        else:
            makeDirectory(path+str(subj_title))
            print("Downloading "+subj_title[1:])
            for slide in subjParser.find_all("li",{"class":"activity resource modtype_resource"}):

                try:
                    slide_a = slide.find_all("a")[0]
                except:
                    pass


                slide_title = slide_a.text
                slide_href = slide_a["href"]

                slidePage = curses.get(slide_href)

                try:
                    slidePageParser = BeautifulSoup(slidePage.content,"html.parser")
                except:
                    pass

                try:
                    pdfUrl_a = slidePageParser.find_all("object")[0].find_all("a")[0]
                except:
                    pass


                name=pdfUrl_a.text

               # print(name)
               # time.sleep(10)
                try:
                    downloadSlide(path+subj_title,curses,pdfUrl_a,name)
                except:
                    pass






def main(root):

    makeDirectory(root)

    folderName = r'\NalandaSlides'

    makeDirectory(root+folderName)


    [parser,curses] = login()

    scrape(parser,curses,root+folderName)


main(root)