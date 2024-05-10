import random
import tkinter as tk
from openai import OpenAI
import os

client = OpenAI(
  api_key = os.getenv("OPEN_AI_KEY")
)

teams = ["iOS", "Android", "Backend", "Platform", "QA", "Product", "Design"]

def get_random_team():
    if teams:
        random_team = random.choice(teams)
        teams.remove(random_team)
        team_label.config(text=random_team)
        remaining_teams_label.config(text=f"Remaining teams: {', '.join(teams)}")
        get_joke(random_team)
    else:
        team_label.config(text="List is complete. Exiting program.")
        button.config(state='disabled')

def get_joke(team):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Tell me a funny joke about the {team} software engineering team. Should in the style of Seinfield standup",
        temperature=0.5,
        max_tokens=300
    )
    joke_label.config(text=response.choices[0].text.strip())

def display_team():
    random_team = random.choice(teams)
    teams.remove(random_team)
    team_label.config(text=random_team)
    remaining_teams_label.config(text=f"Remaining teams: {', '.join(teams)}")

root = tk.Tk()
root.title("SeekR Standup")
root.geometry("500x300")

remaining_teams_label = tk.Label(root, text=f"Remaining teams: {', '.join(teams)}")
remaining_teams_label.pack(pady=20)

team_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), bg="yellow", fg="blue")
team_label.pack(pady=20)

joke_label = tk.Label(root, text="", wraplength=300)
joke_label.pack(pady=20)

button = tk.Button(root, text="Next Team", command=get_random_team)
button.pack(pady=20)

root.mainloop()