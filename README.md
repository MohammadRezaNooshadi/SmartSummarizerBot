# SmartSummarizerBot

**** is a Telegram chatbot designed to interact with users in multiple languages and intelligently process textual content using AI.

---

## ✨ Features

- 🧠 AI-powered responses (DeepSeek-V3 via Together API)
- 📝 Supports plain text, PDFs, and Word documents
- 🌍 Multilingual: English, Persian, Arabic, Spanish, French, Russian
- 📌 Summarize, translate, or answer questions from text
- 📤 Convert responses into downloadable PDF files
- 📲 User-friendly interface with inline language selector

---

## 📁 Project Structure

### `main.py`
- Core bot logic
- Handles Telegram interactions via `telebot`
- Manages user sessions and message types
- Extracts text from `.pdf` and `.docx` files
- Interfaces with AI model for dynamic responses
- Generates PDFs from output (with language compatibility checks)

### `requirements.txt`
Python dependencies:
- `pyTelegramBotAPI`
- `python-dotenv`
- `together`
- `fpdf`
- `python-docx`
- `pypdf`

### `.env` (Not Included)
Environment variables for secure configuration:
- `BOT_TOKEN` (Telegram bot token)

### `Files/`
- Temporary runtime folder
- Stores uploaded files and generated PDFs before cleanup

---

## 🧩 Design Highlights

- **Multilingual Support:**  
  UI and content handling for six languages including RTL scripts. Users choose language via keyboard.

- **AI Integration:**  
  Smart prompt logic tailors responses by language and task (summary, Q&A, translation).

- **Document Parsing:**  
  PDF and DOCX support using `pypdf` and `python-docx` for robust text extraction.

- **PDF Export Limitations:**  
  Due to font constraints (e.g., FPDF + Helvetica), the bot informs users if RTL script PDF generation isn't supported.

- **Security:**  
  Secrets handled securely via `.env` and `python-dotenv`.

- **UX:**  
  Emoji-rich, friendly bot responses and intuitive language selection.

---

## 🚀 Future Improvements

- ✅ Advanced PDF rendering for RTL support (custom fonts)
- ✅ Voice message + multimodal input support
- ✅ Context-aware AI responses
- ✅ Smarter file cleanup & storage management

---

## 📚 Summary

AI Language Bot merges natural language processing, multilingual interaction, and file handling into a single Telegram bot. It showcases secure, scalable bot development with modern AI capabilities using Python.

> Bridging language gaps and making content smarter—one message at a time. 🌍💬

