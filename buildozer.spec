[app]

title = YouTube Downloader
package.name = youtubedownloader
package.domain = org.youtubedl

source.dir = .
source.include_exts = py

version = 1.0
version.code = 1

requirements = python3,kivy==2.1.0,kivymd==1.1.1,requests

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE

# Use older API to avoid build-tools 36.1 issue
android.api = 29
android.minapi = 21

# Use older NDK
android.ndk = 21.3.6528147

# Architecture
android.archs = arm64-v8a

orientation = portrait
fullscreen = 0

[buildozer]

build_dir = ./.buildozer
bin_dir = ./bin

log_level = 2
