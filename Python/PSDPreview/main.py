# Standard libraries
import os, sys

# PIL library
import Image

THUMBNAILS_DIRECTORY = 'thumbnails/'
THUMBNAILS_TYPE = "PNG"
THUMBNAILS_SIZE = (128, 128)

if (len(sys.argv) != 2):
    # retrieve the program name
    n = os.path.split(sys.argv[0])[-1]
    print('Usage: %s <filename>' % (n))
    sys.exit(0)
else if not os.path.exists(sys.argv[1]):
    print('Unable to find %s' % (sys.argv[1]))

# Source file
filename_ext = os.path.split(sys.argv[1])[-1]
filename, fileext = os.path.splitext(filename_ext)

def createThumbnail(filepath):
    """ create the thumbnail in THUMBNAILS_DIRECTORY """

    # Output file
    thumbname = '%s.thumbnail' % (filename)
    thumbpath = '%s%s' % (THUMBNAILS_DIRECTORY, thumbname)

    try:
        im = Image.open(filepath)
        im.thumbnail(THUMBNAILS_SIZE)
        im.save(thumbpath, THUMBNAILS_TYPE)
        return thumbpath
    except IOError:
        return None

def hasValidThumbnail(filepath):
    """ return the path to the valid thumbnail or None """

    

print createThumbnail(sys.argv[1])
