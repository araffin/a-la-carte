#!/bin/bash

convert icons/bunman_no_bg.png -resize 64x64 icons/android-chrome-64x64.png
convert icons/bunman_no_bg.png -resize 192x192 icons/android-chrome-192x192.png
convert icons/bunman_no_bg.png -resize 512x512 icons/android-chrome-512x512.png
convert icons/bunman_no_bg.png -resize 180x180 icons/apple-touch-icon-180x180.png

convert icons/bunman_no_bg.png -resize 32x32 icons/favicon.ico
