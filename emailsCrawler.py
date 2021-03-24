import requests
import re
from bs4 import BeautifulSoup


# this function returns only one email even if there are more .. loop on mails list to output all
# put it in a try and except blokc with Exception to avoid crushing if website has problems
def scrape_email(url, advanced=False):
    try:
        allLinks = []  # all links in website that contains cotnatct , about , etc
        mails = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        links = [a.attrs.get('href') for a in soup.select('a[href]')]
        keywords = [
            "Contact",
            "contact",
            "Kontakt",
            "kontakt",
            "Über",
            "über",
            "career",
            "Career",
            "about",
            "About",
            "impressum",
            "Impressum",
            "ueber",
            "Ueber"
        ]
        for i in links:
            for key in keywords:
                if key in i:
                    allLinks.append(i)
        allLinks = set(allLinks)

        def get_output(mails_):
            if len(mails_) > 1:
                mails_str = ""
                for mail in mails_:
                    mails_str += mail + " , "
                # return mails_str ######################## this edited to show only one email
                return mails_[0]
            else:
                return mails_[0]


        def findmail(soupvar, ret=False):
            anchors = soupvar.find_all('a')
            for a in anchors:
                if a is not None:
                    href = a.attrs.get('href')
                    if href is not None:
                        mailbyhref = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', href)
                        if mailbyhref is not None:
                            print("found : "+mailbyhref.group())
                            if len(mails) == 0 or mailbyhref not in mails:
                                new_mail = mailbyhref.group()
                                mails.append(new_mail)
                        else:
                            text = a.text
                            mailbytext = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', text)
                            if mailbytext is not None:
                                print("found : " + mailbytext.group())
                                if len(mails) == 0 or mailbyhref not in mails:
                                    new_mail2 = mailbytext.group()
                                    mails.append(new_mail2)
            if ret is True:
                if len(mails) == 0:
                    return "Not Found"
                else:
                    return get_output(mails)

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Advanced Email scraping (slower proccess) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if advanced is True:
            for link in allLinks:
                if link.startswith("http") or link.startswith("www"):
                    print("processing: "+link)
                    r = requests.get(link)
                    data = r.text
                    soup = BeautifulSoup(data,'html.parser')
                    findmail(soup)

                else:
                    newurl = url+link
                    print("processing: "+newurl)
                    r = requests.get(newurl)
                    data = r.text
                    soup = BeautifulSoup(data, 'html.parser')
                    findmail(soup)

            mails = list(set(mails))
            if len(mails) == 0:
                return "Not Found"
            else:
                return get_output(mails)

        else:
            return findmail(soup, True)

    except Exception as e:
        return "Not Found"

