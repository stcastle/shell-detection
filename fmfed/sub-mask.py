from fits-proc import FitsProc

def main():
    filename = 'n3923_shell1na.fits'
    image = FitsProc(filename)
    print 'Opened ' + filename

   # data = image.get_data()
   # print 'data:'
   # print data[:10][0]
   # image.edges()
   # print 'Finished fmfe.'
     
    #print 'data:'
    #print data[:10][0]

    mask_filename = 'n3923_shell1na_mask.fits'
    print 'Subtracting mask ' + mask_filename
    image.subtract_mask(mask_filename)
    print 'Subtracted mask ' + mask_filename

    newfile = 'n3923_shell1na_minus_mask.fits' 
    image.write(newfile)
    print 'New file written as ' + newfile 

    print 'Detecting edges.'
    image.edges()
    print 'Detected edges.'

    newfile = 'n3923_shell1na_minus_mask_plus_edges.fits'
    image.write(newfile)
    print 'New file written as ' + newfile 



if __name__ == '__main__':
    main()
