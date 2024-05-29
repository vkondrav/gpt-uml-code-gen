import random
import tkinter as tk
from openai import OpenAI
import os

client = OpenAI(
  api_key = os.getenv("OPEN_AI_KEY")
)

teams = {
    "iOS": ["Igar", "Alex", "Jonathan", "Deep", "Chloe"],
    "Android": ["Rachit", "Naz", "Shubham", "Steven", "Ivan"],
    "Backend": ["MarcAndre", "Nishad", "Firas", "Chris", "Abdullah"],
    "Platform": ["Harpeet", "Arshdeep"],
    "QA": ["Ravi", "Gurdeep"],
    "Design": ["Tori"]
}

def get_random_team():
    if teams:
        random_team = random.choice(list(teams.keys()))
        team_names = teams.pop(random_team)
        print(f"{random_team}: {', '.join(team_names)}")  # print to console
        team_label.config(text=f"{random_team}: {', '.join(team_names)}")
        remaining_teams_label.config(text=f"Remaining teams: {', '.join(teams.keys())}")
        get_joke(random_team)
    else:
        team_label.config(text="List is complete. Exiting program.")
        button.config(state='disabled')

def get_joke(team):

    prompt = f"Tell me a funny joke about the {team} software engineering team in the style of Seinfield standup. Should be short."

    messages = [{"role": "user", "content": prompt}]

    model = "gpt-3.5-turbo"

    response = client.chat.completions.create(model=model, messages=messages).choices[0].message.content

    joke_label.config(text=response.strip())

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