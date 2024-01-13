#!/bin/bash

mogrify -path ./images/ \
        -resize 1000x \
        -format webp \
        -quality 85 \
        ./images-tmp/*

