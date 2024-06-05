from pytube import YouTube
import sys

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    sys.stdout.write(f"\rDownloading... {int(percentage_of_completion)}%")
    sys.stdout.flush()

def download_video(video_url, download_path):
    try:
        yt = YouTube(video_url, on_progress_callback=progress_function)
        stream = yt.streams.get_highest_resolution()
        print(f'Downloading: {yt.title}')
        stream.download(output_path=download_path)
        print('\nDownload completed!')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    video_url = input('Enter the YouTube video URL: ')
    download_path = input('Enter the download path: ')
    download_video(video_url, download_path)
