# 🧠 Software Engineering Tweet Assistant

A production-ready AI application that helps **software engineers** generate **high-quality, professional tweets** related strictly to **software development and engineering**.

The app focuses on **clarity, correctness, and usability**, and is designed to be **safe to release publicly** without incurring external platform costs.

---

## ✨ What This App Does

* Generates **EXACTLY 10 short tweets** (≤280 characters) for unverified X accounts
* Generates **1 long-form tweet** suitable for a verified-style post
* Enforces **strict software-engineering–only content**
* Prevents abusive, illegal, political, or non-technical topics
* Allows users to:

  * 📋 Copy tweets to clipboard
  * 🚀 Open X (Twitter) compose screen
  * 💬 Send tweets to WhatsApp (native app on mobile)
* Fully **mobile-friendly**
* Zero dependency on X APIs, OAuth, or billing

---

## 🏗️ Architecture Overview

The app follows **clean, layered architecture** with clear separation of concerns:

```
UI (Gradio)
 └── Input validation & UX state
Agent layer
 └── Business logic (tweet generation rules)
Tools
 ├── OpenAI interaction
 ├── Input validation
 ├── Tweet parsing & constraints
 └── Platform helpers (clipboard / WhatsApp)
```

This makes the app:

* Easy to extend
* Easy to test
* Safe to deploy publicly

---

## 📁 Project Structure

```
.
├── app.py                     # Gradio UI + client-side JS actions
├── agent.py                   # Agent orchestration (business logic)
│
├── prompts/
│   └── tweet_prompt.py        # Strict software-only prompts
│
├── tools/
│   ├── tweet_generator.py     # OpenAI Responses API calls
│   ├── tweet_validator.py     # 280-char enforcement
│   ├── input_validator.py     # Software-only & safety checks
│
├── config/
│   └── settings.py            # Environment config
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧠 Design Principles

### 1. **Software Engineering Only**

The app **refuses** to generate content outside:

* Software development
* Programming languages
* Architecture
* Performance
* System design
* DevOps
* Testing

If a user enters anything else, they receive a **clear, user-friendly error message**.

---

### 2. **Safety First**

Input validation blocks:

* Abuse / hate
* Illegal activity
* Politics
* Finance / trading
* Medical advice
* NSFW content

Validation happens **before** any OpenAI call.

---

### 3. **No External Platform Risk**

The app does **not**:

* Post directly to X
* Use X OAuth
* Consume X API credits
* Incur billing risk

Users remain fully in control of posting.

---

### 4. **Mobile-First Usability**

* Responsive Gradio UI
* Native app deep-linking:

  * WhatsApp opens WhatsApp app
  * X opens X app
* Clipboard operations via user interaction

---

## 🚀 How Tweet Generation Works

### Short Tweets

* Prompt enforces **EXACTLY 10 tweets**
* Output format is strictly numbered (`1.` → `10.`)
* Robust parsing extracts tweets reliably
* Tweets are validated to be ≤280 characters

### Long Tweet

* Single, detailed, professional tweet
* Suitable for longer posts or threads

---

## 🧩 Key Files Explained

### `prompts/tweet_prompt.py`

* Enforces:

  * Software-only scope
  * Exact tweet count
  * No emojis / hashtags
  * Professional tone
* Prevents prompt drift

---

### `tools/input_validator.py`

Guards user input **before AI invocation**.

Example rejection:

> “Please enter a topic related to software development (e.g. Java, system design, performance).”

---

### `agent.py`

Acts as the **agent boundary**:

* UI does not talk to OpenAI directly
* Business logic is centralized
* Easy to extend with scoring, ranking, or retries

---

### `app.py`

* Gradio UI
* UX state management (button enable/disable)
* Client-side JavaScript for:

  * Clipboard copy
  * Opening X
  * Opening WhatsApp

> Any browser interaction is handled via `js=` callbacks, which is the correct Gradio pattern.

---

## 🔧 Running Locally

### Prerequisites

* Python 3.10+
* `uv` (recommended) or `pip`
* OpenAI API key

### Environment Setup

Create `.env` (local only):

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

Install dependencies:

```bash
uv sync
```

Run the app:

```bash
uv run python app.py
```

Open:

```
http://localhost:7860
```

---

## ☁️ Deploying on Hugging Face Spaces

1. Push code to the Space repo
2. Add secrets:

**Space → Settings → Secrets**

```
OPENAI_API_KEY
```

3. Restart the Space

Your app will be available at:

```
https://<username>-<space-name>.hf.space
```

No further configuration required.

---

## 📱 Mobile Behavior

| Action           | Mobile Result              |
| ---------------- | -------------------------- |
| Copy & Open X    | Opens X app (if installed) |
| Send to WhatsApp | Opens WhatsApp app         |
| Clipboard        | Works via user interaction |
| UI               | Responsive                 |

---

## 🧪 UX Safeguards Implemented

* Generate buttons disabled until input exists
* Copy / WhatsApp buttons disabled until content exists
* No empty actions possible
* Clear visual feedback

---

## 🛡️ Security & Repo Hygiene

* No secrets committed
* `.env` ignored
* `__pycache__/` and `.pyc` ignored
* No user data stored
* No third-party auth

---

## 🔮 Possible Extensions

* Character counter per tweet
* Tweet quality scoring
* Thread auto-splitting
* Regenerate individual tweet
* Save drafts
* Dark mode
* Analytics dashboard

---

## 📜 License

This project is intended as a **developer tool / reference implementation**.
Choose an appropriate license (MIT / Apache 2.0) based on your distribution needs.

---

## 🙌 Final Notes

This app is designed to be:

* Safe to publish
* Easy to maintain
* Professional in output
* Respectful of platform policies
* Pleasant to use on desktop and mobile
