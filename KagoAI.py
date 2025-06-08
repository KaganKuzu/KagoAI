import customtkinter as ctk
import openai
import threading
import os
import sys
import uuid
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class KagoAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KagoAI")

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        icon_path = os.path.join(base_path, "kagoai.ico")
        self.iconbitmap(icon_path)

        self.state('zoomed')
        self.resizable(True, True)

        self.chat_history = []
        self.current_transcript = []
        self.current_chat_id = None
        self.chat_row = 0

        self.sidebar = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        logo = ctk.CTkLabel(self.sidebar, text="KagoAI", font=ctk.CTkFont(size=20, weight="bold"))
        logo.pack(padx=10, pady=(10, 5))

        btn_new = ctk.CTkButton(self.sidebar, text="+ Yeni Sohbet", anchor="w",
                                font=ctk.CTkFont(size=18), command=self.new_chat)
        btn_new.pack(fill="x", padx=10, pady=(0, 10))

        self.history_frame = ctk.CTkScrollableFrame(self.sidebar, corner_radius=0)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=(5, 0))

        self.main = ctk.CTkFrame(self, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nswe")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        header = ctk.CTkLabel(self.main, text="KagoAI", font=ctk.CTkFont(size=22, weight="bold"))
        header.pack(pady=(8, 0))

        self.chat_container = ctk.CTkScrollableFrame(self.main, corner_radius=0)
        self.chat_container.pack(fill="both", expand=True, padx=(20, 5), pady=(0, 0))
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.chat_container.grid_columnconfigure(1, weight=1)

        input_frame = ctk.CTkFrame(self.main, height=50, corner_radius=0)
        input_frame.pack(fill="x", side="bottom", padx=20, pady=10)

        self.entry = ctk.CTkEntry(input_frame, placeholder_text="Bir şeyler yaz... ✍️", font=("Segoe UI Emoji", 20))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)
        self.entry.bind("<Return>", lambda e: self.send_message())

        ctk.CTkButton(input_frame, text="Gönder 🚀", width=100, font=ctk.CTkFont(size=20),
                      command=self.send_message).pack(side="right", padx=(10, 0), pady=5)

        self.new_chat()

        self.fullscreen_warning_frame = ctk.CTkFrame(self, fg_color="red", corner_radius=0)
        self.fullscreen_warning_label = ctk.CTkLabel(
            self.fullscreen_warning_frame,
            text="""BU UYGULAMA EKRANI KAPLA
MODUNDA ÇALIŞIR! 
(üstteki kareye tıkla.)""",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="white"
        )
        self.fullscreen_warning_label.pack(expand=True, padx=20, pady=20)

        self.bind("<Configure>", self._check_fullscreen_status)
        self.after(100, self._check_fullscreen_status)

    def _check_fullscreen_status(self, event=None):
        if self.state() != 'zoomed':
            self.fullscreen_warning_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.sidebar.grid_forget()
            self.main.grid_forget()
        else:
            self.fullscreen_warning_frame.place_forget()
            self.sidebar.grid(row=0, column=0, sticky="nswe")
            self.main.grid(row=0, column=1, sticky="nswe")

    def new_chat(self):
        if self.current_transcript and self.current_chat_id:
            found = False
            for chat in self.chat_history:
                if chat['id'] == self.current_chat_id:
                    chat['messages'] = list(self.current_transcript)
                    found = True
                    break

        for w in self.chat_container.winfo_children():
            w.destroy()

        self.current_transcript = []
        self.current_chat_id = None
        self.chat_row = 0

        self.update_history_buttons()

    def update_history_buttons(self):
        for w in self.history_frame.winfo_children():
            w.destroy()

        for chat in reversed(self.chat_history):
            btn = ctk.CTkButton(self.history_frame, text=chat['title'], anchor="w",
                                font=ctk.CTkFont(size=16),
                                command=lambda chat_id=chat['id']: self.load_history(chat_id))
            btn.pack(fill="x", pady=4)

    def load_history(self, chat_id):
        if self.current_chat_id == chat_id:
            return

        if self.current_transcript and self.current_chat_id:
            for chat in self.chat_history:
                if chat['id'] == self.current_chat_id:
                    chat['messages'] = list(self.current_transcript)
                    break

        for w in self.chat_container.winfo_children():
            w.destroy()

        self.chat_row = 0
        self.current_transcript = []
        self.current_chat_id = chat_id

        loaded_messages = []
        for chat in self.chat_history:
            if chat['id'] == chat_id:
                loaded_messages = chat['messages']
                break

        for sender, text in loaded_messages:
            self.add_bubble(text, sender=sender, is_from_history=True)

        self.current_transcript = list(loaded_messages)
        self.update_history_buttons()

    def add_bubble(self, text, sender="user", loading=False, is_from_history=False):
        col = 1 if sender == "user" else 0
        sticky = "e" if sender == "user" else "w"
        fg_color = "#d9fdd3" if sender == "user" else "#ffffff"
        text_color = "black"

        bubble = ctk.CTkFrame(self.chat_container, corner_radius=10, fg_color=fg_color)
        bubble.grid(row=self.chat_row, column=col, sticky=sticky, padx=10, pady=4)

        label = ctk.CTkLabel(
            bubble,
            text=text,
            font=("Segoe UI Emoji", 16),
            wraplength=600,
            justify="left",
            text_color=text_color,
            anchor="w"
        )
        label.pack(padx=12, pady=8, fill="x", anchor="w")

        if not is_from_history:
            self.current_transcript.append((sender, text))

            if self.current_chat_id is None and sender == "user":
                new_chat_id = str(uuid.uuid4())
                temp_title = "Başlık Oluşturuluyor..."
                new_chat_entry = {
                    'id': new_chat_id,
                    'title': temp_title,
                    'messages': list(self.current_transcript)
                }
                self.chat_history.append(new_chat_entry)
                self.current_chat_id = new_chat_id
                self.update_history_buttons()
                threading.Thread(target=self.generate_chat_title, args=(new_chat_id, list(self.current_transcript)),
                                 daemon=True).start()

        self.chat_row += 1
        self.update_idletasks()
        self.chat_container._parent_canvas.yview_moveto(1.0)

        return bubble, label

    def send_message(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.add_bubble(user_text, sender="user")
        self.entry.delete(0, ctk.END)

        load_bubble, load_label = self.add_bubble("...", sender="bot")

        threading.Thread(target=self.fetch_response, args=(user_text, load_bubble, load_label), daemon=True).start()

    def fetch_response(self, user_text, load_bubble, load_label):
        try:
            messages_for_api = [{"role": "system",
                                 "content": "Sen enerjik, Z kuşağından birisin bana reis, kral gibi konuş, emoji patlatırsın ve senin yapımcın Kağan Kuzu adlı bir çocuk ve kullandığın yapay zeka modeli KagoAI v1."}]

            for sender, text in self.current_transcript:
                role = "user" if sender == "user" else "assistant"
                if text == "..." and role == "assistant":
                    continue
                messages_for_api.append({"role": role, "content": text})

            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_for_api,
                temperature=0.7,
                max_tokens=1000
            )
            answer = resp.choices[0].message.content.strip()
            self.after(0, self._update_ui_with_answer, answer, load_bubble, load_label)
        except Exception as e:
            error_message = f"Hata oluştu kanki: {e} 😵"
            self.after(0, self._update_ui_with_answer, error_message, load_bubble, load_label)

    def _update_ui_with_answer(self, answer, bubble, label):
        label.configure(text=answer)

        if self.current_transcript and self.current_transcript[-1][1] == "...":
            self.current_transcript[-1] = ("bot", answer)

        self.update_idletasks()
        self.chat_container._parent_canvas.yview_moveto(1.0)

    def generate_chat_title(self, chat_id, messages_for_title):
        try:
            api_messages = [{"role": "user" if s == "user" else "assistant", "content": t}
                            for s, t in messages_for_title[:4]]

            title_prompt = [
                {"role": "system",
                 "content": "Sen sohbetleri özetleyen bir yapay zekasın. Sana verilen sohbet metnini tek bir cümleyle, kısa, öz, anlaşılır ve akılda kalıcı, sohbetin ana konusunu belirten bir başlık olarak özetle. Başlık kesinlikle anlamlı bir cümle olsun ve 20 karakteri geçmemeye çalışsın. Yanıtın sadece başlık olsun, başka hiçbir şey olmasın. Örnek: 'Yapay Zeka Nedir?' veya 'Kediler Hakkında Sohbet'"},
                *api_messages
            ]

            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=title_prompt,
                temperature=0.7,
                max_tokens=15
            )

            title = resp.choices[0].message.content.strip()
            title = title.replace('"', '').replace("'", "")

            self.after(0, self._update_chat_title_in_ui, chat_id, title)

        except Exception as e:
            print(f"Başlık oluşturulurken hata oluştu kanki: {e} 😥")
            self.after(0, self._update_chat_title_in_ui, chat_id, "Başlık Oluşturulamadı 😞")

    def _update_chat_title_in_ui(self, chat_id, new_title):
        MAX_UI_TITLE_LENGTH = 28

        cleaned_title = new_title.replace('"', '').replace("'", "").strip()

        if len(cleaned_title) > MAX_UI_TITLE_LENGTH:
            final_title = cleaned_title[:MAX_UI_TITLE_LENGTH - 3] + "..."
        else:
            final_title = cleaned_title

        for chat in self.chat_history:
            if chat['id'] == chat_id:
                chat['title'] = final_title
                break
        self.update_history_buttons()


if __name__ == "__main__":
    if not openai.api_key:
        print("HATA: OPENAI_API_KEY ortam değişkeni bulunamadı. 🚨")
        print("Lütfen kodla aynı dizinde bir .env dosyası oluşturun ve içine OPENAI_API_KEY='anahtarınız' yazın.")
        print("Örnek: OPENAI_API_KEY='sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'")
    else:
        app = KagoAIApp()
        app.mainloop()
