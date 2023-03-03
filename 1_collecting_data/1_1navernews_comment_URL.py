from bs4 import BeautifulSoup
import csv
from urllib.parse import quote, quote_plus
import requests
from bs4 import BeautifulSoup

# 여론조사 날짜
# 3월 5주차 : 0329-0331
# 4월 1주차 : 0405-0409
# 4월 2주차 : 0412-0416
# 4월 3주차 : 0419-0423
# 4월 4주차 : 0426-0430

s_mm = "04" # start month
s_dd = "26" # start day
e_mm = "04" # end month
e_dd = "30" # end day

# channel 'YTN' news URL 
filename = f"{s_mm}{s_dd}{e_mm}{e_dd}YTN.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

cnt = 1
max_page=40
for i in range(0, max_page):
    num_content = i*10 + 1
    url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%E6%96%87%20%7C%20%EB%AC%B8%EC%9E%AC%EC%9D%B8%20%7C%20%EB%AC%B8%EB%8C%80%ED%86%B5%EB%A0%B9&sort=0&photo=0&field=0&pd=3&ds=2021.{}.{}&de=2021.{}.{}&mynews=1&office_type=1&office_section_code=2&news_office_checked=1052&nso=so:dd,p:from2021{}{}to2021{}{},a:all&start={}".format(s_mm,s_dd,e_mm,e_dd,s_mm,s_dd,e_mm,e_dd, num_content)
    res = requests.get(url)
    res.raise_for_status() # returns an HTTPError object if an error has occurred during the process. (not 200 Okay)
    soup = BeautifulSoup(res.text, "lxml")

    comment_urls = soup.find_all("div", attrs={"class":"news_area"})
    # print(len(comment_urls))
    

    for comment_url in comment_urls:
        
        title = comment_url.find("a",attrs={"class":"news_tit"}).get_text().strip() 
        date = comment_url.select_one("div.news_wrap.api_ani_send > div > div.news_info > div.info_group > span").get_text()
        link = comment_url.select_one("div > div > div.news_info > div > a:nth-child(3)")["href"]

        # print(cnt," : ", link[:37] + "m_view=1&includeAllCount=true&" + link[38:] )
        writer.writerow([cnt, title, date, link[:37] + "m_view=1&includeAllCount=true&" + link[38:]])
        cnt+=1

# JTBC

filename = f"{s_mm}{s_dd}{e_mm}{e_dd}JTBC.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

cnt = 1
max_page=40
for i in range(0, max_page):
    num_content = i*10 + 1
    url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%AC%B8%EC%9E%AC%EC%9D%B8%20%7C%20%EB%AC%B8%EB%8C%80%ED%86%B5%EB%A0%B9%20%7C%20%E6%96%87&sort=0&photo=0&field=0&pd=3&ds=2021.{}.{}&de=2021.{}.{}&cluster_rank=50&mynews=1&office_type=1&office_section_code=2&news_office_checked=1437&nso=so:r,p:from2021{}{}to2021{}{},a:all&start={}".format(s_mm,s_dd,e_mm,e_dd,s_mm,s_dd,e_mm,e_dd,num_content)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    comment_urls = soup.find_all("div", attrs={"class":"news_area"})
    # print(len(comment_urls))
    

    for comment_url in comment_urls:
        title = comment_url.find("a",attrs={"class":"news_tit"}).get_text().strip() 
        date = comment_url.select_one("div.news_wrap.api_ani_send > div > div.news_info > div.info_group > span").get_text()
        link = comment_url.select_one("div > div > div.news_info > div > a:nth-child(3)")["href"]

#         print(cnt," : ", link[:37] + "m_view=1&includeAllCount=true&" + link[38:] )
#         cnt+=1
        writer.writerow([cnt, title, date, link[:37] + "m_view=1&includeAllCount=true&" + link[38:]])
        cnt+=1


# SBS

filename = f"{s_mm}{s_dd}{e_mm}{e_dd}SBS.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

cnt = 1
max_page=40
for i in range(0, max_page):
    num_content = i*10 + 1
# for i in range(0, 6):
    url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%AC%B8%EC%9E%AC%EC%9D%B8%20%7C%20%EB%AC%B8%EB%8C%80%ED%86%B5%EB%A0%B9%20%7C%20%E6%96%87&sort=0&photo=0&field=0&pd=3&ds=2021.{}.{}&de=2021.{}.{}&cluster_rank=24&mynews=1&office_type=1&office_section_code=2&news_office_checked=1055&nso=so:r,p:from2021{}{}to2021{}{},a:all&start={}".format(s_mm,s_dd,e_mm,e_dd,s_mm,s_dd,e_mm,e_dd,num_content)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    comment_urls = soup.find_all("div", attrs={"class":"news_area"})
    # print(len(comment_urls))
    

    for comment_url in comment_urls:
        title = comment_url.find("a",attrs={"class":"news_tit"}).get_text().strip() 
        date = comment_url.select_one("div.news_wrap.api_ani_send > div > div.news_info > div.info_group > span").get_text()
        # link = comment_url.select_one("div > div > div.news_info > div > a:nth-child(3)")["href"]
        link = comment_url.select_one("div > div > div.news_info > div.info_group > a:nth-child(3)")["href"]

        # print(cnt," : ", link[:37] + "m_view=1&includeAllCount=true&" + link[38:] )
        # cnt+=1
        writer.writerow([cnt, title, date, link[:37] + "m_view=1&includeAllCount=true&" + link[38:]])
        cnt+=1