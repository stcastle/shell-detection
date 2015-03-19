#from scipy import misc
import matplotlib.image
import fileinput
import fmfe
import edge-detect

def png_proc():
    for file in fileinput.input():
        filename = fileinput.filename()

        img = matplotlib.image.imread(filename)
        img = img[:,:,0] # make 2-D
        print 'Opened ' + filename
        print type(img)
        print img.shape
        print img.dtype

        h = img.shape[0]
        w = img.shape[1]

        print 'Running fmfe...'
        img = fmfe.fmfe(img, w, h, 0.5)
        print 'Completed fmfe.'

        newfilename = 'fmfe_' + filename
        matplotlib.image.imsave(newfilename, img)
        print 'Saved to ' + newfilename

        print 'Detecting edges...'
        img = edge_detect.find_edges(img, h, w)
        print 'Found edges.'

        newfilename = 'edges_' + filename
        matplotlib.image.imsave(newfilename, img)
        print 'Saved to ' + newfilename

        fileinput.nextfile()

    fileinput.close()



if __name__ == '__main__':
    png_proc()
