import os
import threading
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel

from youtube_downloader import YouTubeDownloader

Builder.load_string('''
<Content>:
    orientation: "vertical"
    padding: "20dp"
    spacing: "20dp"

    MDLabel:
        text: "YouTube Downloader"
        font_style: "H4"
        halign: "center"
        size_hint_y: None
        height: "50dp"

    MDTextField:
        id: url_field
        hint_text: "Collez l'URL YouTube ici"
        icon_right: "youtube"
        size_hint_x: None
        width: "350dp"
        pos_hint: {"center_x": 0.5}

    MDBoxLayout:
        size_hint_x: None
        width: "350dp"
        pos_hint: {"center_x": 0.5}
        spacing: "10dp"

        MDLabel:
            text: "Format:"
            size_hint_x: None
            width: "60dp"

        MDRaisedButton:
            id: btn_mp4
            text: "MP4 (Vidéo)"
            size_hint_x: 0.5
            md_bg_color: app.theme_cls.primary_color if root.format_mp4 else [0.5, 0.5, 0.5, 1]
            on_release: root.set_format("mp4")

        MDRaisedButton:
            id: btn_mp3
            text: "MP3 (Audio)"
            size_hint_x: 0.5
            md_bg_color: app.theme_cls.primary_color if not root.format_mp4 else [0.5, 0.5, 0.5, 1]
            on_release: root.set_format("mp3")

    MDRaisedButton:
        id: download_btn
        text: "Télécharger"
        icon: "download"
        size_hint_x: None
        width: "200dp"
        pos_hint: {"center_x": 0.5}
        on_release: root.download_video()
        disabled: root.downloading

    MDProgressBar:
        id: progress_bar
        size_hint_x: None
        width: "350dp"
        pos_hint: {"center_x": 0.5}
        value: 0

    MDLabel:
        id: status_label
        text: ""
        halign: "center"
        theme_text_color: "Secondary"
        size_hint_y: None
        height: "30dp"

    ScrollView:
        size_hint: 1, 0.4

        MDList:
            id: downloads_list
''')


class Content(BoxLayout):
    downloading = BooleanProperty(False)
    format_mp4 = BooleanProperty(True)  # True = MP4, False = MP3

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.downloader = YouTubeDownloader()
        self.download_thread = None

    def set_format(self, fmt):
        """Change le format de téléchargement"""
        self.format_mp4 = (fmt == "mp4")
        self.ids.status_label.text = f"Format sélectionné: {fmt.upper()}"

    def download_video(self):
        url = self.ids.url_field.text.strip()

        if not url:
            self.show_status("Veuillez entrer une URL YouTube", "error")
            return

        if "youtube.com" not in url and "youtu.be" not in url:
            self.show_status("URL YouTube invalide", "error")
            return

        self.downloading = True
        self.ids.download_btn.disabled = True
        self.ids.progress_bar.value = 0
        self.show_status("Préparation du téléchargement...", "info")

        # Lancer le téléchargement dans un thread séparé
        self.download_thread = threading.Thread(
            target=self.download_thread_func,
            args=(url, self.format_mp4)
        )
        self.download_thread.daemon = True
        self.download_thread.start()

    def download_thread_func(self, url, is_mp4):
        """Fonction exécutée dans le thread de téléchargement"""
        try:
            def progress_callback(stream, chunk, bytes_remaining):
                if stream.filesize:
                    percentage = 100 * (1 - bytes_remaining / stream.filesize)
                    Clock.schedule_once(lambda dt: self.update_progress(percentage))

            def complete_callback(filename):
                Clock.schedule_once(lambda dt: self.download_complete(filename))

            self.downloader.on_progress = progress_callback
            self.downloader.on_complete = complete_callback

            audio_only = not is_mp4
            success, result = self.downloader.download(url, audio_only)

            if not success:
                Clock.schedule_once(lambda dt: self.show_status(f"Erreur: {result}", "error"))
                Clock.schedule_once(lambda dt: self.reset_ui())

        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_status(f"Erreur: {str(e)}", "error"))
            Clock.schedule_once(lambda dt: self.reset_ui())

    def update_progress(self, percentage):
        """Met à jour la barre de progression"""
        self.ids.progress_bar.value = percentage
        self.ids.status_label.text = f"Téléchargement: {percentage:.1f}%"

    def download_complete(self, filename):
        """Appelé lorsque le téléchargement est terminé"""
        self.ids.progress_bar.value = 100
        self.show_status(f"Téléchargement terminé: {filename}", "success")
        self.add_to_list(filename)
        self.reset_ui()

    def reset_ui(self):
        """Réinitialise l'interface"""
        self.downloading = False
        self.ids.download_btn.disabled = False

    def add_to_list(self, filename):
        """Ajoute un fichier à la liste d'historique"""
        item = OneLineListItem(text=f"✓ {filename}")
        self.ids.downloads_list.add_widget(item)

    def show_status(self, message, msg_type="info"):
        """Affiche un message de statut"""
        self.ids.status_label.text = message

        # Change la couleur selon le type de message
        if msg_type == "error":
            self.ids.status_label.theme_text_color = "Error"
        elif msg_type == "success":
            self.ids.status_label.theme_text_color = "Custom"
            self.ids.status_label.text_color = [0, 0.7, 0, 1]  # Vert
        else:
            self.ids.status_label.theme_text_color = "Secondary"


class YouTubeDownloaderApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Blue"
        Window.size = (400, 700)
        return Content()

    def on_stop(self):
        """Nettoyage à la fermeture de l'application"""
        if hasattr(self.root, 'download_thread') and self.root.download_thread:
            self.root.download_thread.join(timeout=1)


if __name__ == "__main__":
    YouTubeDownloaderApp().run()
