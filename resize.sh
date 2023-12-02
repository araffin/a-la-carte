#!/bin/bash

mogrify -path ./images/ \
        -resize 600x \
        -format webp \
        -quality 85 \
        ./images-tmp/*

