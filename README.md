# NBA Chatbot

A rule-based regex chatbot that answers questions about basketball and the NBA, built with a Python/Flask backend and a React frontend.

## Stack

- **Backend** — Python, Flask, Gunicorn
- **Frontend** — React (via CDN), served by nginx
- **Infrastructure** — Docker, Docker Compose

## Running it

Make sure Docker Desktop is running, then:
```bash
docker compose up --build
```

Open **http://localhost:3000** in your browser. The first build takes 2–4 minutes; subsequent starts are instant.

To run it in the background:
```bash
docker compose up -d --build
```

To stop it:
```bash
docker compose down
```

## How it works

User input is normalised via a chain of `re.sub` calls (expanding contractions, stripping punctuation), then matched against 56+ regex rules. Each rule's response template uses backreferences (`\1`, `\2`) so the chatbot can echo back the player or team name the user typed. Every response is the product of a `re.sub` substitution, not a static lookup.

## Topics covered

Players, teams, game rules, history, records, stats, and awards.
