from fits_proc import FitsProc
import fileinput

def main():
    for file in fileinput.input():

        filename = fileinput.filename()
        image = FitsProc(filename)
        print 'Opened ' + filename
        
        print 'fmfe working...'
        image.blur()
        print 'Finished fmfe.'
     
        
        newfile = 'fmfe_' + filename
        image.write(newfile)
        print 'New file written as ' + newfile 
     
        print 'Detecting edges.'
        image.edges()
        print 'Edges detected.'

        newfile = 'edges_' + filename
        image.write(newfile)
        print 'New file written as ' + newfile
        
        fileinput.nextfile()

    fileinput.close()

if __name__ == '__main__':
    main()
