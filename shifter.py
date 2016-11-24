from PIL import Image, ImageSequence
import sys, os
# import moviepy.editor as mpy
import imageio
import numpy as np
from images2gif import writeGif

def select():
    if (len(sys.argv) > 1):
        name = sys.argv[1]
    else:
        name = "dolphin"
    return name

def clearDir(dir):
    for f in os.listdir(dir):
        os.remove(dir + "/" + f)

def extractFrames(name, outFolder):
    frame = Image.open("gifs/"+name+".gif")
    nframes = 0
    clearDir(outFolder)
    frames = []
    while frame:
        fr = frame.copy().convert('RGB')
        fr.save( '%s/%s.%s.gif' % (outFolder, name, nframes ) , 'GIF')
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


def switchDimensions(old_frames, outFolder, myName = 'frame'):
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

    name = myName + '.gif'
    writeGif(name, new_frames, dither=0)
    print ("saved gif with name %s" % name)
    return new_frames

def saveAsIms (frames, dir, name = "frame"): #testing method, save the array as a series of images
    clearDir(dir)
    for i in range(len(frames)):
        frames[i].save( '%s/%s.%s.gif' % (dir, name, i ) , 'GIF')
    print "saved images in directory %s" % dir


name = select()
frames = extractFrames(name, 'frames')
switchDimensions(frames,'new_frames', name)

#rebuildImageIo('new_frames', name)
