from pytube import Playlist

def download_youtube_playlist(playlist_url, download_path='./'):
    # Create a Playlist object
    playlist = Playlist(playlist_url)

    print(f'Downloading: {playlist.title}')

    # Loop through all videos in the playlist
    for video in playlist.videos:
        print(f'Downloading {video.title}')
        video.streams.get_highest_resolution().download(download_path)
        print(f'Finished downloading {video.title}')

if __name__ == "__main__":
    # Replace with the URL of the YouTube playlist you want to download
    playlist_url = 'https://www.youtube.com/playlist?list=PL7XUl73Bqi2OkprVOtCm976UdtfujiKTS'
    # Replace with the directory where you want to save the downloaded videos
    download_path = './downloads'
    
    download_youtube_playlist(playlist_url, download_path)
