[app]
title = YouTube Downloader
package.name = youtubedownloader
package.domain = org.youtubedl
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 1.0
requirements = python3,kivy==2.1.0,kivymd==1.1.1,requests
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.arch = arm64-v8a
orientation = portrait

[buildozer]
log_level = 2
