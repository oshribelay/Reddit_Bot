import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

from moviepy.video.io.VideoFileClip import VideoFileClip
import random


def chop_background_video(clip_duration):
    # loading the background video
    video = VideoFileClip("../../Reddit_Bot/background_video/minecraft.mp4")
    # getting the duration of the video
    total_duration = video.duration
    # generate random start time for the clip
    start_time = random.uniform(0, total_duration - clip_duration)
    # cutting the clip from the video
    clip = video.subclip(start_time, start_time + clip_duration)
    # saving the clip
    clip.write_videofile("../background_video/chopped_video.mp4", audio=False)
