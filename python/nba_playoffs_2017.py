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

def organise_results(data):
    first_round = [""] * 8
    conf_semi = [""] * 4
    conf_finals = [""] * 2
    nba_finals = [""]

    # Group data into matches
    matches = [""] * 15
    match_index = 0
    for i in range(30):
        if i % 2 == 0:
            matches[i // 2] = [data[i], data[i + 1]]
    #for i in range(len(matches)): print(i, matches[i])

    # Get first round matches (0, 2, 4, ... 14)
    for i in range(15):
        if i % 2 == 0: first_round[i // 2] = matches[i]

    # Get conference semifinal matches (1, 5, 9, 13)
    for i in range(15):
        if i == 0: conf_semi[i] = matches[i]
        elif (i - 1) % 4 == 0: conf_semi[(i - 1) // 4] = matches[i]

    # Get conference finals matches (3, 11)
    conf_finals[0] = matches[3]
    conf_finals[1] = matches[11]

    # Get nba finals match (7)
    nba_finals = matches[7]
    
    print("First Round:")
    for i in first_round: print(i)
    print("\nConference Semifinals:")
    for i in conf_semi: print(i)
    print("\nConference Finals:")
    for i in conf_finals: print(i)
    print("\nNBA Finals:")
    print(nba_finals)
        
            

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

organise_results(data)
#print(data)
#print(data[0][0], data[0][1])
#print(data[1][0], data[1][1])
count = 0

for i in data:
    #if count % 2 == 0: print()
    #print(i)
    count += 1
    #pass


#print(html_section)

"""
ISSUES:
- Team names only show the first two words, which is fine for
  e.g. Cleveland Cavaliers, but for the Clippers, their team
  name comes up as "Los Angeles" rather than "Los Angeles
  Clippers" -- write a function that shortens all team
  names to their respective acronyms (e.g. CLE, LAC, GS)
"""
