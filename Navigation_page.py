from selenium import webdriver
import time
from datetime import datetime
from Scraping_data import Scraping_data
import Global_var
import sys , os
import ctypes
import wx
from selenium.webdriver.common.keys import Keys
app = wx.App()


def Choromedriver():
    try:
        # File_Location = open("D:\\0 PYTHON EXE SQL CONNECTION & DRIVER PATH\\sppp.rajasthan.gov.in\\Location For Database & Driver.txt" , "r")
        # TXT_File_AllText = File_Location.read()
        # Chromedriver = str(TXT_File_AllText).partition("Driver=")[2].partition("\")")[0].strip()
        # browser = webdriver.Chrome(Chromedriver)
        browser = webdriver.Chrome(executable_path=str(f"D:\\Translation EXE\\chromedriver.exe"))
        browser.get('https://sppp.rajasthan.gov.in')
        # alert = browser.switch_to_alert()  # Close Alert Popup
        # alert.dismiss()
        browser.maximize_window()
        time.sleep(2)
        a = 0
        while a == 0:
            try:
                for latest_Active_Bid in browser.find_elements_by_xpath("//*[@id=\"latest_active_bid\"]/a"):
                    latest_Active_Bid.click()
                    a = 1
            except Exception as e:
                a = 0
        a = 0
        while a == 0:
            try:
                for dropdown in browser.find_elements_by_xpath("//*[@id=\"examplesearch_length\"]/label/select"):
                    dropdown.click()
                    for in_date in browser.find_elements_by_tag_name('option'):
                        if in_date.text == '100':
                            in_date.click()
                            a = 1
            except Exception as e:
                a = 0
        navigating_pages(browser)
    except Exception as e:
        print()


def navigating_pages(browser):
    a = 0
    while a == 0:
        try:
            for add in range(1 , 101 , 1):
                xpath = []

                browser.switch_to.window(browser.window_handles[0])
                xpath_link = "//*[@id=\"examplesearch\"]/tbody/tr[" + str(add) + "]/td[8]/a"
                xpath.append(xpath_link)
                xpath_date: str = "//*[@id=\"examplesearch\"]/tbody/tr[" + str(add) + "]/td[2]"
                for publish_date in browser.find_elements_by_xpath(str(xpath_date)):
                    pubdate = publish_date.get_attribute("innerText")
                    datetime_object = datetime.strptime(pubdate , '%d/%m/%Y')
                    publish_date1 = datetime_object.strftime("%Y-%m-%d")
                    print(Global_var.From_Date)
                    if publish_date1 >= Global_var.From_Date:
                        print("♥ Tender Date Alive ♥")
                        print(" Total: " + str(Global_var.Total) + " Duplicate: " + str(Global_var.duplicate) + " Expired: " + str(Global_var.expired) + " Inserted: " + str(Global_var.inserted) + " Skipped: " + str(Global_var.skipped) + " Deadline Not given: " + str(Global_var.deadline_Not_given) + " QC Tenders: "
                                                         + str(Global_var.QC_tender),"\n")
                        clicking_process(browser , xpath)
                        time.sleep(8)
                        a = 1
                        break
                    else:
                        ctypes.windll.user32.MessageBoxW(0 , "Total: " + str(Global_var.Total) + "\n""Duplicate: " + str(Global_var.duplicate) + "\n""Expired: " + str(Global_var.expired) + "\n""Inserted: " + str(Global_var.inserted) + "\n""Skipped: " + str(Global_var.skipped) + "\n""Deadline Not given: " + str(Global_var.deadline_Not_given) + "\n""QC Tenders: "
                                                         + str(Global_var.QC_tender) + "" , "sppp.rajasthan.gov.in" , 1)
                        Global_var.Process_End()
                        browser.close()
                        sys.exit()

        except Exception :
            a = 0
    a = 0
    while a == 0:
        try:
            for add in range(1 , 500 , 1):
                browser.switch_to.window(browser.window_handles[0])
                for next_button in browser.find_elements_by_xpath('//*[@id="examplesearch_next"]'):
                    next_button.click()
                    navigating_pages(browser)
                    a = 1
                    break
        except Exception:
            a = 0


def clicking_process(browser , xpath):
    a = 0
    while a == 0:
        try:
            a1 = 0
            while a1 == 0:
                try:
                    new1 = str(xpath)
                    new = new1.replace("[\'" , "")
                    xpath1 = new.replace("\']" , "")
                    time.sleep(2)
                    for document in browser.find_elements_by_xpath(xpath1):
                        document.click()
                        break
                    time.sleep(2)
                    Global_var.Total += 1
                    a1 = 1
                except:
                    a1 = 0
                    print("---- Kuch Tho Problem Hai Bhai ----")

            browser.switch_to.window(browser.window_handles[1])
            for table in browser.find_elements_by_xpath("//*[@id=\"print-this-table\"]/tbody/tr[2]/td/table"):
                get_htmlSource = table.get_attribute("outerHTML")
                get_htmlSource = str(get_htmlSource).replace('href="sppp/pdfshowrecord.php' ,'href="https://sppp.rajasthan.gov.in/sppp/pdfshowrecord.php').replace('images/','https://sppp.rajasthan.gov.in/images/')
                get_htmlSource = get_htmlSource.replace("&amp;amp" , "&")
                get_htmlSource = get_htmlSource.replace("&amp;" , "&")
                Scraping_data(get_htmlSource , browser)
                browser.switch_to.window(browser.window_handles[1])
                browser.close()
                a = 1
        except Exception as e:
            browser.switch_to.window(browser.window_handles[0])
            a = 0
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,
                  "\n" , exc_tb.tb_lineno)


Choromedriver()
