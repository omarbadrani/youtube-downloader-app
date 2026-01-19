import os
import time
from pytubefix import YouTube
from pytubefix.cli import on_progress


class YouTubeDownloader:
    def __init__(self, download_folder=None):
        if download_folder is None:
            # Dossier par défaut: Downloads/YouTube
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

        # Créer le dossier de téléchargement
        os.makedirs(self.download_folder, exist_ok=True)
        print(f"Dossier de téléchargement: {self.download_folder}")

    def sanitize_filename(self, filename):
        """Nettoie le nom de fichier des caractères invalides"""
        # Liste des caractères invalides pour Windows
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')

        # Éviter les noms trop longs
        if len(filename) > 100:
            name, ext = os.path.splitext(filename)
            filename = name[:100 - len(ext)] + ext

        return filename

    def get_video_info(self, url):
        """Récupère les informations de la vidéo"""
        try:
            yt = YouTube(url)
            return {
                'title': yt.title,
                'author': yt.author,
                'length': yt.length,
                'views': yt.views,
                'thumbnail': yt.thumbnail_url
            }
        except Exception as e:
            raise Exception(f"Impossible de récupérer les informations: {str(e)}")

    def download(self, url, audio_only=False):
        """Télécharge la vidéo ou l'audio"""
        try:
            print(f"\n{'=' * 50}")
            print(f"Début du téléchargement")
            print(f"URL: {url}")
            print(f"Audio uniquement: {audio_only}")
            print(f"{'=' * 50}")

            # Créer l'objet YouTube avec callback de progression
            if self.on_progress:
                yt = YouTube(url, on_progress_callback=self.on_progress)
            else:
                yt = YouTube(url, on_progress_callback=on_progress)

            # Afficher les informations
            print(f"Titre: {yt.title}")
            print(f"Auteur: {yt.author}")
            print(f"Durée: {yt.length} secondes")
            print(f"Vues: {yt.views:,}")

            # Nettoyer le titre pour le nom de fichier
            safe_title = self.sanitize_filename(yt.title)

            if audio_only:
                print("\nRecherche du meilleur flux audio...")

                # Tenter de trouver le flux audio avec la meilleure qualité
                stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                if not stream:
                    stream = yt.streams.get_audio_only()

                if not stream:
                    return False, "Aucun flux audio disponible"

                print(f"Flux audio trouvé:")
                print(f"  - Format: {stream.mime_type}")
                print(f"  - Bitrate: {stream.abr}")
                print(f"  - Taille: {stream.filesize_mb:.2f} MB")

                # Télécharger avec nom .mp3
                filename = f"{safe_title}.mp3"
                output_path = os.path.join(self.download_folder, filename)

                print(f"\nTéléchargement en cours...")
                start_time = time.time()

                # Télécharger
                stream.download(
                    output_path=self.download_folder,
                    filename=filename
                )

                elapsed = time.time() - start_time
                print(f"Téléchargement terminé en {elapsed:.1f} secondes")
                print(f"Fichier: {output_path}")

                if self.on_complete:
                    self.on_complete(filename)

                return True, filename

            else:
                print("\nRecherche du meilleur flux vidéo...")

                # Tenter de trouver le flux vidéo MP4 progressif (audio+vidéo)
                stream = yt.streams.filter(
                    progressive=True,
                    file_extension='mp4'
                ).order_by('resolution').desc().first()

                # Si pas de flux progressif, prendre le meilleur adaptatif
                if not stream:
                    video_stream = yt.streams.filter(
                        type='video',
                        file_extension='mp4'
                    ).order_by('resolution').desc().first()

                    audio_stream = yt.streams.filter(
                        type='audio'
                    ).order_by('abr').desc().first()

                    if video_stream and audio_stream:
                        print("Attention: flux adaptatif, qualité optimisée")
                        stream = video_stream
                    else:
                        return False, "Aucun flux vidéo MP4 disponible"

                print(f"Flux vidéo trouvé:")
                print(f"  - Résolution: {stream.resolution}")
                print(f"  - Format: {stream.mime_type}")
                print(f"  - FPS: {stream.fps}")
                print(f"  - Taille: {stream.filesize_mb:.2f} MB")

                # Télécharger avec nom .mp4
                filename = f"{safe_title}.mp4"
                output_path = os.path.join(self.download_folder, filename)

                print(f"\nTéléchargement en cours...")
                start_time = time.time()

                # Télécharger
                stream.download(
                    output_path=self.download_folder,
                    filename=filename
                )

                elapsed = time.time() - start_time
                print(f"Téléchargement terminé en {elapsed:.1f} secondes")
                print(f"Fichier: {output_path}")
                print(f"{'=' * 50}")

                if self.on_complete:
                    self.on_complete(filename)

                return True, filename

        except Exception as e:
            error_msg = f"Erreur lors du téléchargement: {str(e)}"
            print(f"\n{error_msg}")

            if self.on_error:
                self.on_error(error_msg)

            return False, error_msg


# Fonction de test
def test_downloader():
    """Teste le téléchargeur"""
    print("Test du YouTube Downloader")
    print("=" * 50)

    downloader = YouTubeDownloader()

    # URL de test (Rick Astley - Never Gonna Give You Up)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    try:
        # Test d'information
        print("\n1. Test d'information:")
        info = downloader.get_video_info(test_url)
        print(f"   Titre: {info['title']}")
        print(f"   Auteur: {info['author']}")
        print(f"   Durée: {info['length']}s")

        # Test téléchargement vidéo
        print("\n2. Test téléchargement vidéo (MP4):")
        success, result = downloader.download(test_url, audio_only=False)
        print(f"   Résultat: {success} - {result}")

        # Test téléchargement audio
        print("\n3. Test téléchargement audio (MP3):")
        success, result = downloader.download(test_url, audio_only=True)
        print(f"   Résultat: {success} - {result}")

    except Exception as e:
        print(f"\nErreur pendant le test: {str(e)}")


if __name__ == "__main__":
    test_downloader()
