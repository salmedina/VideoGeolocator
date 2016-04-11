
# coding: utf-8

# In[6]:

from scipy import misc
import sys, os
import numpy as np
from os import listdir
from os.path import isfile, join
import argparse 
import random
from scipy.spatial.distance import euclidean, cosine, minkowski


# In[5]:

parser = argparse.ArgumentParser()
parser.add_argument("videos_dir", help="all the videos")
parser.add_argument("keyframes_dir", help="output keyframes into this dir")
args= parser.parse_args()


# In[4]:

v_dir = args.videos_dir
sample_v_dir = args.videos_dir # output down sampling results into the VIDEOS_DIR
vnames = [f for f in listdir(v_dir) if isfile(join(v_dir, f)) and "MOV" in f]
vnames = [vname.split('.')[0] for vname in vnames]


# In[30]:

for v_name in vnames:
    cmd = "ffmpeg -y -ss 0 -i {0}/{1}.MOV -strict experimental -r 15 -vf scale=640x480,setdar=4:3 {2}/{1}.mp4".format(v_dir, v_name, sample_v_dir)
    os.system(cmd)


# In[32]:

iframe_dir = "tmp/iframes"
if not os.path.exists(iframe_dir):
    os.makedirs(iframe_dir)
for v_name in vnames:
    #cmd = "~/Documents/ffmpeg/ffmpeg -ss 0 -i {0}/{1}.mp4 -vf select=\"eq(pict_type\\,PICT_TYPE_I)\" -vsync 0 {2}/{1}_%03d.jpg".format(sample_v_dir, v_name, iframe_dir)
    cmd = "~/Documents/ffmpeg/ffmpeg -i {0}/{1}.mp4 -r 1/1 {2}/{1}_%03d.jpg".format(sample_v_dir, v_name, iframe_dir)
    os.system(cmd)


# In[59]:

selected = []
for vname in vnames:
    imgs = []
    img_names = []
    for i in range(1, 100):
        if not os.path.exists("{2}/{0}_{1:03d}.jpg".format(vname, i, iframe_dir)):
            break
        img = misc.imread("{2}/{0}_{1:03d}.jpg".format(vname, i, iframe_dir))
        imgs.append(img)
        img_names.append("{0}_{1:03d}.jpg".format(vname, i))
        hists = []
    for img in imgs:
        hist = [0 for i in range(64)]            
        for i in range(len(img)):
            for j in range(len(img[0])):
                if random.random() > 0.0625: # sample 1/16 pixels for efficiency
                    continue
                b1, b2, b3 = [c/64 for c in img[i][j]]
                idx = b1 * 16 + b2 * 4 + b3
                hist[idx] += 1
        hists.append(np.array(hist))
    selected.append(img_names[0])
    for i in range(1, len(hists)):
        hist1 = hists[i - 1]
        hist2 = hists[i]
        diff= minkowski(hist1, hist2, 1)
        print diff
        if diff > 128000.0/(640 * 480) * (160 * 120): # threshold
            selected.append(img_names[i])
        


# In[63]:

if not os.path.exists(args.keyframes_dir):
    os.mkdir(args.keyframes_dir)
for img in selected:
    os.system("cp {1}/{0} {2}/{0}".format(img, iframe_dir, keyframes_dir))


# In[64]:

print ">> Total keyframes: " + str(len(selected))





