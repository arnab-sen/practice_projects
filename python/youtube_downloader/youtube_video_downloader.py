"""A simple video downloader extending pytube
"""

import pytube

class YT(pytube.YouTube):
	def __init__(self, url):
		super().__init__(url)

	def on_progress(self, bytes_received, file_size, start = None):
		download_progress = round(100 * bytes_received / file_size, 2)
		print("Progress: {}%".format(download_progress))
		if download_progress == 100.0:
			print("Download complete!")

def download(url):
        yt = YT(url)
        video = yt.get_videos()[3]
        video.download("Downloads", on_progress = yt.on_progress)

def main():
        urls = input("Enter video urls separated by a space: ").split()
        for i, url in enumerate(urls):
                print("Downloading video {}/{}".format(i + 1, len(urls)))
                download(url)

if __name__ == "__main__":
        main()
