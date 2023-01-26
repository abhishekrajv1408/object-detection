from moviepy.editor import *

clip = VideoFileClip("video_1.mp4")
clip = clip.subclip(7, 21)
final = clip.fx(vfx.speedx,0.1)
final.write_videofile("input/video_1.mp4")
