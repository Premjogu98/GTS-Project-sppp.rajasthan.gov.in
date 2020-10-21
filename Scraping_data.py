# This Python file uses the following encoding: utf-8
import time
from datetime import datetime
import Global_var
from insert_on_database import insert_in_Local
import sys , os
import urllib.request
import urllib.parse
import re
import string
import time
import requests
import wx
import html
from googletrans import Translator
app = wx.App()


# def Translate(text_without_translate):
#     a1 = 0
#     while a1 == 0:
#         try:
#             String2 = str(text_without_translate)
#             url = "https://translate.google.com/m?hl=en&sl=auto&tl=en&ie=UTF-8&prev=_m&q=" + str(String2) + ""
#             r = requests.get(url)
#             text = r.text
#             text = html.unescape(str(text)).strip()
#             trans_data = text.partition('<div dir="ltr" class="t0">')[2].partition("</div>")[0].strip()
#             trans_data = html.unescape(str(trans_data)).strip()
#             remove_tag = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
#             trans_data = re.sub(remove_tag, '', trans_data).strip()
#             return trans_data
#         except Exception as e:
#             a1 = 0
#             exc_type , exc_obj , exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,
#                   "\n" , exc_tb.tb_lineno)
#             time.sleep(5)


def Scraping_data(get_htmlSource):
    a = 0
    while a == 0:
        try:
            SegFeild = []
            for data in range(45):
                SegFeild.append('')
            new_get_htmlSource = get_htmlSource.replace("\n" , "").replace('ng-if="!isjson"' , "")
            new_get_htmlSource = new_get_htmlSource.replace("&nbsp;" , " ")
            new_get_htmlSource = new_get_htmlSource.replace("&amp;amp" , "&")
            new_get_htmlSource = new_get_htmlSource.replace("&amp;" , "&")
            new_get_htmlSource = new_get_htmlSource.replace("&;amp" , "&")
            new_get_htmlSource: str = new_get_htmlSource.replace("&quot;" , "\"")
            new_get_htmlSource: str = new_get_htmlSource.replace("&QUOT;" , "\"")
            new_get_htmlSource: str = new_get_htmlSource.replace("&nbsp;" , " ")
            new_get_htmlSource: str = new_get_htmlSource.replace("&NBSP;" , " ")
            new_get_htmlSource: str = new_get_htmlSource.replace("&amp;amp" , "&")
            new_get_htmlSource: str = new_get_htmlSource.replace("&AMP;AMP" , "&")
            new_get_htmlSource: str = new_get_htmlSource.replace("&amp;" , "&")
            new_get_htmlSource: str = new_get_htmlSource.replace("&AMP;" , "&")
            new_get_htmlSource: str = new_get_htmlSource.replace("&;amp" , "&")
            new_get_htmlSource: str = new_get_htmlSource.replace("&;AMP" , "&")
            new_get_htmlSource = html.unescape(str(new_get_htmlSource))
            Email = re.search(r'(?<=<td class="data_text">Email: ).*?(?=, Mobile)' , get_htmlSource).group(0)
            Email = Email.replace("[at]" , "@")
            Email = Email.replace("[dot]" , ".")
            SegFeild[1] = Email.strip()
            

            # Address
            CustomerName = ""
            CustomerName = re.search(r'(?<=Procuring Entity Name:).*?(?=</tr>)' , new_get_htmlSource).group(0)
            CustomerName = re.search(r'(?<=class="data_text">).*?(?=</td>)' , CustomerName).group(0)
            CustomerName = re.sub(' +', ' ', str(CustomerName))
            if re.match("^[\W A-Za-z0-9_@?./#&+-]*$" , CustomerName):
                print()  # This string are in English
            else:
                translator = Translator()
                translator_text = translator.translate(str(CustomerName))
                CustomerName = translator_text.text
            if CustomerName.isupper():
                CustomerName = string.capwords(str(CustomerName)).strip()
            Address = re.search(r'(?<=Office Address).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Address = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Address).group(0)
            Address = re.sub(' +', ' ', str(Address))
            
            if Address[0].islower():
                Address = str(Address[0]).upper() + Address[1:]
            else:
                pass
            if Address.isupper():
                Address = string.capwords(str(Address))
            # print(Address)
            SegFeild[2] = Address.strip() + "<br>\n""Name: " + CustomerName.strip()

            Col5_var = str(SegFeild[2])
            Col5_Address = Col5_var.partition(", Phone No")[0]
            Col5_Phone = Col5_var.partition("Phone No")[2].partition("Fax No")[0].replace(".", "").replace(":", "").replace(",","").strip()
            Col5_Fax = Col5_var.partition("Fax No")[2].partition("<br>")[0].replace("." , "").replace(":" , "").strip()
            Col5_BidOpen_Date = re.search(r'(?<=Bid Open Date</td>).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Col5_BidOpen_Date = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Col5_BidOpen_Date).group(0).strip()
            datetime_object = datetime.strptime(Col5_BidOpen_Date.strip() , '%d/%m/%Y')
            Col5_BidOpen_Date = datetime_object.strftime("%Y-%m-%d")
            Col5_DocStartDate = "NA"
            if Col5_Phone != "" and Col5_Fax != "":
                SegFeild[3] = Col5_Address + "<br>\r\n" + "Name : " + CustomerName + "~" + SegFeild[1] + "~" + Col5_Phone + "/" + Col5_Fax + "~" + Col5_DocStartDate + "~" + Col5_BidOpen_Date
            else:
                Col5_MainAddress = Col5_Address + "<br>\r\n" + "Name : " + CustomerName + "~" + SegFeild[1] + "~" + Col5_Phone + "/" + Col5_Fax + "~" + Col5_DocStartDate + "~" + Col5_BidOpen_Date
                SegFeild[3] = Col5_MainAddress.replace("/", "").strip()
            # Country

            SegFeild[7] = "IN"

            # CustomerName
            Department_Name = re.search(r'(?<=Department Name).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Department_Name = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Department_Name).group(0).upper()
            Department_Name = re.sub(' +', ' ', str(Department_Name))  # Remove Multiple Spaces
            
            SegFeild[12] = Department_Name.strip()

            # Tender NO
            Tender_no = re.search(r'(?<=UBN).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Tender_no = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Tender_no).group(0)
            Tender_no = re.sub(' +', ' ', str(Tender_no))
            SegFeild[13] = Tender_no.strip()

            SegFeild[14] = "2"  # notice_type

            # Tender Details
            Bid_Type = ''
            Bid_Type = re.search(r'(?<=Bid Type).*?(?=</tr>)', new_get_htmlSource).group(0)
            Bid_Type = re.search(r'(?<=class="data_text">).*?(?=</td>)', Bid_Type).group(0).lower()

            Bid_Sub_Type = re.search(r'(?<=Bid Sub Type).*?(?=</tr>)', new_get_htmlSource).group(0)
            Bid_Sub_Type = re.search(r'(?<=class="data_text">).*?(?=</td)', Bid_Sub_Type).group(0).lower()

            Dec_Title = re.search(r'(?<=Bid Title).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Dec_Title = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Dec_Title).group(0)
            Dec_Title = Dec_Title.replace("&amp;amp" , "&")
            Dec_Title = re.sub('\s+', ' ', str(Dec_Title))
            Dec_Title = str(Dec_Title[0:200])
            # if re.match("^[\W A-Za-z0-9_@?./#&+-]*$" , Dec_Title):
            #     print()  # This string are in English
            # else:
            #     translator = Translator()
            #     translator_text = translator.translate(str(Dec_Title))
            #     Dec_Title = translator_text.text
            try:
                if Dec_Title[0].islower():
                    Dec_Title = str(Dec_Title[0]).upper() + Dec_Title[1:]
                else:
                    if Dec_Title.isupper():
                        Dec_Title = string.capwords(str(Dec_Title))
            except:pass

            Bid_Pattern = re.search(r'(?<=Bid Pattern).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Bid_Pattern = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Bid_Pattern).group(0)

            Bid_Amount = re.search(r'(?<=Bid Amount).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Bid_Amount = re.search(r'(?<=</i>).*?(?=</td>)' , Bid_Amount).group(0).replace(" ", "").replace(',','')

            Bid_Required_in_Cover = re.search(r'(?<=Bid Required in Cover).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Bid_Required_in_Cover = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Bid_Required_in_Cover).group(0).replace(" ","")

            Bid_Uploaded_Date = re.search(r'(?<=Bid Uploaded Date).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Bid_Uploaded_Date = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Bid_Uploaded_Date).group(0).replace(" " , "")

            Bid_Publish_Date = re.search(r'(?<=Bid Publish Date).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Bid_Publish_Date = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Bid_Publish_Date).group(0).replace(" " , "")

            Available_for_Public_Since = re.search(r'(?<=Available for Public Since Date).*?(?=</tr>)' ,new_get_htmlSource).group(0)
            Available_for_Public_Since = re.search(r'(?<=class="data_text">).*?(?=</td>)' ,Available_for_Public_Since).group(0).replace(" " , "")

            Bid_Submission_End_Date = re.search(r'(?<=Bid Submission End Date).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Bid_Submission_End_Date = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Bid_Submission_End_Date).group(0).replace(" " , "")

            Bid_Open_Date = re.search(r'(?<=Bid Open Date).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Bid_Open_Date = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Bid_Open_Date).group(0).replace(" " , "")

            Tenders_Details = "Title:" + Dec_Title.strip() + "<br>\n""Bid Type:" + Bid_Type.strip() + "<br>\n""Bid Sub Type: " + Bid_Sub_Type.strip() + "<br>\n""Bid Pattern: " + Bid_Pattern.strip() + "<br>\n""Bid Amount: " + Bid_Amount.strip() + "<br>\n""Bid Required in Cover: " + Bid_Required_in_Cover.strip() + "<br>\n""Bid Uploaded Date: " + Bid_Uploaded_Date.strip() + "<br>\n""Bid Publish Date: " + Bid_Publish_Date.strip() + "<br>\n""Available for Public Since: " + Available_for_Public_Since.strip() + "<br>\n""Bid Submission End Date: " + Bid_Submission_End_Date.strip() + "<br>\n""Bid Open Date: " + Bid_Open_Date.strip()
            Tenders_Details = str(Tenders_Details).strip('()')
            SegFeild[18] = Tenders_Details

            # Title Of Tender

            Bid_Type = re.search(r'(?<=Bid Type).*?(?=</tr>)', new_get_htmlSource).group(0)
            Bid_Type = re.search(r'(?<=class="data_text">).*?(?=</td>)', Bid_Type).group(0).strip().lower()

            Bid_Sub_Type = re.search(r'(?<=Bid Sub Type).*?(?=</tr>)', new_get_htmlSource).group(0)
            Bid_Sub_Type = re.search(r'(?<=class="data_text">).*?(?=</td)', Bid_Sub_Type).group(0).strip().lower()

            Global_var.Main_Title = re.search(r'(?<=Bid Title).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Global_var.Main_Title = re.search(r'(?<=class="data_text">).*?(?=</td>)' , Global_var.Main_Title).group(0).strip()
            Global_var.Main_Title = Global_var.Main_Title.replace("&amp;amp" , "&")
            # if re.match("^[\W A-Za-z0-9_@?./#&+-]*$" , Global_var.Main_Title):  # NON Numeric
            #     print()  # This string are in English
            # else:
            #     # Global_var.Main_Title = Translate(Global_var.Main_Title)  # i have to translate this string
            #     translator = Translator()
            #     translator_text = translator.translate(str(Global_var.Main_Title))
            #     Global_var.Main_Title = translator_text.text
            #     Global_var.Main_Title = string.capwords(str(Global_var.Main_Title.strip()))
            if len(Global_var.Main_Title) < 15:
                if re.match('^[0-9]*$', Global_var.Main_Title):
                    if Bid_Type.lower() == "work" or Bid_Type.lower() == "works":
                        Global_var.Main_Title = "Tender are invited for " + Bid_Sub_Type + " work"
                    else:
                        Global_var.Main_Title = ''
                else:
                    if Bid_Type.lower() == "goods" or Bid_Type.lower() == "good":
                        Global_var.Main_Title = "Supply Of " + str(Global_var.Main_Title)
                    elif Bid_Type.lower() == "services" or Bid_Type.lower() == "service":
                        Global_var.Main_Title = "Tender are invited for " + str(Global_var.Main_Title)
                    elif Bid_Type.lower() == "work" or Bid_Type.lower() == "works":
                        Global_var.Main_Title = "Tender are invited for " + str(Global_var.Main_Title) + " work"
                        Global_var.Main_Title = Global_var.Main_Title.replace("works work", 'works').replace("work work", 'work').replace(
                            "Works work", 'works')
                    else:
                        Global_var.Main_Title = ''
                    Global_var.Main_Title = string.capwords(str(Global_var.Main_Title))
                    SegFeild[19] = Global_var.Main_Title.strip()
            else:
               
                Global_var.Main_Title = string.capwords(str(Global_var.Main_Title))
                SegFeild[19] = Global_var.Main_Title.strip()

            # Bid_Amount
            Bid_Amount = re.search(r'(?<=Bid Amount).*?(?=</tr>)' , new_get_htmlSource).group(0)
            Bid_Amount = re.search(r'(?<=</i>).*?(?=</td>)' , Bid_Amount).group(0).replace(" ", "")
            if Bid_Amount != "":
                SegFeild[20] = Bid_Amount.strip()
                SegFeild[21] = 'INR'
            else:
                SegFeild[20] = ""

            # Submission Date
            Bid_Submission_End_Date2 = re.search(r'(?<=Bid Submission End Date).*?(?=</tr>)' ,new_get_htmlSource).group(0)
            Bid_Submission_End_Date2 = re.search(r'(?<=class="data_text">).*?(?=</td>)' ,Bid_Submission_End_Date2).group(0)
            Bid_Submission_End_Date2 = Bid_Submission_End_Date2.replace(" " , "")
            datetime_object = datetime.strptime(Bid_Submission_End_Date2 , '%d/%m/%Y')
            Bid_Submission_End_Date2 = datetime_object.strftime("%Y-%m-%d")
            SegFeild[22] = ""  # doc_cost
            SegFeild[24] = Bid_Submission_End_Date2.strip()
            SegFeild[26] = ""  # earnest_money
            SegFeild[27] = "0"  # Financier
            SegFeild[42] = SegFeild[7]
            SegFeild[43] = ""
            # Tender Link
            SegFeild[28] = 'https://sppp.rajasthan.gov.in'

            # Tender Source
            SegFeild[31] = "sppp.rajasthan.gov.in"

            for SegIndex in range(len(SegFeild)):
                print(SegIndex, end=' ')
                print(SegFeild[SegIndex])
                SegFeild[SegIndex] = html.unescape(str(SegFeild[SegIndex]))
                SegFeild[SegIndex] = str(SegFeild[SegIndex]).replace("'", "''").replace('#39;', '\'')
            a = 1
            if len(SegFeild[19]) >= 200:
                SegFeild[19] = str(SegFeild[19])[:200]+'...'
            Check_date(get_htmlSource, SegFeild)
        except Exception as e:
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname ,"\n" , exc_tb.tb_lineno)


def Check_date(get_htmlSource , SegFeild):
    a = 0
    while a == 0:
        tender_date = str(SegFeild[24])
        nowdate = datetime.now()
        date2 = nowdate.strftime("%Y-%m-%d")
        try:
            if tender_date != '':
                deadline = time.strptime(tender_date , "%Y-%m-%d")
                currentdate = time.strptime(date2 , "%Y-%m-%d")
                if deadline > currentdate:
                    insert_in_Local(get_htmlSource , SegFeild)
                    a = 1
                else:
                    print("Expired")
                    Global_var.expired += 1
                    a = 1
            else:
                print("Deadline was not given")
                Global_var.deadline_Not_given += 1
                a = 1
        except Exception as e:
            exc_type , exc_obj , exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" ,exc_tb.tb_lineno)
            a = 0
