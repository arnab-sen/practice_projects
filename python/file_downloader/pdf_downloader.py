"""
A simple script to download pdf files from given urls
"""

import urllib.request

def retrieve_pdf(url):
	with urllib.request.urlopen(url) as file:
		final = url.rfind("/")
		file_name = url[final + 1:]
		print(file_name)
		with open(file_name, "wb") as pdf:
			pdf.write(file.read())


def main():
	lectures = input("Enter the lecture numbers: ")
	#lectures = list("789")
	#print(lectures)
	lectures = lectures.split()
	with open("url_base.txt", "r") as f:
		base_url = f.read()
		#print(base_url)
	for lecture in lectures:
		if len(lecture) < 2:
			lecture = "0" + lecture
		url = base_url + lecture + ".pdf"
		#print(url)
		retrieve_pdf(url)

if __name__ == "__main__":
	main()
