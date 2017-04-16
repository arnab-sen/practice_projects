"""
This program obtains the results of the NBA Playoffs from Wikipedia,
namely the data from the Bracket section.
"""
import wikipedia
def get_results(html_section, team_key, colour_key):
    # Get team name
    start = html_section.find(team_key) + len(team_key)
    html_section = html_section[start + 1:]
    team_name = html_section
    underscores = [team_name.find("_"), ""]
    t = team_name[underscores[0] + 1:]
    underscores[1] = underscores[0] + t.find("_")
    team_name = team_name[:underscores[0]] + \
                " " + team_name[underscores[0] + 1: underscores[1] + 1]

    # Get team series score e.g. Cleveland Cavaliers 4
    # Use the background colour of the bracket box
    # as the key to find the score
    score_start = html_section.find(colour_key)
    html_section = html_section[score_start + len(colour_key) + 4:]
    #print(html_section)
    if html_section[0] == "<":
        score = html_section[3]
        html_section = html_section[4:]
    else:
        score = html_section[0]
        html_section = html_section[1:]
    #print(score)

    return [team_name, score], html_section

data = []
playoffs_2017 = wikipedia.page("2017 NBA Playoffs")
playoffs_2016 = wikipedia.page("Template:2016_NBA_Playoffs")
page_html = playoffs_2016.html()
# Each team name links to their season page, which
# all begin with "2015%E2%80%9316" ("2015-2016"); use this as a key
team_key = "2015%E2%80%9316"
html_section = page_html[page_html.find(team_key):]

#get_results(html_section, team_key, colour_key)

# data is a list of lists
# Get Eastern Conference results
colour_key = "#87cefa"
for i in range(15):
    d, html_section = get_results(html_section, team_key, colour_key)
    data += [d]

# Get Western Conference results
colour_key = "#ffaeb9"
for i in range(15):
    d, html_section = get_results(html_section, team_key, colour_key)
    data += [d]

#print(data[0][0], data[0][1])
#print(data[1][0], data[1][1])
for i in data: 
    print(i)
    #pass


#print(html_section)
