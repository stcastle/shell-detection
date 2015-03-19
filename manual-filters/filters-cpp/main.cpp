/*
  main.cpp

Author: Sam Castle
Date: October, 2014
Davidson College, CSC 361, Fall 2014
HW 4 - Extension of code form HW 3
Time spent: 3.5 hours + 60 minutes for enlarge function
Collaborators: http://www.cplusplus.com/doc/tutorial/other_data_types/
    http://stackoverflow.com/questions/6260883/c-function-receiving-an-enum-as-one-of-its-parameters
    http://en.wikipedia.org/wiki/Edge_enhancement
Feedback: 
    This was a helpful and manageable project for the given time. Surprisingly,
    I also liked that the assignment did not have an open-ended component
    because I know with confidence that I have fulfilled the assignment
    objectives.
Adapted from code created by Dr. Tabitha Peck.
 
*/


#include <iostream>
#include <math.h>
#include "ImageProcessor.h"
#include "Filter.h"

#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <glut.h>
#endif


float win_width = 512;
float win_height = 512;

ImageProcessor* current_image;

void init( void ){
    
    glClearColor(1.0, 0.0, 0.0, 0.0);
	
}

void idle( void ){
    
    glutPostRedisplay();
}

void drawImage( void ){
    
    if(current_image != NULL){
        
        glClear(GL_COLOR_BUFFER_BIT);
        glRasterPos2i(0, 0);
        
        glDrawPixels(current_image->getWidth(), current_image->getHeight(),
                     GL_RGB, GL_FLOAT, current_image->getImageDisplayArray());
    }
    
}

void display( void )
{
    glMatrixMode( GL_PROJECTION );
    glLoadIdentity();
    glOrtho(0, win_width, 0, win_height, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    drawImage();
    
    glFlush();
}

void reshape( int w, int h )
{
    win_width = w;
    win_height = h;
    glViewport( 0, 0, win_width, win_height );
    
    glutPostRedisplay();
}

void keyboard( unsigned char key, int x, int y ) {
    switch(key) {
        case 27: // Escape key
            exit(0);
            break;
    }
}

int main(int argc, char * argv[])
{
    // open the original image
    ImageProcessor* gaudi = new ImageProcessor(
            "/Volumes/users/sacastle/CSC 361 - Computer Graphics/homework/hw4/ppmReaderWriter/gaudi.ppm");
    ImageProcessor* moire = new ImageProcessor(
            "/Volumes/users/sacastle/CSC 361 - Computer Graphics/homework/hw4/ppmReaderWriter/moire.ppm");
    ImageProcessor* sloth = new ImageProcessor(
            "/Volumes/users/sacastle/CSC 361 - Computer Graphics/homework/hw4/ppmReaderWriter/sloth.ppm");
    
    // create filters
    int filter_radius = 3;
    Filter* box = new Filter(BOX, filter_radius);
    Filter* tent = new Filter(TENT, filter_radius);
    Filter* gaussian = new Filter(GAUSSIAN, filter_radius);
    
    // blurred image
    ImageProcessor* box_blurred = moire->blur(box);
    box_blurred->writeImage("/Users/sacastle/Desktop/box_blur_moire.ppm");
    ImageProcessor* tent_blurred = moire->blur(tent);
    tent_blurred->writeImage("/Users/sacastle/Desktop/tent_blur_moire.ppm");
    ImageProcessor* gaussian_blurred = moire->blur(gaussian);
    gaussian_blurred->writeImage("/Users/sacastle/Desktop/gaussian_blur_moire.ppm");
    ImageProcessor* sloth_blurred = sloth->blur(gaussian);
    sloth_blurred->writeImage("/Users/sacastle/Desktop/sloth_blurred.ppm");
    
    // edge detection
    ImageProcessor* edges = gaudi->edgeDetection();
    edges->writeImage("/Users/sacastle/Desktop/edges_gaudi.ppm");
    
    // sharpen
    ImageProcessor* sharp = gaudi->sharpen();
    sharp->writeImage("/Users/sacastle/Desktop/sharpened_gaudi.ppm");
    
    // enlargement
    ImageProcessor* enlarged = sloth->enlarge(800, 1020);
    enlarged->writeImage("/Users/sacastle/Desktop/big_sloth.ppm");
    
    // display the desired image
    current_image = enlarged;
    
    win_height = current_image->getHeight();
    win_width = current_image->getWidth();
    
    glutInit( &argc, argv );
     
    glutInitDisplayMode( GLUT_RGB );
    glutInitWindowSize( win_width, win_height );
    
    glutCreateWindow( "Image" );
     
    init();
     
    glutDisplayFunc( display );
    glutReshapeFunc( reshape );
    glutKeyboardFunc( keyboard );
    glutIdleFunc( idle );
     
     
    glutMainLoop();
    
    // delete filters
    delete box;
    delete tent;
    delete gaussian;
    
    // delete images
    delete gaudi;
    delete moire;
    delete sloth;
    delete box_blurred;
    delete tent_blurred;
    delete gaussian_blurred;
    delete sloth_blurred;
    delete edges;
    delete sharp;
    delete enlarged;
    delete current_image;
    
    return 0;
}