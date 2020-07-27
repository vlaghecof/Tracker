from email.mime.multipart import MIMEMultipart

import requests, bs4, re, time, selenium
from selenium import webdriver
from datetime import date, timedelta
import re
import decimal
import smtplib, ssl
from email.mime.text import MIMEText
import sys

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



class Raport :
    def __init__(self,data,todayCases,externariTotal,totalTests,totalSibiu):
           self.data=data
           self.todayCases=todayCases
           self.externariTotal=externariTotal
           self.aziExternari=3
           self.totalTests=totalTests
           self.testeAzi=3
           self.aziSibiu=0
           self.totalSibiu=totalSibiu

    def __init__(self, data, todayCases, externariTotal, totalTests, totalSibiu,aziSibiu):
        self.data = data
        self.todayCases = todayCases
        self.externariTotal = externariTotal
        self.aziExternari = 3
        self.totalTests = totalTests
        self.testeAzi = 3
        self.aziSibiu = aziSibiu
        self.totalSibiu = totalSibiu

    def setExternari (self,  aziExternari):
          self.aziExternari=aziExternari

    def setTotalTests(self, totalTests):
        self.totalTests = totalTests

    def setTesteAzi(self,testeAzi):
        if int(testeAzi)>800000 :
            self.testeAzi=0
        else:
            self.testeAzi=testeAzi
    def setAziSibiu(self,aziSibiu):
        self.aziSibiu=aziSibiu





def getNumberByDateVer2( romanaDate ):

    driver.get("https://stirioficiale.ro/informatii/buletin-de-presa-" + romanaDate + "-ora-13-00")


    rows = driver.find_elements_by_xpath("/html/body/main/div/div[2]/section/div[2]/table[1]/tbody/tr    ")
    usefullData=[]
    for row in rows:
        if str(row.text).__contains__("TOTAL"):
            sup=row.text;
            data = re.findall('([0-9]*\.*[0-9]*)',row.text )

            for ex in data :
                ex1=str(ex).replace(".","")
                if ex1.isdigit():
                    usefullData.append(int(ex1))
            cazuriTotale = int(usefullData[0])
            cazuriAzi = int(usefullData[1])
        if str(row.text).__contains__("Sibiu"):
            dataSibiu=[int(s) for s in str(row.text).split() if s.isdigit()]
            cazuriTotaleSibiu = dataSibiu[0]
            cazuriAziSibiu = dataSibiu[1]

    # textt = numarul de cazuri azi

    # externari=driver.find_element_by_xpath("/html/body/main/div/div[2]/section/article/div/div[2]/p")
    # mesajExternari=str(externari.text)
    # numarExternari=str(re.findall(r' ([0-9]*\.*[0-9]*) au fost externate',mesajExternari)[0]).replace(".","")

    totalTeste=driver.find_element_by_xpath("/html/body/main/div/div[2]/section/div[2]")


    totalNumber=re.findall(r'([0-9]*\.*[0-9]*\.*[0-9]*)\s*(de)? teste',totalTeste.text )


    numberCasses = [number for number, val in totalNumber]
    numberCasses=(numberCasses)


    totalSibiu=int(re.findall(r'Sibiu\n([0-9]*\.*[0-9]*)',totalTeste.text )[0])


    if  len(str(totalNumber))==2 :
        totalNumber=3
    else:
        totalNumber=int( str(numberCasses[1]).replace(".","") )

    raports.append(Raport(romanaDate,cazuriAzi,77,totalNumber,cazuriTotaleSibiu,cazuriAziSibiu))




