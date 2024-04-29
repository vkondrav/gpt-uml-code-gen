from pathlib import Path
from openai import OpenAI
import json
import os
from halo import Halo
import requests
import pygame
import warnings
import webbrowser

warnings.filterwarnings("ignore", category=DeprecationWarning)

def output_html(id, line1, line2, image_url):
    with open('output.html', 'w') as f:
        f.write(f"""
            <html>
                <head>
                    <style>
                        body {{
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            font-family: Arial, sans-serif;
                            padding: 0 10%;
                        }}
                        .play-description {{
                            font-size: 1.5em;
                            color: blue;
                            text-align: center;
                        }}
                        .response-play {{
                            font-size: 2em;
                            color: red;
                            text-align: center;
                        }}
                        img {{
                            max-width: 50%;
                            max-height: 50%;
                            height: auto;
                        }}
                    </style>
                </head>
                <body>
                    <p class="play-description">{line1}</p>
                    <p class="response-play">{line2}</p>
                    <img src="{image_url}" alt="Generated image">
                </body>
            </html>
        """
    )

    file_name = f"{id}_output.html"
    file_path = os.path.abspath(file_name)
    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok = True)
    file_path = output / file_name

    webbrowser.open('file://' + file_path)

client = OpenAI(
  api_key = os.getenv("OPEN_AI_KEY")
)

pygame.mixer.init()

event_id = "29232"

play_by_play_url = f"https://api.thescore.com/nhl/events/{event_id}/play_by_play_records"
event_url = f"https://api.thescore.com/nhl/events/{event_id}"

play_by_play_response = requests.get(play_by_play_url)

plays = json.loads(play_by_play_response.text)

event_response = requests.get(event_url)

event = json.loads(event_response.text)

abstract = event['preview_data']['abstract']
headline = event['preview_data']['headline']

prompt = f'''
You are a colour commentator for a hockey game from Sportsnet located in Toronto. 
I will comment on the play as a commentator would.
Try to incorporate what has already happened into each response.
Your response should fairly short as the game is live and ongoing.

Here is some information about the game.

Abstract:
{abstract}

Headline:
{headline}
    '''

print(f"{prompt}")

messages = [{"role": "user", "content": prompt}]

model = "gpt-4-turbo"

spinner = Halo(text = "Generating", spinner = "dots")

for play in plays[:10]:

    play_description = play['description']
    play_id = play['id']

    print(f"{play_description}\n")

    messages.append({"role": "user", "content": play_description})

    response = client.chat.completions.create(
        model = model,
        messages = messages
    )

    response_play = response.choices[0].message.content

    print(f"{response_play}\n")

    messages.append({"role": "assistant", "content": response_play})

    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok=True)
    play_file_path = Path(__file__).parent / "output" / f"play_{play_id}.mp3"

    print(f"{play_file_path}\n")
    
    response = client.audio.speech.create(
        model = "tts-1",
        voice = "alloy",
        input = response_play,
        speed = 1.1
    )

    response.stream_to_file(play_file_path)

    image_prompt = f"""
    Create a photorealistic, clear, and detailed illustration of a key moment in a hockey game.

    - Key moment: {response_play}

    The image should capture the energy and excitement of the game, with dynamic camera angles and close-ups of players.
    """

    response = client.images.generate(
        model = "dall-e-2",
        prompt = image_prompt,
        size = "512x512",
        n = 1,
     )

    image_url = response.data[0].url

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    output_html(play_id, play_description, response_play, image_url)

    pygame.mixer.music.load(play_file_path)
    pygame.mixer.music.play()