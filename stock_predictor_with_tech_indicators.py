import pickle
import stockstats
# Load data (deserialize)
with open('stock_prices_dict.pickle', 'rb') as f:
    stock_prices_dict = pickle.load(f)

df = stock_prices_dict["WIPRO"]
df_stock = StockDataFrame.retype(df)
from moviepy.editor import VideoFileClip, concatenate_videoclips
clip1 = VideoFileClip("/home/anup/Downloads/personal/vid_a.mp4")
clip2 = VideoFileClip("/home/anup/Downloads/personal/vid_b.mp4")

import moviepy.editor as mp
clip1 = clip1.resize(height=360)
clip2 = clip2.resize(height=360)


concat_clip = mp.concatenate_videoclips([clip1,clip2], method="compose")


concat_clip.write_videofile("concat_file.mp4")