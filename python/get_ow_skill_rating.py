"""
This repeatedly polls the Overwatch website once per given
time period for a player's skill rating, and logs the skill rating
if it has changed from the previous entry.
Currently for PC only.
"""
import urllib.request
import os
import ast
import datetime
from bs4 import BeautifulSoup

def get_user_info():
    battletag = input("Enter your battletag: ")
    url = "https://playoverwatch.com/en-us/career/pc/us/" + battletag
    return url

def get_html(url, form):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")

    if form == "messy": return soup
    if form == "neat": return soup.prettify()
    if form == "text": return soup.get_text()
    else:
        raise Exception("Incorrect form argument in get_html(url, form)")

def file_exists(file_path):
    if os.path.isfile(file_path): return True
    else: return False

def write_string_to_file(content, filename, directory):
    # Make a directory folder if it doesn't already
    # exist, then save a text file to that folder
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + "\\" + filename, "w") as file:
        file.write(content)
        
def get_skill_rating(html):
    sr = html.find("div", "u-align-center h6")
    skill_rating = get_data_between_tags(sr)
    
    return int(skill_rating)

def get_data_between_tags(tagged_data):
    t = str(tagged_data)
    
    return t[t.find(">") + 1 : t.find("</")]

def get_date_and_time(country, city):
    country = country.strip().lower()
    space = country.find(" ")
    country = country[:space] + "-" + country[space + 1:]
    city = city.strip().lower()
    url = "https://www.timeanddate.com/worldclock/" + country + "/" + city
    html = get_html(url, "messy")
    span_classes = list(html.find_all("span"))
    for i in span_classes:
        i = str(i)
        if "h1" in i: time = get_data_between_tags(i)
        if "ctdat" in i: date = get_data_between_tags(i)
        
    return time + " " + date
    
def main():
    url = get_user_info()
    page_html = get_html(url, "messy")
    skill_rating = get_skill_rating(page_html)
    country = input("Enter country: ")
    city = input("Enter city: ")
    time = get_date_and_time(country, city)
    print(time + "\n" + "Skill Rating: " + str(skill_rating))

if __name__ == "__main__":
    main()
