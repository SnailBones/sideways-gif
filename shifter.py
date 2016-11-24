
#
# This code turns GIFs sideways in time!
#
# It makes use of the images2gif module by Almar Klein, Ant1, and Marius van Voorden
#
# If you use/modify it, please credit me and show me what you create!
#
# SnailBones (A. Hendrickson) 2016
#


from PIL import Image, ImageSequence
import sys, os
import numpy as np
from images2gif import writeGif

def select():
    if (len(sys.argv) > 1):
        name = sys.argv[1]
    else:
        name = "pizzadog.gif"
    return name

def clearDir(dir):
    for f in os.listdir(dir):
        os.remove(dir + "/" + f)

def extractFrames(name):
    frame = Image.open(name)
    nframes = 0
    frames = []
    while frame:
        fr = frame.copy().convert('RGB')
        # if nframes == 0:
        #     palette = fr.getpalette()
        # else:
        #     fr.putpalette(palette)
        frames.append(fr)
        nframes += 1
        try:
            frame.seek( nframes )
        except EOFError:
            break;
    return frames


def switchDimensions(old_frames, myName):
    length = len(old_frames)
    new_frames = []
    width, height = old_frames[0].size

    print "width: %i height: %i, depth: %i" % (width, height, length)
    for r in range(height):
        new_img = Image.new('RGB',(width, length))
        for c in range(width):
            for i in range(length):
                pix = old_frames[i].getpixel((c, r))
                new_img.putpixel((c,i), pix)
        new_frames.append(new_img)

    name = 'twisted-' + myName
    writeGif(name, new_frames, dither=0)
    print ("saved gif with name %s" % name)
    return new_frames

def saveAsIms (frames, dir, name = "frame"): #testing method, save the array as a series of images
    clearDir(dir)
    for i in range(len(frames)):
        frames[i].save( '%s/%s.%s.gif' % (dir, name, i ) , 'GIF')
    print "saved images in directory %s" % dir


name = select()
frames = extractFrames(name)
switchDimensions(frames, name)
