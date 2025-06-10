import customtkinter as ctk
import openai
import threading
import os
import sys
import uuid
from dotenv import load_dotenv

# .env dosyasından API anahtarını yükle
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# CustomTkinter ayarları
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class KagoAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KagoAI")

        # Uygulama simgesi (EXE yapıldığında da çalışması için)
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        icon_path = os.path.join(base_path, "kagoai.ico")
        self.iconbitmap(icon_path)

        # Pencereyi tam ekran yap ve boyutlandırılabilir ayarla
        self.state('zoomed')
        self.resizable(True, True)

        # Sohbet geçmişi ve mevcut sohbet değişkenleri
        self.chat_history = []  # Tüm sohbetlerin listesi
        self.current_transcript = []  # Mevcut sohbetin mesajları
        self.current_chat_id = None  # Mevcut sohbetin ID'si
        self.chat_row = 0  # Sohbet baloncuklarının satır numarası

        # Sol menü (sidebar)
        self.sidebar = ctk.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        # Logo veya başlık
        logo = ctk.CTkLabel(self.sidebar, text="KagoAI", font=ctk.CTkFont(size=20, weight="bold"))
        logo.pack(padx=10, pady=(10, 5))

        # Yeni Sohbet butonu
        btn_new = ctk.CTkButton(self.sidebar, text="+ Yeni Sohbet", anchor="w",
                                font=ctk.CTkFont(size=18), command=self.new_chat)
        btn_new.pack(fill="x", padx=10, pady=(0, 10))

        # Sohbet geçmişi çerçevesi (kaydırılabilir)
        self.history_frame = ctk.CTkScrollableFrame(self.sidebar, corner_radius=0)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=(5, 0))

        # Ana sohbet alanı
        self.main = ctk.CTkFrame(self, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nswe")
        self.grid_columnconfigure(1, weight=1)  # Ana sütunu genişletilebilir yap
        self.grid_rowconfigure(0, weight=1)  # Ana satırı genişletilebilir yap

        # Ana sohbet başlığı
        header = ctk.CTkLabel(self.main, text="KagoAI", font=ctk.CTkFont(size=22, weight="bold"))
        header.pack(pady=(8, 0))

        # Sohbet baloncuklarının bulunduğu kaydırılabilir çerçeve
        self.chat_container = ctk.CTkScrollableFrame(self.main, corner_radius=0)
        self.chat_container.pack(fill="both", expand=True, padx=(20, 5), pady=(0, 0))
        self.chat_container.grid_columnconfigure(0, weight=1)  # Bot mesajları için sütun
        self.chat_container.grid_columnconfigure(1, weight=1)  # Kullanıcı mesajları için sütun

        # Giriş kutusu ve gönder butonu çerçevesi
        input_frame = ctk.CTkFrame(self.main, height=50, corner_radius=0)
        input_frame.pack(fill="x", side="bottom", padx=20, pady=10)

        # Mesaj giriş kutusu
        self.entry = ctk.CTkEntry(input_frame, placeholder_text="Bir şeyler yaz... ✍️", font=("Segoe UI Emoji", 20))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)
        self.entry.bind("<Return>", lambda e: self.send_message())  # Enter tuşu ile mesaj gönderme

        # Gönder butonu
        ctk.CTkButton(input_frame, text="Gönder 🚀", width=100, font=ctk.CTkFont(size=20),
                      command=self.send_message).pack(side="right", padx=(10, 0), pady=5)

        # Uygulama başladığında yeni bir sohbet başlat
        self.new_chat()

        # Tam ekran uyarısı çerçevesi
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

        # Pencere boyutlandığında tam ekran kontrolünü yap
        self.bind("<Configure>", self._check_fullscreen_status)
        # Başlangıçta da kontrol et
        self.after(100, self._check_fullscreen_status)

    def _check_fullscreen_status(self, event=None):
        """Pencerenin tam ekran (zoomed) olup olmadığını kontrol eder."""
        if self.state() != 'zoomed':
            self.fullscreen_warning_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.sidebar.grid_forget()  # Sidebar'ı gizle
            self.main.grid_forget()  # Ana içeriği gizle
        else:
            self.fullscreen_warning_frame.place_forget()
            self.sidebar.grid(row=0, column=0, sticky="nswe")  # Sidebar'ı göster
            self.main.grid(row=0, column=1, sticky="nswe")  # Ana içeriği göster

    def new_chat(self):
        """Yeni bir sohbet başlatır veya mevcut sohbeti kaydeder."""
        if self.current_transcript and self.current_chat_id:
            # Mevcut sohbeti geçmişe kaydet
            found = False
            for chat in self.chat_history:
                if chat['id'] == self.current_chat_id:
                    chat['messages'] = list(self.current_transcript)
                    found = True
                    break
            # Eğer sohbet geçmişinde yoksa (ilk sohbet veya yeni bir sohbetse) ekle
            if not found and self.current_chat_id:  # current_chat_id var ama history'de yoksa demek ki yeni oluşmuş
                self.chat_history.append({
                    'id': self.current_chat_id,
                    'title': "Başlık Oluşturuluyor...",  # Başlık sonradan belirlenecek
                    'messages': list(self.current_transcript)
                })

        # Sohbet alanını temizle
        for w in self.chat_container.winfo_children():
            w.destroy()

        # Değişkenleri sıfırla
        self.current_transcript = []
        self.current_chat_id = None
        self.chat_row = 0

        # Sohbet geçmişi butonlarını güncelle
        self.update_history_buttons()

    def update_history_buttons(self):
        """Sohbet geçmişi butonlarını günceller."""
        # Mevcut butonları temizle
        for w in self.history_frame.winfo_children():
            w.destroy()

        # Her sohbet için yeni bir buton oluştur
        for chat in reversed(self.chat_history):  # En son sohbet en üstte olsun
            btn = ctk.CTkButton(self.history_frame, text=chat['title'], anchor="w",
                                font=ctk.CTkFont(size=16),
                                command=lambda chat_id=chat['id']: self.load_history(chat_id))
            btn.pack(fill="x", pady=4)

    def load_history(self, chat_id):
        """Belirli bir sohbet geçmişini yükler."""
        if self.current_chat_id == chat_id:  # Zaten yüklüyse bir şey yapma
            return

        # Mevcut sohbeti kaydet (eğer varsa)
        if self.current_transcript and self.current_chat_id:
            for chat in self.chat_history:
                if chat['id'] == self.current_chat_id:
                    chat['messages'] = list(self.current_transcript)  # List() ile kopyalandığından emin ol
                    break

        # Sohbet alanını temizle
        for w in self.chat_container.winfo_children():
            w.destroy()

        # Değişkenleri sıfırla ve yüklenecek sohbeti ayarla
        self.chat_row = 0
        self.current_transcript = []  # Burası önemli, boşaltıyoruz
        self.current_chat_id = chat_id

        loaded_messages = []
        for chat in self.chat_history:
            if chat['id'] == chat_id:
                loaded_messages = chat['messages']
                break

        # Yüklenen mesajları baloncuk olarak ekle
        for sender, text in loaded_messages:
            # Geçmişten yüklendiği için add_bubble içinde transcript'e eklemeyecek
            self.add_bubble(text, sender=sender, is_from_history=True)

        # UI'a ekledikten sonra loaded_messages'ı transcript'e kopyala
        self.current_transcript = list(loaded_messages)  # Kesinlikle kopyala
        self.update_history_buttons()

    def add_bubble(self, text, sender="user", loading=False, is_from_history=False):
        """Sohbet baloncuklarını UI'a ekler."""
        col = 1 if sender == "user" else 0  # Kullanıcı sağda, bot solda
        sticky = "e" if sender == "user" else "w"  # Sağ veya sol hizala
        fg_color = "#d9fdd3" if sender == "user" else "#ffffff"  # Renkleri ayarla
        text_color = "black"

        bubble = ctk.CTkFrame(self.chat_container, corner_radius=10, fg_color=fg_color)
        bubble.grid(row=self.chat_row, column=col, sticky=sticky, padx=10, pady=4)

        label = ctk.CTkLabel(
            bubble,
            text=text,
            font=("Segoe UI Emoji", 16),
            wraplength=600,  # Yazıyı belirli bir genişlikte sar
            justify="left",
            text_color=text_color,
            anchor="w"
        )
        label.pack(padx=12, pady=8, fill="x", anchor="w")

        # Eğer geçmişten yüklenmiyorsa transcript'e ekle
        if not is_from_history:
            self.current_transcript.append((sender, text))

            # İlk mesajda sohbet başlığını oluştur (eğer yeni bir sohbetse)
            if self.current_chat_id is None and sender == "user":
                new_chat_id = str(uuid.uuid4())  # Yeni bir ID oluştur
                temp_title = "Başlık Oluşturuluyor..."
                new_chat_entry = {
                    'id': new_chat_id,
                    'title': temp_title,
                    'messages': list(self.current_transcript)  # İlk mesajı kaydet
                }
                self.chat_history.append(new_chat_entry)
                self.current_chat_id = new_chat_id
                self.update_history_buttons()
                # Başlık oluşturmayı ayrı bir thread'de yap
                threading.Thread(target=self.generate_chat_title, args=(new_chat_id, list(self.current_transcript)),
                                 daemon=True).start()

        self.chat_row += 1  # Sonraki baloncuk için satırı artır
        self.update_idletasks()  # UI'ı hemen güncelle
        self.chat_container._parent_canvas.yview_moveto(1.0)  # En alta kaydır

        return bubble, label  # Baloncuk ve etiketi döndür (stream için lazım)

    def send_message(self):
        """Kullanıcının mesajını gönderir ve AI yanıtını ister."""
        user_text = self.entry.get().strip()
        if not user_text:  # Boş mesaj gönderme
            return

        self.add_bubble(user_text, sender="user")  # Kullanıcı mesajını ekle
        self.entry.delete(0, ctk.END)  # Giriş kutusunu temizle

        # Bot için yükleme balonu ekle
        load_bubble, load_label = self.add_bubble("...", sender="bot")

        # AI yanıtını ayrı bir thread'de çek
        threading.Thread(target=self.fetch_response, args=(user_text, load_bubble, load_label), daemon=True).start()

    def fetch_response(self, user_text, load_bubble, load_label):
        """OpenAI API'den stream modunda yanıt alır."""
        try:
            # API için mesajları hazırla
            messages_for_api = [{"role": "system",
                                 "content": "Sen enerjik, Z kuşağından birisin bana reis, kral gibi konuş, emoji patlatırsın ve senin yapımcın Kağan Kuzu adlı bir çocuk."}]

            # current_transcript'i API için doğru formatta hazırla
            for sender, text in self.current_transcript:
                role = "user" if sender == "user" else "assistant"
                # Yükleme (...) mesajlarını API'ye gönderme, bu önemli!
                if text == "..." and role == "assistant":
                    continue
                messages_for_api.append({"role": role, "content": text})

            full_answer = ""  # Tam cevabı biriktirmek için

            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_for_api,
                temperature=0.7,
                max_tokens=1000,
                stream=True
            )

            for chunk in resp:
                # Delta.content'ın varlığını kontrol et
                if chunk.choices[0].delta and chunk.choices[0].delta.content:
                    content_chunk = chunk.choices[0].delta.content
                    full_answer += content_chunk

                    # UI güncellemesini ana thread'de yap
                    self.after(0, lambda c=content_chunk: self._update_loading_label(c, load_label))

            # Akış bittikten sonra tam cevabı transcript'e kaydet
            self.after(0, lambda a=full_answer: self._finalize_transcript(a))

        except Exception as e:
            error_message = f"Hata oluştu kanki: {e} 😵"
            # Hata durumunda yükleme baloncuğunu hata mesajıyla güncelle
            self.after(0, lambda e_msg=error_message: self._update_ui_with_answer(e_msg, load_bubble, load_label))

    def _update_loading_label(self, chunk, label):
        """Yükleme etiketinin metnine gelen parçayı ekler ve UI'ı günceller."""
        current_text = label.cget("text")
        # Eğer ilk gelen parça ise "..." yazısını kaldırıp direk metni ekle
        if current_text == "...":
            label.configure(text=chunk)
        else:
            label.configure(text=current_text + chunk)
        self.update_idletasks()  # UI'ı hemen güncelle
        self.chat_container._parent_canvas.yview_moveto(1.0)  # En alta kaydır

    def _finalize_transcript(self, final_answer):
        """Akış bittikten sonra transcript'i günceller."""
        # Mevcut transcript'in son elemanı bot'un yükleme mesajı ("...") olmalı
        # veya bot'un önceki cevabı olmalı (eğer streamden gelmiyorsa)
        if self.current_transcript and self.current_transcript[-1][0] == "bot" and self.current_transcript[-1][
            1] == "...":
            self.current_transcript[-1] = ("bot", final_answer)
        else:
            # Bu durum normalde olmamalı ama her ihtimale karşı:
            # Eğer transcript'te son bot mesajı yoksa veya "..." değilse,
            # yeni bir bot mesajı olarak ekle.
            self.current_transcript.append(("bot", final_answer))

        self.update_idletasks()
        self.chat_container._parent_canvas.yview_moveto(1.0)

    def _update_ui_with_answer(self, answer, bubble, label):
        """Hata durumunda veya stream olmayan yanıtlarda UI'ı günceller ve transcript'i yönetir."""
        label.configure(text=answer)

        # Hata mesajıysa veya manuel bir güncelleme ise transcript'i ekle/güncelle
        # Eğer en son mesaj bir bot mesajı ve yükleme ikonu ise onu güncelle
        if self.current_transcript and self.current_transcript[-1][0] == "bot" and self.current_transcript[-1][
            1] == "...":
            self.current_transcript[-1] = ("bot", answer)
        else:
            # Veya direkt yeni bir bot mesajı olarak ekle (hata mesajı gibi)
            self.current_transcript.append(("bot", answer))

        self.update_idletasks()
        self.chat_container._parent_canvas.yview_moveto(1.0)

    def generate_chat_title(self, chat_id, messages_for_title):
        """Sohbet için otomatik başlık oluşturur."""
        try:
            # API için mesajları hazırla (ilk 4 mesajı kullan)
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
            title = title.replace('"', '').replace("'", "")  # Tırnakları temizle

            self.after(0, self._update_chat_title_in_ui, chat_id, title)

        except Exception as e:
            print(f"Başlık oluşturulurken hata oluştu kanki: {e} 😥")
            self.after(0, self._update_chat_title_in_ui, chat_id, "Başlık Oluşturulamadı 😞")

    def _update_chat_title_in_ui(self, chat_id, new_title):
        """Oluşturulan başlığı UI'da günceller."""
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
        self.update_history_buttons()  # Butonları yeniden çiz


# Uygulamayı başlat
if __name__ == "__main__":
    if not openai.api_key:
        print("HATA: OPENAI_API_KEY ortam değişkeni bulunamadı. 🚨")
        print("Lütfen kodla aynı dizinde bir .env dosyası oluşturun ve içine OPENAI_API_KEY='anahtarınız' yazın.")
        print("Örnek: OPENAI_API_KEY='sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'")
    else:
        app = KagoAIApp()
        app.mainloop()
