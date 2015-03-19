from filter import Filter
from image_processor import FitsProc

def main():
    '''
    # Play with filters.
    rad = 2

    box = Filter('BOX', rad)
    print "box:"
    print box.getFilter()

    tent = Filter('Tent', rad)
    print
    print 'tent:'
    print tent.getFilter()

    gauss = Filter('gaussian', rad)
    print
    print 'gauss:'
    print gauss.getFilter()

    print
    nope = Filter('nope', rad)

    print
    '''

    # Convolution
    filename = 'n3923_shell1na.fits'
    orig = FitsProc(filename)
    print 'Opened ' + filename + '.'
    
    #orig_data = orig.get_data()
    #print 'got orig data.'

    orig.detect_edges()
    print 'Edges detected.'

    #edge_data = edge.get_data()
    
    orig.write('edges.fits')
    print 'Wrote edges data to file.'

    #print orig_data[:10][:10]
    #print edge_data[:10][:10]

if __name__ == '__main__':
    main()
