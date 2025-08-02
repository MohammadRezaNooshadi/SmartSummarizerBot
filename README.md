# Summarify

An AI-powered Telegram bot that reads user input (text or files), summarizes it, translates it, or generates smart questions — all in six languages. Powered by the DeepSeek-V3 model via the Together API, this multilingual assistant brings natural interaction, document handling, and PDF export into one seamless chatbot experience.

---

## ✨ Features

- 🧠 AI-powered responses (DeepSeek-V3 via Together API)
- 📝 Accepts plain text, PDFs, and Word documents
- 🌍 Multilingual support: English, Persian, Arabic, Spanish, French, Russian
- 📌 Smart summarization, Q&A generation, and translation
- 📤 Converts responses to downloadable PDF files
- 📲 User-friendly interface with inline language selection

---

## 📁 Project Files

### `main.py`
- Core logic: handles Telegram API via `telebot`
- Processes text and documents
- Integrates AI API
- Generates responses and PDF outputs
- Manages language selection and session states

### `requirements.txt`
Python dependencies:
- `pyTelegramBotAPI`
- `python-dotenv`
- `together`
- `fpdf`
- `python-docx`
- `pypdf`

### `.env` (Not Included)
- Contains environment variables, e.g.:
  - `BOT_TOKEN` (Telegram bot token)

### `Files/` (Runtime only)
- Temporary folder to store:
  - Uploaded files
  - Generated PDFs

---

## 🧩 Design Choices and Challenges

### Language Support
- RTL support (Persian, Arabic) included
- PDF generation currently limited to LTR languages due to font issues with FPDF
- Bot gracefully handles unsupported cases with friendly messages

### AI Integration
- Together’s DeepSeek-V3 API used for efficient, dynamic responses
- Prompts adapted based on input type and language

### Document Handling
- PDFs parsed with `pypdf`
- Word docs parsed with `python-docx`
- Clean error handling for file parsing issues

### UX Focus
- Language selection via inline keyboard
- Emoji-enhanced responses for friendly tone
- Always acknowledges user actions (feedback-first)

### Security
- Secrets like bot token loaded from `.env` using `python-dotenv`
- No hardcoded credentials

---

## 📚 Summary

SmartSummarizerBot (AI Language Bot) is a real-world implementation of AI in messaging — blending natural language processing, file I/O, and multi-language support into an accessible Telegram interface. It prioritizes clean architecture, secure handling of data, and useful interaction design for global users.

> Making content simpler, smarter, and multilingual — straight from your chat window. 🌐📄💬