def getNumberByDate( romanaDate ):

    driver.get("https://stirioficiale.ro/informatii/buletin-de-presa-" + romanaDate + "-ora-13-00")

    info = driver.find_element_by_xpath("/html/body/main/div/div[2]/section/div[2]/p[9]")
    if  not str(info.text).__contains__("De la ultima informare transmisă de Grupul de Comunicare Strategică, au fost"):
        info=driver.find_element_by_xpath("/html/body/main/div/div[2]/section/div[2]/p[8]")
        if not str(info.text).__contains__("De la ultima informare transmisă de Grupul de Comunicare Strategică, au fost"):
            info = driver.find_element_by_xpath("/html/body/main/div/div[2]/section/div[2]/p[10]")

    textt=re.findall(r'\d+', info.text).pop(0)
    mesaj="In data de  "+romanaDate+" au fost " + textt


    externari=driver.find_element_by_xpath("/html/body/main/div/div[2]/section/article/div/div[2]/p")
    mesajExternari=str(externari.text)
    numarExternari=str(re.findall(r' ([0-9]*\.*[0-9]*) au fost externate',mesajExternari)[0]).replace(".","")

    totalTeste=driver.find_element_by_xpath("/html/body/main/div/div[2]/section/div[2]")


    totalNumber=re.findall(r'([0-9]*\.*[0-9]*)\s*(de)? teste',totalTeste.text )

    numberCasses = [number for number, val in totalNumber]
    numberCasses=(numberCasses)


    totalSibiu=int(re.findall(r'Sibiu\n([0-9]*\.*[0-9]*)',totalTeste.text )[0])


    if  len(str(totalNumber))==2 :
        totalNumber=3
    else:
        totalNumber=int( str(numberCasses[0]).replace(".","") )

    raports.append(Raport(romanaDate,textt,numarExternari,totalNumber,totalSibiu,0))

    return mesaj




def getPastDays(pastDaysNumber):
    yesterday = date.today() - timedelta(days=pastDaysNumber)
    monthYES = yesterday.strftime("%B")
    yesterday = yesterday.strftime('%d-' + monthDict[monthYES] + '-2020')
    # print(yesterday)
    return yesterday

def formatRaport(rap):


    # message = f'Data de {rap.data} \nNumarul de cazuri de azi: {rap.todayCases} ' \
    #           # f'\nNumarul total  de cazuri externate: {rap.externariTotal}  \nNumarul de externari de azi:  {rap.aziExternari} ' \
    #           f'\nNumar total  de teste: {rap.totalTests}\nNumar de teste azi: {rap.testeAzi}' \
    #           f'\nTotal in sibiu:  {rap.totalSibiu} \nCazuri sibiu  azi: {rap.aziSibiu}'+"\nProcentul Cazurilor confirmate " + str("{:.2f}".format((decimal.Decimal(rap.todayCases)*100)/decimal.Decimal(rap.testeAzi)))+"% \n-----------------------------------------\n"
    message = f'Data de {rap.data} \nNumarul de cazuri de azi: {rap.todayCases} ' \
              f'\nNumar total  de teste: {rap.totalTests}\nNumar de teste azi: {rap.testeAzi}' \
              f'\nTotal in sibiu:  {rap.totalSibiu} \nCazuri sibiu  azi: {rap.aziSibiu}'+"\nProcentul Cazurilor confirmate " + str("{:.2f}".format((decimal.Decimal(rap.todayCases)*100)/decimal.Decimal(rap.testeAzi)))+"% \n-----------------------------------------\n"

    return message

raports=[]

today = date.today()

monthDict={"July":"iulie","August":"august","September":"septembrie"}

month = today.strftime("%B ").strip()
# print("d2 =", month)

day=today.strftime("%d ").strip()

# print(day)


romanaDate=(str(day)+" "+str(monthDict[month]+" 2020")).replace(" ","-")
# print(romanaDate)

yesterday = date.today() - timedelta(days=1)
# print(yesterday.month)
monthYES=yesterday.strftime("%B")
# print(monthYES)
yesterday=yesterday.strftime('%d-'+monthDict[monthYES]+ '-2020')

# /print(yesterday)




op=webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(executable_path='C:\\Users\\Vlad\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\selenium\\webdriver\\chromedriver.exe',options=op)




# test
#tot asa si pt sibiu
#numarul de teste e bun
#mai trebuie externati
driver.get("https://stirioficiale.ro/informatii/buletin-de-presa-" + romanaDate + "-ora-13-00")
# print("got to the page ")
# rows= driver.find_elements_by_xpath("/html/body/main/div/div[2]/section/div[2]/table[1]/tbody/tr    ")
# for row in rows:
#     if str(row.text).__contains__("TOTAL"):
#        words=str(row.text).split(" ")
#        data=[int(s) for s in str(row.text).split() if s.isdigit()]
#        cazuriTotale=data[0]
#        cazuriAzi=data[1]
#
#        print ( cazuriAzi, " si " , cazuriTotale)
#        print(row.text)
#        print("==========")


