import os, json
from googleapiclient.discovery import build
import pandas as pd

test_path = "./test/"
with open(test_path+"secret.json", encoding='utf-8') as f:
    secret = json.load(f)
    api_key = secret['secret_key']

api_key = api_key # 사용자 API key
keywords = ['문재인', '문대통령', '文'] # 검색 Keyword
# 검색 Channel ID
channel_ids = {'YTN':'UChlgI3UHCOnwUGzWzbJ3H5w', 'JTBC':'UCsU-I-vHLiaMfV_ceaYz5rQ', 'SBS':'UCkinYTS9IHqOEwR1Sze2JTw'}
# {Start, End} Period
start_period = ['2021-03-29T00:00:00Z', '2021-04-05T00:00:00Z', '2021-04-12T00:00:00Z', '2021-04-19T00:00:00Z', '2021-04-26T00:00:00Z']
end_period = ['2021-04-01T00:00:00Z', '2021-04-10T00:00:00Z', '2021-04-17T00:00:00Z', '2021-04-24T00:00:00Z', '2021-05-01T00:00:00Z']

# Crawling with Youtube API
api_obj = build('youtube', 'v3', developerKey=api_key)
item_dict = {}
for channel_name, channel_id in channel_ids.items(): # 채널 이름 및 채널널 아이디
    for start, end in zip(start_period, end_period): # 수집 기간
        # 저장 파일 명
        out_file_name = 'Youtube'+'_'+channel_name+'_'+ ''.join(start.split('T')[0].split('-')[1:]) + '_' + ''.join(end.split('T')[0].split('-')[1:])+'_comment.csv'
				# search()
        response = api_obj.search().list(part='snippet',
                                    q=keywords,
                                    channelId=channel_id,
                                    publishedAfter=start,
                                    publishedBefore=end,
                                    maxResults=100).execute()
        for item in response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title'].strip()
            pulish_time = item['snippet']['publishTime']
						# commentThread() 
            response = api_obj.commentThreads().list(part='snippet, replies', videoId=video_id, maxResults=100).execute()
            while response:
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']

                    comment_time = comment['publishedAt']
                    comment_text = comment['textDisplay'].strip()

                    try:
                        item_dict['publish_time'].append(pulish_time)
                        item_dict['title'].append(title)
                        item_dict['comment_time'].append(comment_time)
                        item_dict['comment'].append(comment_text)
                    except:
                        item_dict['publish_time'] = [pulish_time]
                        item_dict['title'] = [title]
                        item_dict['comment_time'] = [comment_time]
                        item_dict['comment'] = [comment_text]

                if 'nextPageToken' in response:
                    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
                else:
                    break

        data = pd.DataFrame.from_dict(item_dict)

        data['publish_time'] = list(map(lambda x:x.split('T')[0], data['publish_time']))
        data['comment_time'] = list(map(lambda x:x.split('T')[0], data['comment_time']))

        target_idx = data['publish_time']==data['comment_time']
        target_data = data.loc[target_idx]

        target_data.to_csv(out_file_name, index=False)