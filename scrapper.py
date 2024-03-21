from bs4 import BeautifulSoup
import requests
import warnings
import re

warnings.filterwarnings('ignore')

# pokemonArr = ['Sprigatito', 'Floragato', 'Meowscarada', 'Fuecoco', 'Crocalor', 'Skeledirge', 'Quaxly', 'Quaxwell', 'Quaquaval', 'Lechonk', 'Oinkologne', 'Tarountula', 'Spidops', 'Nymble', 'Lokix', 'Pawmi', 'Pawmo', 'Pawmot', 'Tandemaus', 'Maushold', 'Fidough', 'Dachsbun', 'Smoliv', 'Dolliv', 'Arboliva', 'Squawkabilly', 'Nacli', 'Naclstack', 'Garganacl', 'Charcadet', 'Armarouge', 'Ceruledge', 'Tadbulb', 'Bellibolt', 'Wattrel', 'Kilowattrel', 'Maschiff', 'Mabosstiff', 'Shroodle', 'Grafaiai', 'Bramblin', 'Brambleghast', 'Toedscool', 'Toedscruel', 'Klawf', 'Capsakid', 'Scovillain', 'Rellor', 'Rabsca', 'Flittle', 'Espathra', 'Tinkatink', 'Tinkatuff', 'Tinkaton',
#               'Wiglett', 'Wugtrio', 'Bombirdier', 'Finizen', 'Palafin', 'Varoom', 'Revavroom', 'Cyclizar', 'Orthworm', 'Glimmet', 'Glimmora', 'Greavard', 'Houndstone', 'Flamigo', 'Cetoddle', 'Cetitan', 'Veluza', 'Dondozo', 'Tatsugiri', 'Annihilape', 'Clodsire', 'Farigiraf', 'Dudunsparce', 'Kingambit', 'Great_Tusk', 'Scream_Tail', 'Brute_Bonnet', 'Flutter_Mane', 'Slither_Wing', 'Sandy_Shocks', 'Iron_Treads', 'Iron_Bundle', 'Iron_Hands', 'Iron_Jugulis', 'Iron_Moth', 'Iron_Thorns', 'Frigibax', 'Arctibax', 'Baxcalibur', 'Gimmighoul', 'Gholdengo', 'Wo-Chien', 'Chien-Pao', 'Ting-Lu', 'Chi-Yu', 'Roaring_Moon', 'Iron_Valiant', 'Koraidon', 'Miraidon', 'Walking_Wake', 'Iron_Leaves']

# pokemonArr = ["Maschiff"]
pokemonArr = [
    "Dipplin",
    "Poltchageist",
    "Sinistcha",
    "Okidogi",
    "Munkidori",
    "Fezandipiti",
    "Ogerpon",
    "Archaludon",
    "Hydrapple",
    "Gouging Fire",
    "Raging Bolt",
    "Iron Boulder",
    "Iron Crown",
    "Terapagos",
    "Pecharunt",
]
df = []

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())

for pokemon in pokemonArr:
    URL = f"https://bulbapedia.bulbagarden.net/wiki/{pokemon}_(Pokémon)"
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[-1])
    browser.get(URL)
    page = requests.get(URL, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Pokedex
    pokeDexResult = soup.find_all("a", attrs={"title": "List of Pokémon by National Pokédex number"})
    pokeDex = int(pokeDexResult[1].get_text().replace("#", ""))

    # Typings
    typeResult = soup.find_all("a", attrs={"title": re.compile(r"[A-Za-z]+ \(type\)$")})
    type1 = typeResult[0].get_text()
    type2 = typeResult[1].get_text()
    if type2 == "Unknown":
        type2 = ""

    # Color
    # pokeDexColorHeader = soup.find('span', text="Pokédex color")
    # print(pokeDexColorHeader.parent.parent.parent.parent.find_all("span")[1])

    # Abilities
    hiddenAbilityHeader = soup.find('small', text=re.compile(r"Hidden Ability"))
    if hiddenAbilityHeader.parent.get("style") == "display: none":
        hiddenAbility = ""
    else:
        hiddenAbility = hiddenAbilityHeader.parent.find_all("span")[0].get_text()
    abilityArr = hiddenAbilityHeader.parent.parent.find_all("td")[0].get_text().strip().split("\xa0or ")
    if len(abilityArr) > 1:
        ability1 = abilityArr[0]
        ability2 = abilityArr[1]
    else:
        ability1 = abilityArr[0]
        ability2 = ""

    # Height
    heightHeader = soup.find('td', text=re.compile(r"\d+(\.\d+)? m"))
    height = float(heightHeader.get_text().replace(" m", ""))
    if height.is_integer():
        height = int(height)

    # Weight
    weightHeader = soup.find('td', text=re.compile(r"\d+(\.\d+)? kg"))
    weight = float(weightHeader.get_text().replace(" kg", ""))
    if weight.is_integer():
        weight = int(weight)

    # HP
    HPHeader = soup.find('span', text="HP")
    HP = int(HPHeader.parent.parent.parent.find_all("div")[1].get_text())

    # Attack
    AttackHeader = soup.find('span', text="Attack")
    Attack = int(AttackHeader.parent.parent.parent.find_all("div")[1].get_text())

    # Defense
    DefenseHeader = soup.find('span', text="Defense")
    Defense = int(DefenseHeader.parent.parent.parent.find_all("div")[1].get_text())

    # Sp. Atk
    SpAtkHeader = soup.find('span', text="Sp. Atk")
    SpAtk = int(SpAtkHeader.parent.parent.parent.find_all("div")[1].get_text())

    # Sp. Def
    SpDefHeader = soup.find('span', text="Sp. Def")
    SpDef = int(SpDefHeader.parent.parent.parent.find_all("div")[1].get_text())

    # Speed
    SpeedHeader = soup.find('span', text="Speed")
    Speed = int(SpeedHeader.parent.parent.parent.find_all("div")[1].get_text())

    # Total
    TotalHeader = soup.find('div', text=re.compile(r"Total"))
    Total = int(TotalHeader.parent.find_all("div")[1].get_text())

    df.append(
        [
            pokeDex,
            1,
            int(str(pokeDex) + "1"),
            pokemon,
            type1,
            type2,
            "COLOR",
            ability1,
            ability2,
            hiddenAbility,
            9,
            0,
            0,
            height,
            weight,
            HP,
            Attack,
            Defense,
            SpAtk,
            SpDef,
            Speed,
            Total,
        ]
    )
    print(pokemon)

import pandas as pd

data = pd.DataFrame(df)
data.to_csv("test.csv", index=False, sep=",")
