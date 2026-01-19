import os
import time

class YouTubeDownloader:
    def __init__(self, download_folder=None):
        if download_folder is None:
            self.download_folder = os.path.join(
                os.path.expanduser("~"),
                "Downloads",
                "YouTube_Downloads"
            )
        else:
            self.download_folder = download_folder

        self.on_progress = None
        self.on_complete = None
        self.on_error = None

        os.makedirs(self.download_folder, exist_ok=True)

    def download(self, url, audio_only=False):
        """Version de démonstration"""
        try:
            # Simuler la progression
            if self.on_progress:
                for i in range(0, 101, 10):
                    self.on_progress(i)
                    time.sleep(0.2)

            # Simuler la fin
            filename = "video_test.mp4" if not audio_only else "audio_test.mp3"
            
            if self.on_complete:
                self.on_complete(filename)
            
            return True, filename
            
        except Exception as e:
            error_msg = f"Erreur: {str(e)}"
            if self.on_error:
                self.on_error(error_msg)
            return False, error_msg
