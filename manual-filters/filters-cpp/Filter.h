//
//  Filter.h
//  ppmReaderWriter
//
//  Created by Castle, Sam on 10/8/14.
//  Davidson College CSC 361 Fall 2014 - HW 4
//  Copyright (c) 2014 Davidson College. All rights reserved.
//
//  Class creates a filter for image convolutions.
//  header file

#ifndef ppmReaderWriter_Filter_h
#define ppmReaderWriter_Filter_h

#include <iostream>

#include <stdio.h>
#include <stdlib.h>
#include <cmath>

#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <glut.h>
#endif
using namespace std;

enum filter_name {BOX, TENT, GAUSSIAN}; // available filters enum

class Filter {
    
public:
    
    Filter(filter_name filter_type, int filter_r);
    ~Filter();
    
    float* getFilter();
    int getRadius();
    int getWidth();
    
private:
    // fields
    float* f_array; // the filter array
    int f_radius;   // the filter radius
    int f_width;    // the filter width
    
    // methods
    void make_box();
    void make_tent();
    void make_gaussian();
    float gauss(float, float);
    
};

#endif
