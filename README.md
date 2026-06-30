# TrendAnalyzer

Web dashboard that allows analytics of Mastodon social media platform. 

## :star: Functional requirements

- See hashtag popularity in current moment and over time.
- See hashtag sentiments (% of positive/neutral/negative posts with this hashtag) over some period of time.
- Dashboard with top 10 most popular hashtags over some period of time.
- Get most popular posts with given hashtag over some period of time.
- Track posts that are being added in real time that contain given hashtag.
- Get the correlated tags to the searched for
- See the percentages of languages for the searched posts
---

## Prerequisites

### Python 3.10+

Check if you have it:
```bash
python3 --version
```

If not, download from [python.org](https://www.python.org/downloads/) or use your system package manager:
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv

# macOS (Homebrew)
brew install python
```

### Node.js and npm

Check if you have them:
```bash
node --version
npm --version
```

If not, the easiest way is **nvm** (Node Version Manager):
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Restart your terminal, then install Node
nvm install --lts
```

Alternatively, download the installer directly from [nodejs.org](https://nodejs.org/).

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd TrendAnalyzer
```

### 2. Backend

```bash
cd app
python3 -m venv venv
source venv/bin/activate        
# Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend

```bash
cd frontend
npm install
```

---

## Running the project

You need **three terminals** running simultaneously.

### Terminal 1 — Streaming worker (fills the database)

The worker connects to Mastodon and saves public posts to a local SQLite database. It requires a Mastodon account on [techhub.social](https://techhub.social)

```bash
cd app
source venv/bin/activate
cd workers
python streaming_api_worker.py
```

On run it will:
1. Register the app on the Mastodon instance
2. Print an OAuth URL — open it in your browser
3. Authorize the app and paste the code it gives you back into the terminal

After that it starts streaming all public posts and saving them. Leave it running.

### Terminal 2 — Backend API

```bash
cd app
source venv/bin/activate
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.  

### Terminal 3 — Frontend

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000` in your browser.
