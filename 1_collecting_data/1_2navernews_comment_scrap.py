import time
import csv
from selenium import webdriver
import pandas as pd

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1950x1080")


options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("disable-gpu") 


prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=options)

# glob.glob('data/*.csv')

csv_list = ['04190423YTN_null2.csv']

for file_name in csv_list:
    # file_name = "03290331SBS.csv"
    data = pd.read_csv(file_name, index_col=False, header=None)
    data.columns = ['index', 'title', 'date', 'urls']
    # data = data.drop_duplicates(subset=['urls']) 내가 직접 전처리
    # data.to_csv('{03290331SBS}_1.csv', index=False, encoding='utf-8')

    filename = file_name.split('.')[0]+'_comment.csv' #f"03290331SBS_comment.csv"
    f = open(filename, "w", encoding="utf-8-sig", newline="")
    writer = csv.writer(f)

    for url in data['urls']:
        
        #웹 드라이버
        driver.implicitly_wait(30)
        driver.get(url)

        #네이버의 경우, 클린봇으로 추출이 안되는게 있다, 클린봇 옵션 해제 후 추출해주도록 한다.
        cleanbot = driver.find_element_by_css_selector('a.u_cbox_cleanbot_setbutton')
        cleanbot.click()
        time.sleep(1)
        cleanbot_disable = driver.find_element_by_xpath("//input[@id='cleanbot_dialog_checkbox_cbox_module']")
        cleanbot_disable.click()
        time.sleep(1)
        cleanbot_confirm = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[4]/button')
        cleanbot_confirm.click()
        time.sleep(1)

        #더보기 계속 클릭하기
        while True:
            try:
                btn_more = driver.find_element_by_css_selector('a.u_cbox_btn_more')
                btn_more.click()
                # time.sleep(1)
            except:
                break

        #기사제목 추출
        article_head = driver.find_elements_by_css_selector('div.article_info > h3 > a')
        print("기사 제목 : " + article_head[0].text)

        #기사시간 추출
        article_time = driver.find_elements_by_css_selector('div.sponsor > span.t11')
        print("기사 등록 시간 : " + article_time[0].text)

        # # 성비와 연령대 추출
        # per = driver.find_elements_by_css_selector('span.u_cbox_chart_per')
        
        # print("남자 성비 : " + per[0].text)
        # print("여자 성비 : " + per[1].text)
        # print("10대 : " + per[2].text)
        # print("20대 : " + per[3].text)
        # print("30대 : " + per[4].text)
        # print("40대 : " + per[5].text)
        # print("50대 : " + per[6].text)
        # print("60대 이상 : " + per[7].text)

        #댓글추출
        contents = driver.find_elements_by_css_selector('span.u_cbox_contents')
        comment_dates = driver.find_elements_by_css_selector('span.u_cbox_date')

        cnt = 1;
        for content, comment_date in zip(contents, comment_dates):
            writer.writerow([cnt, article_time[0].text, article_head[0].text, comment_date.text, content.text])
            cnt+=1
            # print(cnt, " : ", comment_date.text, content.text)
            # cnt+=1