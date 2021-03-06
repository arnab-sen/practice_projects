"""
This program obtains the results of the NBA Playoffs from Wikipedia,
namely the data from the Bracket section.
"""
import wikipedia

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
    
    print_results = True
    if print_results:
        print("----------------First Round----------------")
        for i in range(len(first_round)):
            print(first_round[i][0][0] + ": " + first_round[i][0][1], end = " | ")
            print(first_round[i][1][0] + ": " + first_round[i][1][1])
            if i == 3: print() 
        print("\n-----------Conference Semifinals-----------")
        for i in range(len(conf_semi)):
            print(conf_semi[i][0][0] + ": " + conf_semi[i][0][1], end = " | ")
            print(conf_semi[i][1][0] + ": " + conf_semi[i][1][1])
            if i == 1: print() 
        print("\n-------------Conference Finals--------------")
        for i in range(len(conf_finals)):
            print(conf_finals[i][0][0] + ": " + conf_finals[i][0][1], end = " | ")
            print(conf_finals[i][1][0] + ": " + conf_finals[i][1][1])
            if i == 0: print() 
        print("\n-----------------NBA Finals----------------")
        print(nba_finals[0][0] + ": " + nba_finals[0][1], end = " | ")
        print(nba_finals[1][0] + ": " + nba_finals[1][1])

def get_alternate_team_key(team_key):
    # This is required for instances where the hyperlink
    # for the team has e.g. "2014-15" rather than
    # "2014%E2%80%9315"
    return team_key[0 : 4] + "-" + team_key[-2:]

def get_results(html_list, team_key, colour_key):
    # This function will extract match results
    # and return the html_list with those
    # results removed

    # Get team name   
    for i in range(len(html_list)):
        if colour_key in html_list[i]:            
            index = i
            break
        else: index = 0

    team_name = html_list[index]
    html_list = html_list[index + 1:]

    # Get score
    for i in range(len(html_list)):
        #print(html_list[i])
        if colour_key in html_list[i]:            
            index = i
            break
        else: index = 0         
            
    score = html_list[index]
    html_list = html_list[index + 1:]
    alternate_team_key = get_alternate_team_key(team_key)

    if team_key in team_name:
        team_name, score = clean_data(team_name, score, team_key, colour_key)
        return [team_name, score], html_list
    elif alternate_team_key in team_name:
        team_name, score = clean_data(team_name, score,\
                                      alternate_team_key, colour_key)
        return [team_name, score], html_list
    else: return ["TBD", "-"], html_list

def check_name(key, team_name, full_name):
    if key in team_name: team_name = full_name
    return team_name

def clean_data(team_name, score, team_key, colour_key):
    # Extract team name
    # Check for a team name with more than two words
    t = check_name("Lakers", team_name, "Los Angeles Lakers")
    t = check_name("Clippers", t, "Los Angeles Clippers")
    t = check_name("Portland", t, "Portland Trail Blazers")
    t = check_name("Thunder", t, "Oklahoma City Thunder")
    t = check_name("Golden", t, "Golden State Warriors")
    t = check_name("Spurs", t, "San Antonio Spurs")
    t = check_name("Pelicans", t, "New Orleans Pelicans")
    t = check_name("Knicks", t, "New York Knicks")
    t = check_name("Jersey", t, "New Jersey Nets")
                   
    if t != team_name:
        team_name = t
    else:
        start = team_name.find(team_key) + len(team_key)
        team_name = team_name[start + 1:]
        underscores = [team_name.find("_"), ""]
        temp = team_name[underscores[0] + 1:]
        underscores[1] = underscores[0] + temp.find("_")
        u = underscores
        t = team_name
        team_name = t[:u[0]] + " " + t[u[0] + 1: u[1] + 1]
        
    # Extract score
    start = score.find(colour_key)
    score = score[start + len(colour_key) + 4:]
    if score[0] == "<": score = score[3]
    else: score = score[0]
    
    return team_name, score

def get_page():
    # Get the raw HTML from the bracket template page
    year = input("Enter year (2001+): ")
    print()
    if year == "" or int(year) < 2001:
        print("There was an error with your input.")
        print("2017 will be the year by default.\n")    
        year = "2017"
    try:
        playoffs = wikipedia.page("Template:" + year + "_NBA_Playoffs")
    except:
        print("There was an error with your input.")
        print("2017 will be the year by default.\n")
        year = "2017"
        playoffs = wikipedia.page("Template:" + year + "_NBA_Playoffs")
        
    previous_year = str(int(year) - 1)
    year_short = year[-2:]
    team_key = previous_year + "%E2%80%93" + year_short
    page_html = playoffs.html()
    
    return page_html, team_key

def get_all_results(html_list, team_key):
    data = []
    colour_key = "#87cefa" # Eastern conference
    for i in range(30):
        if i == 15: colour_key = "#ffaeb9" # Western conference
        d, html_list = get_results(html_list, team_key, colour_key)
        data += [d]
         
    return organise_results(data)

def main():
    while(1):
        page_html, team_key = get_page()
        html_section = page_html
        start = html_section.find("<td height=\"7\">")
        html_section = html_section[start:]
        html_list = html_section.split("</td>")
        
        get_all_results(html_list, team_key)
        restart = input("\nWould you like to enter another year? (y/n): ")
        if restart.lower() != "y": break

main()
