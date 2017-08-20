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

#url = input("Enter video url: ")
url = ""
yt = YT(url)
videos = yt.get_videos()

for i, video in enumerate(videos):
	print(i, video)

videos[0].download("Downloads", on_progress = yt.on_progress)