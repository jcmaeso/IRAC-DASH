#!/bin/bash

x264 --output ./video/$1/low_config.264 --fps 24 --preset slow --bitrate 100 --vbv-maxrate 4800 --vbv-bufsize 9600 --min-keyint 48 --keyint 48 --scenecut 0 --no-scenecut --pass 1 --video-filter "resize:width=160,height=90" ./video/$1/$1.mp4
x264 --output ./video/$1/medium_config.264 --fps 24 --preset slow --bitrate 600 --vbv-maxrate 4800 --vbv-bufsize 9600 --min-keyint 48 --keyint 48 --scenecut 0 --no-scenecut --pass 1 --video-filter "resize:width=640,height=360" ./video/$1/$1.mp4
x264 --output ./video/$1/high_config.264 --fps 24 --preset slow --bitrate 2400 --vbv-maxrate 4800 --vbv-bufsize 9600 --min-keyint 48 --keyint 48 --scenecut 0 --no-scenecut --pass 1 --video-filter "resize:width=1280,height=720" ./video/$1/$1.mp4


#Low quality video
MP4Box -add ./video/$1/low_config.264 -add ./video/$1/$1.mp4#audio -fps 24 ./video/$1/low.mp4
#Medium quality video
MP4Box -add ./video/$1/medium_config.264 -fps 24 ./video/$1/medium.mp4
#High quality video
MP4Box -add ./video/$1/high_config.264 -fps 24 ./video/$1/high.mp4


#Low quality video
 ../Bento/bin/mp4fragment ./video/$1/medium.mp4 ./video/$1/frag_medium.mp4
#Medium quality video
 ../Bento/bin/mp4fragment ./video/$1/high.mp4 ./video/$1/frag_high.mp4
#High quality video
 ../Bento/bin/mp4fragment ./video/$1/low.mp4 ./video/$1/frag_low.mp4


../Bento/bin/mp4dash  ./video/$1/frag_high.mp4 ./video/$1/frag_low.mp4 ./video/$1/frag_medium.mp4 -o ./data/$1

ffmpeg -ss 00:01:00 -i ./video/$1/$1.mp4 -vframes 1 -q:v 2 ./data/$1/thumbnail.jpg

rm -rf ./video/$1/
