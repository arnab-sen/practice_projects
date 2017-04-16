"""
This program obtains the results of the NBA Playoffs from Wikipedia,
namely the data from the Bracket section.
"""
import wikipedia
def get_results(html_section, team_key):
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
    colour_key = "#87cefa"
    score_start = html_section.find(colour_key)
    html_section = html_section[score_start + 1:]
    print(html_section)
    score_slice = html_section[score_start : html_section.find("</td>")]
    #print(score_slice)
    #score = html_section[score_start]
    html_section = html_section[score_start:]

    #return [team_name, score, html_section]
    return [""]

data = []
playoffs_2017 = wikipedia.page("2017 NBA Playoffs")
playoffs_2016 = wikipedia.page("Template:2016_NBA_Playoffs")
page_html = playoffs_2016.html()
# Each team name links to their season page, which
# all begin with "2015%E2%80%9316" ("2015-2016"); use this as a key
team_key = "2015%E2%80%9316"
html_section = page_html[page_html.find(team_key):]

get_results(html_section, team_key)

# data is a list of lists
#data += [get_results(html_section, team_key)]
#data += [get_results(data[0][2], team_key)]

#print(data[0][0], data[0][1])
#print(data[1][0], data[1][1])


#print(html_section)
