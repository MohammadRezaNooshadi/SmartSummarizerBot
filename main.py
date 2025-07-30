import telebot
import os
from telebot import types
from os import environ
from dotenv import load_dotenv
from together import Together
from fpdf import FPDF
from docx import Document
from pypdf import PdfReader

load_dotenv()
token = environ.get("BOT_TOKEN")


def main():
    bot(token, prompt())


def bot(token, prompt):
    user_language = {}
    user_text = {}
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start(message):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("English", callback_data="English"),
            types.InlineKeyboardButton("فارسی", callback_data="Persian"),
            types.InlineKeyboardButton("العربية", callback_data="Arabic"),
            types.InlineKeyboardButton("Español", callback_data="Spanish"),
            types.InlineKeyboardButton("Français", callback_data="French"),
            types.InlineKeyboardButton("Русский", callback_data="Russian"),
        )
        user_name = message.from_user.first_name
        bot.send_message(
            message.chat.id,
            f"Hi {user_name} 👋\nFirst, tell me what language you speak 🌍",
            reply_markup=markup,
        )

    @bot.callback_query_handler(func=lambda call: call.data)
    def language(call):
        language_list = ["English", "Persian", "Arabic", "Spanish", "French", "Russian"]
        if call.data in language_list:
            user_language[call.message.chat.id] = call.data
            bot.send_message(call.message.chat.id, ai(prompt[0],
                                                      None,
                                                      user_language[call.message.chat.id],
                                                      None))  # type: ignore
        elif call.data == "pdf":
            if ltr_language(user_language[call.message.chat.id]):
                path = make_pdf(call.message.chat.id, user_text)
                if not path == False:
                    with open(path, "rb") as f:
                        bot.send_document(call.message.chat.id, f)
                    os.remove(path)
                else:
                    bot.send_message(call.message.chat.id, ai(prompt[4],
                                                              None ,
                                                              user_language[call.message.chat.id],
                                                              call.message.from_user.first_name)) # type: ignore
            else:
                bot.send_message(call.message.chat.id, ai(prompt[3],
                                                          None ,
                                                          user_language[call.message.chat.id],
                                                          call.message.from_user.first_name)) # type: ignore

    @bot.message_handler(content_types=["text", "document"])
    def acho(message):
        if message.content_type == "text":
            markup = types.InlineKeyboardMarkup()
            ai_txt = ai(prompt[1],
                        message.text,
                        user_language[message.chat.id],
                        message.from_user.first_name)
            user_text[message.chat.id] = ai_txt
            markup.add(types.InlineKeyboardButton("Converting to PDF...", callback_data="pdf"))
            bot.reply_to(message, ai_txt, reply_markup=markup)  # type: ignore

        elif message.content_type == "document":
            docx_format = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            pdf_format = "application/pdf"
            if message.document.mime_type == docx_format:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("Converting to PDF...", callback_data="pdf"))
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)  # type: ignore
                os.makedirs("Files", exist_ok=True)

                file_name = f"{message.from_user.id}"
                file_path = os.path.join("Files", file_name)

                with open(file_path, "wb") as f:
                    f.write(downloaded_file)

                ai_txt = ai(prompt[1],
                            docx(file_path),
                            user_language[message.chat.id],
                            message.from_user.first_name)
                user_text[message.chat.id] = ai_txt

                bot.reply_to(message, ai_txt, reply_markup=markup)  # type: ignore
                os.remove(file_path)
            elif message.document.mime_type == pdf_format:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("Converting to PDF...", callback_data="pdf"))
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)  # type: ignore
                os.makedirs("Files", exist_ok=True)

                file_name = f"{message.from_user.id}"
                file_path = os.path.join("Files", file_name)

                with open(file_path, "wb") as f:
                    f.write(downloaded_file)

                txt = pdf(file_path)
                ai_txt = ai(prompt[1], txt, user_language[message.chat.id], message.from_user.first_name)
                user_text[message.chat.id] = ai_txt
                bot.reply_to(message, ai_txt, reply_markup=markup)  # type: ignore
                os.remove(file_path)
            else:
                bot.reply_to(message, ai(prompt[2],
                                         None,
                                         user_language[message.chat.id],
                                         message.from_user.first_name)) # type: ignore
    bot.polling()


def ai(prompt, message=None, language=None, user_name=None):

    client = Together()

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[
            {
                "role": "user",
                "content": f"{prompt} : the message is :{message}  the user name is :{user_name} the language is =>{language}",
            }
        ],
    )
    return response.choices[0].message.content  # type: ignore


def pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.strip()


def docx(path):
    doc = Document(path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def ltr_language(language):
    return language in ["English", "Spanish", "French", "Russian"]


def make_pdf(id, text_dict):
    text = text_dict[id]
    text = text.replace("’", "'").replace("“", '"').replace("”", '"').replace("—", " ")
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=14)
        pdf.multi_cell(0, 10, text)
        file_path = f"Files/{id}.pdf"
        pdf.output(file_path)
    except:
        return False
    else:
        return file_path


def prompt():
    return [
        """Translate and slightly rephrase the following message into the given language.
        Keep it friendly and natural and gen z.
        Use emojis.
        Do not explain anything at all.
        return the version as specifide language:
        'Hey there! drop your text, PDF, or Word file and I’ll handle the rest for you!' """,
        """You will receive a text and the user's preferred language (referred to as "language").
        The specified language appears at the **end** of the input in this format:
        **"the language is => [Language]"**
        (This is not part of the message text itself.)

        ⚠️ Important: The font used to generate the PDF is "Helvetica", which only supports basic Latin characters.
        If the specified language is **not** Persian or Arabic, avoid using characters that fall outside the standard Latin range.
        (You may ignore this warning if the language is Persian or Arabic.)

        Your task:

        → If the message appears to be a **question**, and it’s in the same language as specified:
        → Simply answer the question in language.

        Otherwise:

        1. If the text is written in the same language as the specified language:
        → Summarize it clearly and concisely in language.
        → Highlight the key points or important ideas.

        2. If the text is in a different language:
        → First, translate it smoothly into language, preserving the tone.
        → Then summarize and extract the key points in language.

        3. If the text feels educational or like a lesson:
        → Generate a few thoughtful and relevant questions based on the content, in language.

        Guidelines:
        - Keep the response natural, clear, and user-friendly.
        - Do not explain what you're doing. Only return the final result in language.""",
        """Tell the user that the file they sent is not supported.
        Keep the response natural, clear, and user-friendly.
        Do not explain what you're doing. Only return the final result in language.""",
        """The user's preferred language is provided as language.
        Respond with the following sentence in that language, naturally and politely. You may rephrase it slightly if needed:
        "I'm sorry, I can't generate a PDF in your selected language."
        Do not explain what you're doing. Only return the final result in language.""",
        """The user's preferred language is provided as language.
        Respond with the following sentence in that language, naturally and politely. You may rephrase it slightly if needed:
        "I'm sorry, I can't generate PDF Because of my limitations"
        never explain what you're doing. Only return the final result in language. act like an app"""]


if __name__ == "__main__":
    main()
