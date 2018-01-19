
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
ffmpeg_extract_subclip("2018-01-04-VIDEO-00000576.mp4", 0, 140, targetname="test.mp4")