# getNumberByDateVer2(romanaDate)
# getNumberByDateVer2(getPastDays(1))
# mesajMail = formatRaport(raports[0])
# mesajMail += formatRaport(raports[1])
#
#
# print(mesajMail)


#
strings = time.strftime("%H")
hour=int(strings)


try:

    driver.get("https://stirioficiale.ro/informatii/buletin-de-presa-" + romanaDate + "-ora-13-00")
    exists=driver.find_element_by_xpath("/html/body/main/article/h1/span")
    offset=1
except:
    offset=0

# if hour<13 :
#     offset=1
# else:
#     offset=0

print(offset)

try:
   # getNumberByDateVer2(romanaDate)
    for i in range(0,4):
        try :

            getNumberByDateVer2(getPastDays(i + offset))
        except:
            getNumberByDate(getPastDays(i+offset))


    for i in range(1, 4):
      raports[i-1].setExternari(int(raports[i-1].externariTotal) -int(raports[i].externariTotal))
      raports[i - 1].setTesteAzi(int(raports[i - 1].totalTests ) - int(raports[i].totalTests))
      raports[i - 1].setAziSibiu (int(raports[i - 1].totalSibiu ) - int(raports[i].totalSibiu))

    textRaport=""

    # for rap in raports:
    #     print("Data de ", rap.data, "\nNumarul de cazuri de azi ",
    #           rap.todayCases + "\nNumarul total  de cazuri:" + rap.externariTotal + "\nNumarul de externari de azi : ",
    #           rap.aziExternari, "\nNumar total  de teste:", rap.totalTests, "\nNumar de teste azi :", rap.testeAzi,
    #           " \nTotal in sibiu ", rap.totalSibiu, "\nCazuri sibiu  azi:", rap.aziSibiu
    #           , "\nProcentul Cazurilor confirmate",
    #           "{:.2f}".format((decimal.Decimal(rap.todayCases) * 100) / decimal.Decimal(rap.testeAzi)))
    #
    #
    #     print("Data de ",rap.data,"\nNumarul de cazuri de azi ",rap.todayCases + "\nNumarul total  de cazuri:"+ rap.externariTotal + "\nNumarul de externari de azi : " ,rap.aziExternari, "\nNumar total  de teste:",rap.totalTests,"\nNumar de teste azi :",rap.testeAzi," \nTotal in sibiu ",rap.totalSibiu,"\nCazuri sibiu  azi:",rap.aziSibiu
    #         ,"\nProcentul Cazurilor confirmate","{:.2f}".format((decimal.Decimal(rap.todayCases)*100)/decimal.Decimal(rap.testeAzi)))
    #     print("--------------------------------------------------------")


    mesajMail=""
    for i in range(3):
        mesajMail+=formatRaport(raports[i] )

    print(mesajMail)
except:
    print("Sa facut buba")


    # try to get the table and the row
    # driver.get("https://stirioficiale.ro/informatii/buletin-de-presa-" + romanaDate + "-ora-13-00")
    # print("got to the page ")
    # rows= driver.find_elements_by_xpath("/html/body/main/div/div[2]/section/div[2]/table[1]/tbody/tr/td    ")
    # for row in rows:
    #     print(row.text)





    sys.exit()


finally:
    driver.close()
    driver.quit()







port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "automateemailtestcv@gmail.com"  # Enter your address
receiver_emails = ["vladcofaru@yahoo.com","nicolae.cofaru@ulbsibiu.ro","ioana.cofaru@ulbsibiu.ro","ionutcofaru@yahoo.com","gabrielasas2007@yahoo.com"]  # Enter receiver address
password = "cofaru123"




# textMessage=f'Azi,In data de {romanaDate} au fost {raports[0].todayCases}   , diferenta fata de ieri a fost de {int(raports[0].todayCases)-int(raports[1].todayCases)} \n' \
#         f'Ieri , in data de {yesterday} au fost {raports[1].todayCases}' \
#         f'' \
#         f'    '
#
#
#
#
message = MIMEMultipart("alternative")
message["Subject"] = f'Situatia Azi {romanaDate}'
message["From"] = sender_email

part1=MIMEText(mesajMail,"plain")
message.attach(part1)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    for receiver in receiver_emails:
        # server.sendmail(sender_email, receiver, message.as_string())


        pass