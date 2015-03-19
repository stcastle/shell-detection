//
//  ImageProcessor.h
//  ppmReaderWriter
//
//  Created by Peck, Tabitha on 9/18/14.
//  Modified by S.T. Castle on 2014-10-08.
//  Copyright (c) 2014 Davidson College. All rights reserved.
//

#ifndef __ppmReaderWriter__ImageProcessor__
#define __ppmReaderWriter__ImageProcessor__

#include <iostream>

#include <stdio.h>
#include <stdlib.h>
#include <cmath>

#include "Filter.h"

#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <glut.h>
#endif
using namespace std;

class ImageProcessor{
public:
    ImageProcessor(int w, int h, int max);
    ImageProcessor(const char* file_name);
    ~ImageProcessor(void);
    void writeImage(const char* file_name);
    int getWidth();
    int getHeight();
    float*** getImage();
    float* getImageDisplayArray();
    ImageProcessor* removeRed();
    ImageProcessor* grayScale();
    ImageProcessor* makeCheck(int, int, int);
    ImageProcessor* simpleScale(int);
    ImageProcessor* spiral(int, float, bool);
    ImageProcessor* overlay(ImageProcessor*);
    ImageProcessor* spiralOverlay(int, float);
    
    // HW 4 functions
    ImageProcessor* blur(Filter* f);
    ImageProcessor* edgeDetection();
    ImageProcessor* sharpen();
    
    // in-class 2014-10-10
    ImageProcessor* enlarge(int w, int h);
    
private:
    char magic_number[2];
    int width;
    int height;
    int max;
    float*** image;
    float* imageDisplayArray;
    
};


#endif /* defined(__ppmReaderWriter__ImageProcessor__) */
