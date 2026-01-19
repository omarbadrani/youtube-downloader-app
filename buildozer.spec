[app]

title = YouTube Downloader
package.name = youtubedownloader
package.domain = org.youtubedl

source.dir = .
source.include_exts = py,png,jpg,kv,ttf

version = 1.0
version.code = 1

requirements = python3,kivy==2.1.0,kivymd==1.1.1,requests,certifi

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# CORRECTION : Utiliser android.api seulement
android.api = 30
android.minapi = 21
# SUPPRIMEZ cette ligne : android.sdk = 30

# CORRECTION : Utiliser android.archs au lieu de android.arch
android.archs = arm64-v8a

# NDK version compatible
android.ndk = 23b

orientation = portrait
fullscreen = 0

[buildozer]

build_dir = ./.buildozer
bin_dir = ./bin

log_level = 2
