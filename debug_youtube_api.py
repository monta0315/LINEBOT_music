from apiclient.discovery import build

YOUTUBE_API_KEY = "AIzaSyDWbuxE3tzF4RMnCjC045fPy5Cp9GYRHXM"

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

#必要なもの
#動画の画像，動画のタイトル，動画の概要欄の文言，

def hello_world():
    List=[]
    search_response = youtube.search().list(
        part='snippet',
        q="ヒステリックナイトガール",
        order="relevance",
        type='video',
    ).execute()
    for i in range(len(search_response['items'])):
        result_dict = {
            "image": search_response["items"][i]["snippet"]['thumbnails']["default"]["url"],
            "title": search_response["items"][i]["snippet"]["title"],
            "description": search_response["items"][i]["snippet"]['description'],
            "actions": {
                "label": "動画を視聴する",
                "videoURL": search_response["items"][i]["id"]["videoId"],
            }
        }
        List.append(result_dict)
    print(List)

if __name__ == "__main__":
    hello_world()
