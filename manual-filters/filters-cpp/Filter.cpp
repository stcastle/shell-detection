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

#include <cmath>
#include "Filter.h"


// constructs a 1D filter object of the specified filter_type (box, tent, or
// gaussian) with radius filter_r. So, total filter width is (2*filter_r + 1).
Filter::Filter(filter_name filter_type, int filter_r) {

    f_radius = filter_r;
    f_width = 2*f_radius + 1;
    f_array = new float[f_width];
    
    switch (filter_type) {
        case BOX: make_box(); break;
        case TENT: make_tent(); break;
        case GAUSSIAN: make_gaussian(); break;
    }
    
}

Filter::~Filter() {
    delete [] f_array;
}

float* Filter::getFilter() {
    return f_array;
}

int Filter::getRadius() {
    return f_radius;
}

int Filter::getWidth() {
    return f_width;
}

// pre: f_array is defined and has size f_width
void Filter::make_box() {

    float val = 1.0 / f_width; // normalized value at each point
    for (int i=0; i<f_width; i++)
        f_array[i] = val;
    
}

// pre: f_array is defined and has size f_width
void Filter::make_tent() {

    float sum = 0.0; // track the sum of filter values for normalization
    
    // fill f_array
    for (int i=0; i<f_width; i++) {
        // displacement from center pixel, which has index f_radius
        float x = i - f_radius;
        // compute the tent filter value for the current position
        float val = ( 1.0 - abs(x*1.0/f_radius) ) / f_radius;
        // place val in array and increase sum
        f_array[i] = val;
        sum += val;
    }
    
    // normalize values in f_array
    for (int i=0; i<f_width; i++)
        f_array[i] = f_array[i] / sum;

}

// pre: f_array is defined and has size f_width
void Filter::make_gaussian() {

    float sum = 0.0; // track the sum of filter values for normalization
    float sigma = (f_radius - 1.0) / 3.0; // standard dev for gaussian distro
    
    // fill f_array
    for (int i=0; i<f_width; i++) {
        // calculate value for filter at position i-f_radius, which equals the
        // displacement from the center pixel located at index f_radius
        float val = gauss(i-f_radius, sigma);
        // place val in array and increase sum
        f_array[i] = val;
        sum += val;
    }
    
    // normalize values in f_array
    for (int i=0; i<f_width; i++)
        f_array[i] = f_array[i] / sum;
    
}

// returns the value at position x of a gaussian distribution centered at zero
// and with standard deviation sigma
float Filter::gauss(float x, float sigma) {
    return ( (1.0 / (sigma * sqrt(2*M_PI)) ) * exp(-x*x / (2*sigma*sigma)) );
}