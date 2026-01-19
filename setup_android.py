# setup_android.py - Script pour accepter les licences
import os
import subprocess
import time


def setup_android_licenses():
    """Configure Android SDK licenses automatiquement"""

    print("🔧 Configuration des licences Android...")

    # Créer le dossier .android
    android_dir = os.path.expanduser("~/.android")
    licenses_dir = os.path.join(android_dir, "licenses")

    os.makedirs(licenses_dir, exist_ok=True)

    # Fichiers de licence acceptés
    license_files = {
        "android-sdk-license": [
            "8933bad161af4178b1185d1a37fbf41ea5269c55",
            "d56f5187479451eabf01fb78af6dfcb131a6481e",
            "24333f8a63b6825ea9c5514f83c2829b004d1fee"
        ],
        "android-sdk-preview-license": [
            "84831b9409646a918e30573bab4c9c91346d8abd"
        ]
    }

    # Écrire les fichiers de licence
    for filename, licenses in license_files.items():
        with open(os.path.join(licenses_dir, filename), "w") as f:
            f.write("\n".join(licenses))
        print(f"✅ {filename} créé")

    # Créer repositories.cfg
    repos_file = os.path.join(android_dir, "repositories.cfg")
    with open(repos_file, "w") as f:
        f.write("### User Sources for Android SDK Manager\n")
    print("✅ repositories.cfg créé")

    # Configurer les variables d'environnement
    os.environ["BUILD_OZER_ACCEPT_SDK_LICENSE"] = "1"
    os.environ["BUILD_OZER_SKIP_SDK_CHECK"] = "1"

    print("🎉 Licences Android configurées avec succès!")


if __name__ == "__main__":
    setup_android_licenses()