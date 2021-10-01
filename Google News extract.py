from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import csv
import os
import time as t
start = t.time()
PERIOD_OF_TIME = 10
Stock = "Bharti+Airtel"
Stocks_list = ["Mahindra+and+Mahindra","CEAT+tyres","HCL+Technologies","JK+Cement"]
while True:
    mycsv = open('data.csv', 'w')
    fieldnames = ['Time_stamp','Stock', 'Title', 'Description', 'Time', 'Link']
    writer = csv.DictWriter(mycsv, fieldnames=fieldnames)
    writer.writeheader()

    link = "https://www.google.com/search?q=" + Stock + "+share+news&rlz=1C5CHFA_enIN902IN903&tbs=sbd:1,qdr:d&tbm=nws&sxsrf=ALeKk00VV_0Ac60LQjOzg8gQKPem2bV8pA:1609864757179&source=lnt&sa=X&ved=0ahUKEwi-qvPHnYXuAhX-zzgGHbpeB40QpwUIKA&biw=1440&bih=701&dpr=2"
    req = Request(link, headers={'user-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    with requests.session() as c:
        soup = BeautifulSoup(webpage,'html5lib')
        #print(soup)
        for item in soup.find_all('div',attrs={'class': 'ZINbbc xpd O9g5cc uUPGi'}):
            raw_link = (item.find('a',href=True)['href'])
            link = (raw_link.split("/url?q=")[1]).split('&sa=U&')[0]
            #print(item)
            Desc = item.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).get_text()
            time = Desc.split(" · ")[0]
            description = Desc.split(" · ")[1]
            description = description.replace(",", "")
            title = item.find('div',attrs={'class':'BNeawe vvjwJb AP7Wnd'}).get_text()
            title = title.replace(",","")
            #print(title)
            #print(description)
            #print(time)
            #print(link)
            writer.writerow({'Time_stamp':t.ctime(start),'Stock':Stock.replace("+"," "),'Title':title,'Description':description,'Time':time,'Link':link})
        mycsv.close()

    for additional_stocks in Stocks_list:
        link = "https://www.google.com/search?q=" + additional_stocks + "+share+news&rlz=1C5CHFA_enIN902IN903&tbs=sbd:1,qdr:d&tbm=nws&sxsrf=ALeKk00VV_0Ac60LQjOzg8gQKPem2bV8pA:1609864757179&source=lnt&sa=X&ved=0ahUKEwi-qvPHnYXuAhX-zzgGHbpeB40QpwUIKA&biw=1440&bih=701&dpr=2"
        req = Request(link, headers={'user-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        with requests.session() as c:
            soup = BeautifulSoup(webpage,'html5lib')
            #print(soup)
            for item in soup.find_all('div',attrs={'class': 'ZINbbc xpd O9g5cc uUPGi'}):
                raw_link = (item.find('a',href=True)['href'])
                link = (raw_link.split("/url?q=")[1]).split('&sa=U&')[0]
                #print(item)
                Desc = item.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).get_text()
                time = Desc.split(" · ")[0]
                description = Desc.split(" · ")[1]
                description = description.replace(",", "")
                title = item.find('div',attrs={'class':'BNeawe vvjwJb AP7Wnd'}).get_text()
                title = title.replace(",","")
                #print(title)
                #print(description)
                #print(time)
                #print(link)
                mycsv = open('data.csv','a')
                mycsv.write("{},{},{},{},{},{} \n".format(t.ctime(start),additional_stocks.replace("+"," "),title,description,time,link))
            mycsv.close()


    import smtplib
    import mimetypes
    from email.mime.multipart import MIMEMultipart
    from email import encoders
    from email.message import Message
    from email.mime.audio import MIMEAudio
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.text import MIMEText

    emailfrom = "saikrishna0716@gmail.com"
    emailto = "saikrishna0716@gmail.com"
    fileToSend = "data.csv"
    username = "saikrishna0716@gmail.com"
    password = "Svallur@1935"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Latest stock news"
    #msg.preamble = "help I cannot send an attachment to save my life"

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
    t.sleep(20)
    if t.time() > start + PERIOD_OF_TIME : break