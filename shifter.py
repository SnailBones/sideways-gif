
# SnailBones (A. Hendrickson) 2016
#


from PIL import Image, ImageFile, ImageSequence
import sys, os
import numpy as np
import imageio

Image.LOAD_TRUNCATED_IMAGES = True
ImageFile.LOAD_TRUNCATED_IMAGES = True

def select():
    if (len(sys.argv) > 1):
        name = sys.argv[1]
    else:
        print("using demo GIF")
        name = "gifs/pizzatwist.gif"
    if (len(sys.argv) > 2 and sys.argv[2] == "-v"):
        mode = 1
    else:
        mode = 0
    return name, mode

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


def switchDimensions(old_frames, myName, mode):
    length = len(old_frames)
    new_frames = []
    width, height = old_frames[0].size
    print ("width: %i height: %i, depth: %i" % (width, height, length))
    if (mode == 1):
    # top to bottom
        print("switching z with x")
        for y in range(height):
            new_img = Image.new('RGB',(width, length))
            for x in range(width):
                for z in range(length):
                    pix = old_frames[z].getpixel((x, y))
                    new_img.putpixel((x,z), pix)
            new_frames.append(new_img)

    else:
    # left to right
        print("switching z with y")
        for x in range(width):
            new_img = Image.new('RGB',(length, height))
            for y in range(height):
                for z in range(length):
                    pix = old_frames[z].getpixel((x, y))
                    new_img.putpixel((z, y), pix)
            new_frames.append(new_img)
            # imageio.mimsave("frames/frame"+ str(x) + ".gif", [new_img])


    name = 'twisted-' + myName.split("/")[-1]
    print ("saving gif with name %s" % name)
    imageio.mimsave(name, new_frames)
    return new_frames

def saveAsIms (frames, dir, name = "frame"): #testing method, save the array as a series of images
    clearDir(dir)
    for i in range(len(frames)):
        frames[i].save( '%s/%s.%s.gif' % (dir, name, i ) , 'GIF')
    print ("saved images in directory %s" % dir)


name, mode = select()
frames = extractFrames(name)
switchDimensions(frames, name, mode)
