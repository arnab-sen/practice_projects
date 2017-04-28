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
import time
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
    # "a" rather than "w" so the txt file is added to
    # rather than overwritten
    with open(directory + "\\" + filename, "a") as file:
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
        
    return time, date

def show_menu():
    print("1. Manual\n2. Auto")
    choice = input("Enter your choice: ")
    if choice == "1": choice = 1
    elif choice == "2": choice = 2
    else: choice = 1
    return choice
    
def main():
    choice = show_menu()
    country = input("Enter country: ")
    city = input("Enter city: ")
    current_time, date = get_date_and_time(country, city)
    filename = "sr_log.txt"
    directory = "OW SR Logs"
    write_string_to_file("--- " + date + " ---" + "\n\n", filename, directory)
    url = get_user_info()
    clock_cycle = 900 # seconds to wait
    page_html = get_html(url, "messy")
    skill_rating = get_skill_rating(page_html)
    previous_sr = skill_rating
    current_sr = previous_sr
    starting_sr_message = "Starting SR: " + str(current_sr) + "\n"
    write_string_to_file(starting_sr_message, filename, directory)
    print("Starting SR:", current_sr)
    
    #test_sr = []
    while(1):
    #for sr in test_sr:
        print("Checking...", end = "")
        page_html = get_html(url, "messy")
        skill_rating = get_skill_rating(page_html)
        #skill_rating = sr
        if skill_rating != previous_sr:
            current_sr = skill_rating
            sr_difference = current_sr - previous_sr
            if sr_difference < 0:
                diff_text = " (" + str(sr_difference) + ")"
            else:
                diff_text = " (+" + str(sr_difference) + ")"

            previous_sr = current_sr
            current_time, date = get_date_and_time(country, city)
            message = current_time + ": " + str(current_sr) + diff_text + "\n"
            write_string_to_file(message, filename, directory)
            #print(time + "\n" + "Skill Rating: " + str(skill_rating))
            print(message)
        else:
            print(" no change")
        print()
        if choice == 1:
            input("Press enter to check again")
        elif choice == 2:
            time.sleep(clock_cycle)
        else:
            print("Unexpected break")
            break

if __name__ == "__main__":
    main()
