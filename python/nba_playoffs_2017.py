"""
This program obtains the results of the NBA Playoffs from Wikipedia,
namely the data from the Bracket section.
"""
import wikipedia
def get_results(html_section, team_key):
    start = html_section.find(team_key) + len(team_key)
    team_name = html_section[start + 1:]
    #print(team_name)
    underscores = [team_name.find("_"), ""]
    
    #print(team_name[underscores[0] + 1])
    t = team_name[underscores[0] + 1:]
    underscores[1] = underscores[0] + t.find("_")
    team_name = team_name[:underscores[0]] + \
                " " + team_name[underscores[0] + 1: underscores[1] + 1]
    print(team_name)
    
    #print(team_slice)
    #team_name = team_slice[und
    underscores += [team_name[underscores[0] + 1:].find("_")]
    t = team_name[:underscores[0]]
    #print(t)
    t += team_name[underscores[0] + 1 : underscores[1]]
    team_name = t
    
    #print(t)

playoffs_2017 = wikipedia.page("2017 NBA Playoffs")
playoffs_2016 = wikipedia.page("Template:2016_NBA_Playoffs")
page_html = playoffs_2016.html()
# Each team name links to their season page, which
# all begin with "2015%E2%80%9316" ("2015-2016"); use this as a key
team_key = "2015%E2%80%9316"
html_section = page_html[page_html.find(team_key):]
get_results(html_section, team_key)



#print(html_section)
