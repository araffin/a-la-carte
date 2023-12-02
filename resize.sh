#!/bin/bash

mogrify -path ./images/ \
        -resize 600x \
        -format jpg \
        -quality 90 \
        ./images/*

