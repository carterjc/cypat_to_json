from bs4 import BeautifulSoup
import requests
import time
import json


backup = {}


def search_terms(div, tier, states, first_team):
    team_page = requests.get("http://scoreboard.uscyberpatriot.org/team.php?team=" + first_team)
    team_soup = BeautifulSoup(team_page.text, 'lxml')
    teamHTML = team_soup.select("tr")[3:]
    comp_year = teamHTML[0].select("td")[0].text.split("_")[1].upper()  # takes first image title and parses it for data
    round = teamHTML[0].select("td")[0].text.split("_")[2]
    backup["search"] = {
        "comp_year": comp_year,
        "round": round,
        "divison": div,
        "states": states,
        "tier": tier
    }
    print("Generated JSON search heading")


def get_teams(divs, tiers, loc):
    main_page = requests.get("http://scoreboard.uscyberpatriot.org/")  # makes initial request, recieves HTML
    soup = BeautifulSoup(main_page.text, 'lxml')
    mainHTML = soup.select("tr")
    global imageNum, backup
    imageNum = int(mainHTML[1].select("td")[5].text)
    lastTeam = int(mainHTML[-1].select("td")[0].text)
    search_terms(divs, tiers, loc, mainHTML[1].select("td")[1].text)
    print("Starting scraping\n\n----\n")
    for i in range(1, len(mainHTML[1:])):
        rank = mainHTML[i].select("td")[0].text
        division = mainHTML[i].select("td")[3].text
        tier = mainHTML[i].select("td")[4].text
        cumulative_score = mainHTML[i].select("td")[11].text
        location = mainHTML[i].select("td")[2].text
        if division in divs or divs[0].lower() == "all":
            if tier in tiers or tiers[0].lower() == "all":
                if location in loc or loc[0].lower() == "all":
                    backup[i - 1] = {}
                    backup[i - 1]["team_num"] = mainHTML[i].select("td")[1].text
                    backup[i - 1]["location"] = location
                    backup[i - 1]["division"] = division
                    backup[i - 1]["tier"] = tier
                    image_data(mainHTML[i].select("td")[1].text, i - 1)
                    backup[i - 1]["play_time"] = mainHTML[i].select("td")[6].text
                    backup[i - 1]["warnings"] = mainHTML[i].select("td")[7].text
                    backup[i - 1]["image_score"] = mainHTML[i].select("td")[8].text
                    backup[i - 1]["adjustments"] = mainHTML[i].select("td")[9].text
                    backup[i - 1]["cisco_score"] = mainHTML[i].select("td")[10].text
                    backup[i - 1]["cumulative_score"] = cumulative_score
                    print("Team " + str(rank) + "/" + str(lastTeam) + "{" + str(round((int(rank) / lastTeam) * 100, 2)) + "%}")
    print("\nFinished grabbing data\n\n----")


def image_data(team_num, index):
    team_page = requests.get("http://scoreboard.uscyberpatriot.org/team.php?team=" + team_num)
    team_soup = BeautifulSoup(team_page.text, 'lxml')
    teamHTML = team_soup.select("tr")[3:]
    scores = []
    for image in teamHTML:
        scores.append(
            (image.select("td")[0].text.split("_")[0], image.select("td")[5].text, image.select("td")[1].text)
        )
        # Name, score, time
    for score in scores:
        backup[index][score[0]] = {"score": score[1], "time": score[2]}
    # Image scoring data
    teamData = team_page.text[team_page.text.find("arrayToDataTable("):team_page.text.find("]);")][:-7] + "]"
    j_info = teamData.partition("ToDataTable(")[2].replace("'", '"')
    json1 = json.loads(j_info)  # formats the data as JSON to be accessed easily
    backup[index]["scoring_data"] = json1
    time.sleep(2)


def output_json(year, round_num):
    print("Writing JSON data to " + str(year) + "r" + str(round_num) + ".txt")
    with open(str(year) + "r" + str(round_num) + ".txt", "w+") as f:
        json.dump(backup, f)


def main():
    print("""
Welcome to cypat_to_json! This program takes the public CyberPatriot scoreboard and scrapes it for all necessary data, 
including individual image data like scores, times, and checks. Be aware, this program does have a long run time,
especially in the earlier rounds.
    """)
    time.sleep(2)
    year = input("What season is it (ex. CPXII)?")
    round_num = input("What round is it (number only?")
    print("\n--\nPossible divisions (write exactly):\nOpen\nAll Service\nMiddle School\n--\n")
    div_search = input("Do you want to sort by division? List any search terms separated by just a comma or write "
                       "'all'.").split(",")
    print("\n--\nPossible tiers (write exactly):\nMiddle School\nSilver\nGold\nPlatinum\n--\n")
    tier_search = input("Do you want to sort by tier? List any search terms separated by just a comma or write "
                        "'all'.").split(",")
    state_search = input("Do you want to sort by location? Enter location abbreviations separated by just a comma or "
                         "write 'all'.").split(",")
    print("\n\n----Program starting---\n")
    # Get data from following functions
    get_teams(div_search, tier_search, state_search)
    output_json(year, round_num)
    print("Program complete")


main()
