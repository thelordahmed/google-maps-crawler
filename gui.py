import wx
import wx.xrc
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from time import sleep
import json
import os
import csv
from emailsCrawler import scrape_email
from wx.adv import HyperlinkCtrl
import random
import xpaths as xpaths_module
from webdriver_manager.chrome import ChromeDriverManager
from platform import system

######################################################
######################################################
################# COPYRIGHTS #########################

copyright_name = "Oscar Network Solutions"
hyperlink = False
url = "http://www.facebook.com/lord.ahmed110"

######################################################
######################################################
######################################################

if system() == "Darwin":
    data_folder = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "gmapsCrawlerData"
        )
else:
    data_folder = r'C:\ProgramData\GmapsBot'

os.system(f"mkdir {data_folder}")


class Win(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Google Maps Bot", pos=wx.DefaultPosition,
                          size=wx.Size(746, 506), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        # the icon path is relative to how the script starts .. if it's starting from bundled one exe file it will change to temp file path
        # that's why i need to catch it in "folder" variable
        # self.SetIcon(wx.Icon(f"{folder}\\icon.ico"))

        # i disabled icon loading because it's detected on some systems as virus for trying to access protected folder (sys._MEIPASS)

        self.BackgroundColour = "#444444"
        self.ForegroundColour = "White"
        mainframe = wx.BoxSizer(wx.VERTICAL)
        labelframe = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Places search options"), wx.HORIZONTAL)
        labelframe.SetMinSize(wx.Size(-1, 110))
        search_text_frame = wx.BoxSizer(wx.VERTICAL)
        self.search_label = wx.StaticText(labelframe.GetStaticBox(), wx.ID_ANY, u"Search text ( place category )",
                                          wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE)
        self.search_label.Wrap(-1)
        self.search_label.SetFont(wx.Font(10, 74, 90, 92, False, wx.EmptyString))
        search_text_frame.Add(self.search_label, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.m_textCtrl48 = wx.TextCtrl(labelframe.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        self.m_textCtrl48.SetMinSize(wx.Size(250, -1))
        search_text_frame.Add(self.m_textCtrl48, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        ### selected categories to choose from results ###
        self.category_label = wx.StaticText(labelframe.GetStaticBox(), wx.ID_ANY,
                                            u"selected categories (will only scrape these categores)",
                                            wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE)
        self.category_label.Wrap(-1)
        self.category_label.SetFont(wx.Font(10, 74, 90, 92, False, wx.EmptyString))
        search_text_frame.Add(self.category_label, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.category_ctrl = wx.TextCtrl(labelframe.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.category_ctrl.SetMinSize(wx.Size(250, -1))
        search_text_frame.Add(self.category_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        labelframe.Add(search_text_frame, 1, wx.EXPAND, 5)
        Countries_frame = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText2 = wx.StaticText(labelframe.GetStaticBox(), wx.ID_ANY, u"Cities List", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        self.m_staticText2.SetFont(wx.Font(10, 74, 90, 92, False, wx.EmptyString))
        Countries_frame.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        # file picker
        self.m_filePicker1 = wx.FilePickerCtrl(labelframe.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a file",
                                               u"*.txt", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        self.m_filePicker1.SetMinSize(wx.Size(250, -1))
        Countries_frame.Add(self.m_filePicker1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.country_status = wx.StaticText(labelframe.GetStaticBox(), wx.ID_ANY, u"Searching in : ",
                                            wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE)
        self.country_status.Wrap(-1)
        self.country_status.SetFont(wx.Font(10, 74, 90, 92, False, wx.EmptyString))
        self.country_status.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))

        Countries_frame.Add(self.country_status, 1, wx.ALL | wx.EXPAND, 5)
        labelframe.Add(Countries_frame, 1, wx.EXPAND, 5)
        mainframe.Add(labelframe, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)
        Data_frame = wx.BoxSizer(wx.VERTICAL)
        options_frame = wx.BoxSizer(wx.VERTICAL)

        self.deep_search = wx.CheckBox(self, wx.ID_ANY, u"  Deep searching for emails ( Slower process )",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        self.deep_search.SetFont(wx.Font(10, 74, 90, 92, False, wx.EmptyString))
        options_frame.Add(self.deep_search, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        Data_frame.Add(options_frame, 0, wx.EXPAND, 5)
        export_btn_frame = wx.BoxSizer(wx.HORIZONTAL)
        self.m_button20 = wx.Button(self, wx.ID_ANY, u"Export to csv", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button20.BackgroundColour = "#c9d1d3"
        self.m_button20.SetFont(wx.Font(12, 74, 90, 92, False, "@Microsoft JhengHei UI"))
        export_btn_frame.Add(self.m_button20, 0, wx.ALL, 5)
        Data_frame.Add(export_btn_frame, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)
        # data view
        self.data_view = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        self.data_view.InsertColumn(0, "Name", width=200)
        self.data_view.InsertColumn(1, "Address", width=150)
        self.data_view.InsertColumn(2, "Phone", width=110)
        self.data_view.InsertColumn(3, "website", width=150)
        self.data_view.InsertColumn(4, "E-mail", width=110)
        Data_frame.Add(self.data_view, 1, wx.ALL | wx.EXPAND, 5)
        mainframe.Add(Data_frame, 1, wx.EXPAND, 5)

        counter_frame = wx.BoxSizer(wx.HORIZONTAL)

        self.counter_label = wx.StaticText(self, wx.ID_ANY, u"Results : ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.counter_label.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        self.counter_label.Wrap(-1)
        counter_frame.Add(self.counter_label, 0, wx.ALL, 5)

        self.counter_int = wx.StaticText(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.counter_int.SetFont(wx.Font(12, 70, 90, 90, False, wx.EmptyString))
        self.counter_int.Wrap(-1)
        counter_frame.Add(self.counter_int, 0, wx.ALL, 5)

        mainframe.Add(counter_frame, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        buttons_frame = wx.BoxSizer(wx.HORIZONTAL)
        buttons_frame.SetMinSize(wx.Size(150, 50))
        # start btn & clear btn
        self.Start_btn = wx.Button(self, wx.ID_ANY, u"Start bot", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Start_btn.SetDefault()
        self.Start_btn.BackgroundColour = "#c9d1d3"
        self.Start_btn.SetFont(wx.Font(13, 74, 90, 92, False, "@Microsoft JhengHei UI"))
        self.clear_btn = wx.Button(self, wx.ID_ANY, "Clear Data", wx.DefaultPosition, wx.DefaultSize, 0)
        self.clear_btn.SetFont(wx.Font(11, 74, 90, 92, False, "@Microsoft JhengHei UI"))
        self.clear_btn.BackgroundColour = "#c9d1d3"
        buttons_frame.Add(self.Start_btn, 1, wx.ALL | wx.EXPAND, 5)
        buttons_frame.Add(self.clear_btn, 1, wx.ALL | wx.EXPAND, 5)
        mainframe.Add(buttons_frame, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        # copyrights
        copyrights_frame = wx.BoxSizer(wx.VERTICAL)
        if hyperlink is False:
            self.copyrights = wx.StaticText(self, wx.ID_ANY, f"\u00a9 Copyright 2020 {copyright_name}",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        else:
            self.copyrights = HyperlinkCtrl(self, wx.ID_ANY, f"Developed by : {copyright_name}",
                                            f"{url}", wx.DefaultPosition, wx.DefaultSize)
        self.copyrights.SetFont(wx.Font(10, 70, 90, 92, False, wx.EmptyString))
        self.copyrights.SetBackgroundColour("black")
        copyrights_frame.Add(self.copyrights, 1, wx.ALL | wx.EXPAND, 3)
        mainframe.Add(copyrights_frame, 0, 0, 5)
        self.SetSizer(mainframe)
        self.Layout()
        self.Centre(wx.BOTH)
        # Connect Events
        self.deep_search.Bind(wx.EVT_CHECKBOX, self.advanced_search)
        self.clear_btn.Bind(wx.EVT_BUTTON, self.clear)
        self.Start_btn.Bind(wx.EVT_BUTTON, self.start)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onclose)
        self.m_button20.Bind(wx.EVT_BUTTON, self.csv_export)
        ########################################################################
        self.win = None
        # data is stored here for exporting .. stored as dict of lists
        self.data = {
            "name": [],
            "phone": [],
            "address": [],
            "website": [],
            "email": [],
            "check data": []
        }
        self.processed_urls = []
        self.country = ""
        self.country_index = 0
        self.searchquery = ""
        self.get_history()
        self.searchtext = self.searchquery + " " + self.country.title()
        self.searchplus = self.searchtext.replace(" ", "+")
        self.link = "https://www.google.com/maps/search/" + self.searchplus
        self.thread = Thread(target=self.run, name="process thread", daemon=True)
        self.clean_categories = []
        # get saved history
        self.data_xpath = {
            "name": '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]//h1',
            "phone": '//img[@src="//www.gstatic.com/images/icons/material/system_gm/1x/phone_gm_blue_24dp.png"]/../../../div[2]/div[1]',
            "address": '//img[@src="//www.gstatic.com/images/icons/material/system_gm/1x/place_gm_blue_24dp.png"]/../../../div[2]/div[1]',
            "website": '//img[@src="//www.gstatic.com/images/icons/material/system_gm/1x/public_gm_blue_24dp.png"]/../../../div[2]/div[1]',
            "no_phone": '//*[@id="pane"]/div/div[1]/div/div//h2[@class="section-subheader-header GLOBAL__gm2-subtitle-alt-1"]/following::img[@src="//www.gstatic.com/images/icons/material/system_gm/1x/phone_gm_blue_24dp.png"]',
            "no_address": '//*[@id="pane"]/div/div[1]/div/div//h2[@class="section-subheader-header GLOBAL__gm2-subtitle-alt-1"]/following::img[@src="//www.gstatic.com/images/icons/material/system_gm/1x/place_gm_blue_24dp.png"]',
            "no_website": '//*[@id="pane"]/div/div[1]/div/div//h2[@class="section-subheader-header GLOBAL__gm2-subtitle-alt-1"]/following::img[@src="//www.gstatic.com/images/icons/material/system_gm/1x/public_gm_blue_24dp.png"]',
            "back": '//*[@id="pane"]/div/div[1]/div/div/button/span',
            "back css": '#pane > div > div.widget-pane-content.scrollable-y > div > div > button > span',
            "nextpage": '//button[contains(@id, "__section-pagination-button-next")]',
            "prevpage": '//button[contains(@id, "__section-pagination-button-prev")]',
            "current pages": '//div[contains(@class, "__root")]//span[contains(@class, "__left")]/span[2]',
        }
        self.results = None
        self.advanced_var = False

    # deep search check button command function
    def advanced_search(self, event):
        self.advanced_var = True

    # csv export button command function
    def csv_export(self, event):
        pathpicker = wx.FileDialog(None, u"Where will you save data ?", wx.EmptyString, wx.EmptyString, u"*.csv",
                                   wx.FD_SAVE, wx.DefaultPosition, wx.DefaultSize, "data.csv")
        pathpicker.ShowModal()
        with open(pathpicker.GetPath(), "w", encoding="utf-8", newline="") as f:
            csv_writer = csv.writer(f)

            for name, phone, address, website, email in zip(self.data["name"], self.data["phone"], self.data["address"],
                                                            self.data["website"], self.data["email"]):
                row = [name, phone, address, website, email]
                csv_writer.writerow(row)

    # clear button command function
    def clear(self, event):
        res = wx.MessageDialog(None, "Are you sure you want clear current Data ?", "Data Clear Confirmation",
                               wx.YES_NO | wx.ICON_EXCLAMATION, wx.DefaultPosition).ShowModal()
        if res == wx.ID_YES:
            self.data_view.DeleteAllItems()
            for value in self.data.values():
                value.clear()
            self.processed_urls.clear()
            self.country_index = 0
            self.set_history()
            counter = str(self.data_view.GetItemCount())
            self.counter_int.SetLabel(counter)
        else:
            pass

    def country_list(self):
        with open(self.m_filePicker1.GetPath(), "r") as f:
            country_list = f.read().split("\n")
            return country_list

    # app window close event function
    def onclose(self, event):
        self.set_history()
        self.win.quit()
        app.ExitMainLoop()

    def set_history(self):
        with open(os.path.join(data_folder, "history.json"), "w") as f:
            info = {
                "search": self.m_textCtrl48.GetValue(),
                "path": self.m_filePicker1.GetPath(),
                "data": self.data,
                "urls": self.processed_urls,
                "country_index": self.country_index,
                "current_status": self.country
            }
            f.write(json.dumps(info))
        with open(os.path.join(data_folder, "categories.txt"), "w", encoding="utf-8") as f:
            f.write(self.category_ctrl.GetValue())

    def get_history(self):
        try:
            with open(os.path.join(data_folder, "history.json"), "r") as f:
                info = f.read()
                dict_ = json.loads(info)
            self.m_textCtrl48.SetValue(dict_["search"])
            self.m_filePicker1.SetPath(dict_["path"])
            self.data = dict_["data"]
            self.processed_urls = dict_["urls"]
            self.country_index = dict_["country_index"]
            self.country = dict_["current_status"]
            status = "Searching in: " + self.country.title()
            self.country_status.SetLabelText(status)
            for name, address, phone, website, email in zip(self.data["name"], self.data["phone"],
                                                            self.data["address"], self.data["website"],
                                                            self.data["email"]):
                index = self.data_view.InsertItem(0, name)
                self.data_view.SetItem(index, 1, phone)
                self.data_view.SetItem(index, 2, address)
                self.data_view.SetItem(index, 3, website)
                self.data_view.SetItem(index, 4, email)
            counter = str(self.data_view.GetItemCount())
            self.counter_int.SetLabel(counter)
            with open(os.path.join(data_folder, "categories.txt"), "r", encoding="utf-8") as f:
                self.category_ctrl.SetValue(f.read())
        except Exception:
            pass

    def start(self, event):
        self.thread.start()

    def run(self):
        self.Start_btn.Disable()
        categories = self.category_ctrl.GetValue().split(",")
        # cleaning the cateogries list from spaces
        for cat in categories:
            clean_cat = cat.strip()
            if clean_cat != '':
                self.clean_categories.append(clean_cat)
        # save dir check
        self.set_history()
        # get search text
        self.searchquery = self.m_textCtrl48.GetValue()
        # get country list
        try:  # if list ended .. start over
            self.country = self.country_list()[self.country_index]
        except IndexError:
            self.country_index = 0
            self.country = self.country_list()[self.country_index]
        self.searchtext = self.searchquery + " " + self.country.title()
        self.searchplus = self.searchtext.replace(" ", "+")
        self.link = "https://www.google.com/maps/search/" + self.searchplus
        status = "Searching in: " + self.country.title()
        self.country_status.SetLabelText(status)
        self.Layout()
        self.open()
        self.scrape_data()

    def next_country(self):
        self.country_index += 1
        # get country list
        try:
            self.country = self.country_list()[self.country_index]
            # print("next country is : ", self.country)
        except IndexError:
            # print("no more countries.. The End ^_^")
            self.set_history()
            return False
        self.searchtext = self.searchquery + " " + self.country.title()
        # print("next search text is : ", self.searchtext)
        self.searchplus = self.searchtext.replace(" ", "+")
        self.link = "https://www.google.com/maps/search/" + self.searchplus
        # print("next url search is : ", self.link)
        self.win.get(self.link)
        self.data["check data"].clear()
        status = "Searching in: " + self.country.title()
        self.country_status.SetLabelText(status)
        self.Layout()

    def open(self):
        self.win = webdriver.Chrome(ChromeDriverManager().install())
        self.win.get(self.link)

    def data_protection(self):
        try:
            WebDriverWait(self.win, 1).until(
                ec.visibility_of_element_located(
                    (By.CLASS_NAME, "widget-consent-dialog")))
            self.win.execute_script(
                'document.querySelector("#consent-bump > div > div.widget-consent-dialog").remove()')
            # print("Data Protection pop up Removed Successfully!")
        except TimeoutException:
            # print("Data protection pop up not found .. trying again...")
            try:
                WebDriverWait(self.win, 1).until(
                    ec.visibility_of_element_located(
                        (By.XPATH, "//*[@class='widget-consent-dialog']")
                    )
                )
                self.win.execute_script(
                    'document.querySelector("#consent-bump > div > div.widget-consent-dialog").remove()')
                # print("Data protection pop up not found .. trying again...")
            except TimeoutException:
                # print("Data protection pop up not found!.. continue")
                pass

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< MAIN SCRIPT >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def scrape_data(self):
        while True:
            # waiting for the invisibile div on the results to disappear
            WebDriverWait(self.win, 10).until(ec.invisibility_of_element_located((
                By.XPATH, xpaths_module.ajax_loader)))
            sleep(random.randint(1, 3))  # to avoid bot pattern detection
            try:
                self.win.find_element_by_xpath(self.data_xpath["current pages"]).text
            except Exception as e:
                print(e, "connection lost .. trying in 7 - 10 seconds")
                sleep(random.randint(7, 10))
                self.win.refresh()
                continue

            # DATA PROTECTION >> the data protection pop up work around .. for Germany and Eu countries
            self.data_protection()

            self.results = self.win.find_elements_by_xpath(xpaths_module.results)
            print(len(self.results))
            if len(self.results) == 0:
                self.win.quit()
                sleep(5)
                self.run()
                self.scrape_data()

            i = 0  # result index in results list
            # if len(self.results) > 20:
            #     i = len(self.results) - 20  # changing the start point after the ads

            # FOR LOOP >> the for loop .. it's inside a function to be able to break parent loop
            loop_return = self.forloop(i)
            if loop_return is False:
                break
            elif loop_return is True:
                continue

            # if next page button is not clickable >> stop
            try:
                if self.nextpage() is False:  # next page button not active .. means no more results
                    if self.next_country() is False:
                        break
                    print("no more results .. goning to next country")
                    continue
            except ElementClickInterceptedException:
                if self.next_country() is False:
                    break
                print("no more results .. goning to next country")
                continue
        # STOP POINT >> what happens when program completes***********************************************************
        self.thread = Thread(target=self.run,name="Thread" ,daemon=True)
        self.Start_btn.Enable()
        self.set_history()
        try:
            self.win.quit()
        except Exception:
            pass
        wx.MessageDialog(None, f"{len(self.data['name'])} results scraped.. Bot Finished succssefully ^_^",
                         "Finished Successfully.", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def forloop(self, i):
        for _ in range(len(self.results) - i):
            try:
                try:
                    # sleep(2)
                    self.results = self.win.find_elements_by_xpath(xpaths_module.results)
                except NoSuchElementException:
                    # print("can't get the results")
                    # if False returned .. means no more countries
                    if self.next_country() is False:
                        return False
                    print("no more results .. goning to next country")
                    return True

                ####### SAME BUG FIX START ######

                # getting results data to check before clicking on it to skip faster
                xpaths = [".//div[@class='section-place-result-container-summary']//div[contains(@class, '_title-container')]/div/span | .//h3[@class='section-result-title']/span",
                          ".//div[@class='section-place-result-container-summary']//span[contains(@class,'__rating')] | .//span[@class='cards-rating-score']",
                          ".//div[@class='section-place-result-container-summary']//span[contains(@class,'__reviews')] | .//span[@class='section-result-num-ratings']",
                          ".//div[@class='section-place-result-container-summary']//div[contains(@class, '__title-container')]/../div[last()]/div[1]/span[2]//span[not(@class)] | .//span[@class='section-result-location']"]
                res_check_data = []
                category_path = ".//div[@class='section-place-result-container-summary']//div[contains(@class, '__title-container')]/../div[last()]/div[1]/span[1]//span[not(@style)] | .//span[@class='section-result-details']"

                category = self.results[i].find_element_by_xpath(category_path).text

                for path in xpaths:
                    try:
                        data = self.results[i].find_element_by_xpath(path).text
                    except NoSuchElementException:
                        data = "None"

                    res_check_data.append(data)
                ############ ALGORITHM : choosing the desired category from results #############
                # if scraped data from outside (lcoation, title, score, reviews) in the list .. skip before clicking
                if res_check_data not in self.data["check data"]:
                    if len(self.clean_categories) != 0:  # check if the categores ctrl empty or not
                        if category not in self.clean_categories:
                            print("not selected category")
                            i += 1
                            continue
                    self.data["check data"].append(res_check_data)
                    try:
                        self.results[i].click()
                    except ElementClickInterceptedException:
                        print("ElementClickInterceptedException .. waiting 10 secs")
                        sleep(10)
                        self.results[i].click()
                else:
                    i += 1
                    continue

                # waiting for place info to appear
                try:
                    WebDriverWait(self.win, 10).until(ec.visibility_of_element_located((
                        By.XPATH, self.data_xpath["back"])))
                except TimeoutException:
                    print("the same bug again .. refreshing...")
                    self.win.get(self.link)
                    return True

                ###### SAME BUG FIX END ######
                # SCRAPING POINT >> scraping data >>>>>>>>>>>>
                sleep(2)
                keys = ['name', 'address', 'website']
                phone = self.get_data("phone")
                website = self.get_data(keys[2])  # to get the email .. it's appended in the for loop
                # adding the data structure
                if phone not in self.data["phone"]:
                    for key in keys:
                        value = self.get_data(key)
                        self.data[key].append(value)
                    # Email scrape
                    if website != "No Website":
                        url = "https://www." + website
                        if url not in self.processed_urls:
                            print("scraping email from " + url)
                            if self.advanced_var is True:
                                email = scrape_email(url)
                                if email == "Not Found":
                                    email = scrape_email(url, True)
                            else:
                                email = scrape_email(url)
                            self.processed_urls.append(url)
                        else:
                            email = "Same website"
                    else:
                        email = "Not Found"
                    self.data["email"].append(email)
                    self.data["phone"].append(phone)
                    index = self.data_view.InsertItem(0, self.get_data(keys[0]))
                    self.data_view.SetItem(index, 1, self.get_data(keys[1]))
                    self.data_view.SetItem(index, 2, phone)
                    self.data_view.SetItem(index, 3, website)
                    self.data_view.SetItem(index, 4, email)
                    self.set_history()

                    # updating the counter
                    counter = str(self.data_view.GetItemCount())
                    self.counter_int.SetLabel(counter)
                # back to results
                self.win.find_element_by_xpath(self.data_xpath["back"]).click()
                # waiting for results to appear
                try:
                    sleep(1)
                    WebDriverWait(self.win, 18).until(ec.visibility_of_element_located((
                        By.XPATH, xpaths_module.results)))
                except TimeoutException:
                    print("waited 10 secs . results didn't appear .. clicking back again...")
                    try:
                        self.win.find_element_by_xpath(
                            "//div[@id='pane']//button[@class='section-back-to-list-button blue-link noprint']").click()
                        sleep(1)
                        WebDriverWait(self.win, 18).until(ec.visibility_of_element_located((
                            By.XPATH, xpaths_module.results)))
                        sleep(1)
                    except NoSuchElementException:
                        try:
                            # print('back btn not found .. clicking again with javascript')
                            self.win.execute_script(
                                'document.querySelector("#pane > div > div.widget-pane-content.scrollable-y > div > div > button").click()')
                        except Exception:
                            # print("back button not found .. moving to next country!")
                            if self.next_country() is False:
                                return False
                            # print("no more results .. goning to next country")
                            return True
                    except TimeoutException:
                        # print("clicking back failed .. refreshing...")
                        self.win.get(self.link)
                        return True
                i += 1
            except TimeoutError as e:
                print(e)
                return False

    def nextpage(self):
        try:
            WebDriverWait(self.win, 15).until(
                ec.visibility_of_element_located((By.XPATH, self.data_xpath['nextpage']))).click()
        except TimeoutException:
            return False
        except ElementClickInterceptedException:
            self.data_protection()
            self.win.find_element_by_xpath(self.data_xpath["nextpage"]).click()
        sleep(2)
        # waiting for results to appear
        try:
            self.win.find_elements_by_xpath(xpaths_module.results)
        except NoSuchElementException:
            # print("results not ready after waiting 2 sec .. waiting another 1 ...")
            sleep(2)
            try:
                self.win.find_elements_by_xpath(xpaths_module.results)
            except NoSuchElementException:
                # print("results not ready after waiting 1 sec.. waiting another 5 ... (2)")
                sleep(5)
                try:
                    self.win.find_elements_by_xpath(xpaths_module.results)
                except NoSuchElementException:
                    # print("waited another 5 secs but results didn't appear .. moving to next country")
                    return False

    def get_data(self, data):
        def base_func(dict_key1, return_, dict_key2):
            try:
                self.win.find_element_by_xpath(self.data_xpath[dict_key1])
                return return_
            except NoSuchElementException:
                try:
                    return self.win.find_element_by_xpath(self.data_xpath[dict_key2]).text
                except NoSuchElementException:
                    return "No " + dict_key2

        if data == "phone":
            return base_func("no_phone", "No Phone", "phone")
        elif data == "address":
            return base_func("no_address", "No address", "address")
        elif data == "website":
            return base_func("no_website", "No Website", "website")
        elif data == "name":
            return self.win.find_element_by_xpath(self.data_xpath[data]).text


app = wx.App()
frame = Win(None)
frame.Show()
app.MainLoop()
