from apiclient.discovery import build

YOUTUBE_API_KEY = "AIzaSyDWbuxE3tzF4RMnCjC045fPy5Cp9GYRHXM"

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def hello_world():
    search_response = youtube.search().list(
        part='snippet',
        q="ヒステリックナイトガール",
        order="viewCount",
        type='video',
    ).execute()
    reply_video = search_response["items"][0]["id"]["videoId"]
    print("https://youtu.be/"+reply_video)
    #print(video_thumbnails)

hello_world()
