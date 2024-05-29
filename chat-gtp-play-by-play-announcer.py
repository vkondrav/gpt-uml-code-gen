from string import Template
from pathlib import Path
from openai import OpenAI
import json
import os
from halo import Halo
import pygame
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

def output_html(id, line1, line2):

    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok=True)

    file_name = f"output/output.html"

    with open('data/template.html', 'r') as template_file:
        template = Template(template_file.read())

    with open(file_name, "w") as f:
        f.write(template.substitute(line1=line1, line2=line2))

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

pygame.mixer.init()

def get_plays():
    with open("data/leafs-bruins-game-7.json", "r") as f:
        data = json.load(f)

    plays = []

    for period in data["periods"]:
        for event in period["events"]:
            if event["event_type"] != "substitution":
                plays.append(
                    f"Period: {period['number']} | Clock: {event['clock']} | {event['description']}"
                )

    return plays

plays = get_plays()

def get_roster(team):
    with open(f"data/{team}-roster.json", "r") as f:
        data = json.load(f)

    roster = [player["full_name"] for player in data["players"]]
    roster_string = "\n".join(roster)

    return roster_string

leafs_roster_string = get_roster("leafs")

bruins_roster_string = get_roster("bruins")

def get_preview():
    with open("data/preview-article.txt", "r") as f:
        preview_content = f.read()

    return preview_content

preview_content = get_preview()

prompt = f"""
You are a colour commentator for an NHL hockey game. 
You will comment on the play as a commentator would.
Try to incorporate what has already happened into each response.
Your response should be very short as the game is live and ongoing.

Here is some information about the game.

Preview:
{preview_content}

Leafs Roster:
{leafs_roster_string}

Bruins Roster:
{bruins_roster_string}
    """

messages = [{"role": "user", "content": prompt}]

model = "gpt-4o"

spinner = Halo(text="Generating", spinner="dots")

output_html(0, "Sports Radar Raw Data", "Chat GPT generated commentary")

for play_number, play in enumerate(plays, start=1):

    print(f"{play}\n")

    messages.append({"role": "user", "content": play})

    response = client.chat.completions.create(model=model, messages=messages)

    response_play = response.choices[0].message.content

    print(f"{response_play}\n")

    messages.append({"role": "assistant", "content": response_play})

    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok=True)
    play_file_path = Path(__file__).parent / "output" / f"play_{play_number}.mp3"

    print(f"{play_file_path}\n")

    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=response_play, speed=1.1
    )

    response.stream_to_file(play_file_path)

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    output_html(play_number, play, response_play)

    pygame.mixer.music.load(play_file_path)
    pygame.mixer.music.play()