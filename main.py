import pandas as pd
from googleapiclient.discovery import build
Api_key = 'AIzaSyCsvjWJrWlLj_hdhAcFOtHchEfbsJfQUV8'
Channel_id = ["UCzxp40xFweF9Vik3lLA03zg",]

api_service_name = "youtube"
api_version = "v3"


# Get credentials and create an API client

youtube = build(
    api_service_name, api_version, developerKey=Api_key)

def Channel_info(youtube,Channel_id):
    all_data = []
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id= ",".join(Channel_id)
    )
    response = request.execute()

    for item in response["items"]:
        data = {
            "channelName" : item["snippet"]["title"],
            "subscribers" : item["statistics"]["subscriberCount"],
            "views": item["statistics"]["viewCount"],
            "totalViews": item["statistics"]["viewCount"],
            "playlistId" : item["contentDetails"]["relatedPlaylists"]["uploads"]

        }
        all_data.append(data)
        return pd.DataFrame(all_data)


channel_status = Channel_info(youtube,Channel_id)
print(channel_status)

playlistId = "UUzxp40xFweF9Vik3lLA03zg"

def videoId(youtube,playlistId):
    allVideoId = []


    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId= playlistId,
        maxResults=100
    )

    response = request.execute()

    next_page_token = response.get("nextPageToken")

    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlistId,
            maxResults=100,
            pageToken = next_page_token
        )

        response = request.execute()

        for item in response["items"]:
            allVideoId.append(item["contentDetails"]["videoId"])

        next_page_token = response.get("nextPageToken")
    return allVideoId

video_ids = videoId(youtube,playlistId)

print(len(video_ids))




def videos_information(youtube,video_ids ):
    all_video_info = []

    for i in range(0,len(video_ids),50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_ids[i:i+50]
        )
        response = request.execute()

        for video in response["items"]:
            stats_to_keep = {
                "snippet": ["channelTitle", "title", "description", "tags", "publishedAt"],
                "statistics": ["viewCount", "likeCount", "favouriteCount", "commentCount"],
                "contentDetails": ["duration", "definition", "caption"]
            }
            video_info = {}
            video_info['video_id'] = video["id"]



            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)

    return pd.DataFrame(all_video_info)


video_df = videos_information(youtube,video_ids )
# print(video_df)

video_df.to_excel('C:\\Users\\ishita mishra\\Desktop\\Projects\\videoData.xlsx', index=False)

















