from bs4 import BeautifulSoup
import requests
import json
import csv

parsed = ['ChavvlaD-NA1', 'bonescollector-NA1', 'Snooptwin-NA1', 'Discipl-5684', 'koshizuka-1994', 'bagsik-0813', 'McPlayin-NA1', 'EstrelaGalaxia-Ehe', 'Evy%20is%20carried-NA1', 'InstantTwilight-NA1', 'HeiGui%20Neigaer-NA1', 'WhatsUpBJ-8964', 'AMORMENSIS-NA1', 'Captain%20Healthy-NA1', 'Ronkiji-Sun', 'masumi-3060', 'Chuusagi-NA1', 'LaughingAtOnions-NA1', 'Grifter-NA1', 'ParktheShark7-NA1', 'WrathOfR3ptar-NA1', 'Lychabee-NA1', 'LilacCrayon-NA1', 'Shi%20no%20tenshi-Kami', 'heartseeker01-NA1', 'SORRY%20BOUT%20THAT-TURNT', 'Florence-444', '14nicholas14-NA1', 'CrayGoo-NA1', 'ZombiePhoenix-ZP10', 'lKOTB-6137', 'Lotus%20Iroh0-NA1', 'qoochieqlapper-NA1', 'FeatherKuhn-NA1', 'Final%20Boss-NA1', 'DragonDrake-NA1', 'Sierz24-NA1', 'BadAtCollege-9952', 'Zuko%20Ålone-NA1', 'Quippy-NA1', 'DinosLuvMehh-NA1',
          'NurgleDaddy-NA1', 'JohnBadAtGame-NA1', 'VilkasTheBlind-NA1', 'TakeIt2TheRift-NA1', 'skijss-NA1', 'Roogaboo-9035', 'Yukino-Fuki', 'Apostol-NA1', 'redspeed200-NA1', 'JungleMonkey-9409', 'Iko-6281', 'Deontas-6589', 'Pingcapto80ms-NA1', 'Soulstyce-NA1', 'MïlfAndCookïes-NA1', 'Squat%20CEO-NA1', 'sneakpeakjfk-NA1', 'Raigun-NA1', 'cuddlewizard-7252', 'Jeshua-NA1', 'fappinerday-NA1', 'Darth%20Puggles-NA1', 'NA%20PODS-NA1', 'ŚÓÁŹ%20ÉÙìùçØŠœïÖą-8488', 'Mighty%20Soupcan-NA1', 'Nyne%20Tailed%20Fox-NA1', 'Zaidis-NA1', 'To%20Pimp%20A%20Haiiro-NA1', 'TripNapTrip-NA1', 'Charlyarvv%20V2-MYM', 'Cato0-2407', 'Lebrra-NA1', 'Squidmyers33-NA1', 'Rumah-00001', 'IAFKIFUFEED-NA1', 'xXUchihaMadaraXx-NA1', 'LetMeSeeMySon-NA1', 'ZDarkcrest-NA1', 'DJ%20PhantomForce-NA1', 'BlueCore01-NA1', 'Turnandcough4me-NA1', 'kurushadou-NA1']


def run(name):

    headers = {"User-Agent": "PostmanRuntime/7.36.0"}
    page_to_scrape = requests.get(
        "https://www.op.gg/summoners/na/" + name, headers=headers)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    data = soup.find("script", attrs={"id": "__NEXT_DATA__"})
    json_object = json.loads(data.text)

    with open("data.csv", "r") as file:
        line_count = sum(1 for line in file)
    file.close()
    write_file = open("data.csv", 'a', newline='')
    reader = csv.reader(write_file)
    csv_writer = csv.writer(write_file)

    json_stats = ["damage_dealt_to_objectives", "total_damage_taken", "total_damage_dealt_to_champions",
                  "vision_score", "minion_kill", "neutral_minion_kill", "gold_earned", "kill", "death", "assist", "champion_level", "total_heal", "op_score"]
    entry_stats = ["kda", "kill_participation"]
    entry_stats.extend(json_stats)
    game_type = ["NORMAL", "FLEXRANKED", "SOLORANKED"]

    for game in json_object["props"]["pageProps"]["games"]["data"]:
        if game["queue_info"]["game_type"] in game_type and not game["is_remake"]:

            blue_kills = 1 if game["teams"][0]["game_stat"]["kill"] == 0 else game["teams"][0]["game_stat"]["kill"]
            red_kills = 1 if game["teams"][1]["game_stat"]["kill"] == 0 else game["teams"][1]["game_stat"]["kill"]

            time = game["game_length_second"]

            for player in game["participants"]:
                team = player["team_key"]
                stats = player["stats"]
                try:
                    player_name = player["summoner"]["game_name"] + \
                        "-" + player["summoner"]["tagline"]
                    player_name = player_name.replace(" ", "%20")
                    if player_name not in parsed:
                        parsed.append(player_name)
                except Exception:
                    pass

                entry = []
                for column in json_stats:
                    if column != "op_score":
                        entry.append(stats[column]/time)
                    else:
                        entry.append(stats[column])

                if team == "BLUE":
                    entry.insert(
                        0, (stats["kill"] + stats["assist"])/blue_kills * 100)
                else:
                    entry.insert(
                        0, (stats["kill"] + stats["assist"])/red_kills * 100)

                denom = 1 if stats["death"] == 0 else stats["death"]
                entry.insert(0, (stats["kill"] + stats["assist"])/denom)

                if line_count == 0:
                    csv_writer.writerow(entry_stats)
                    line_count += 1
                csv_writer.writerow(entry)
    write_file.close()


if __name__ == "__main__":
    for name in parsed:
        run(name)
