//
//  ImageProcessor.cpp
//  Resolution
//
//  Created by Tabitha Peck on 7/23/13.
//  Modified by S.T. Castle on 2014-10-08.
//  Copyright (c) 2013 Tabitha Peck. All rights reserved.
//  based on code from stack overflow:
//  http://stackoverflow.com/questions/2693631/read-ppm-file-and-store-it-in-an-array-coded-with-c

#include <cmath>

#include "ImageProcessor.h"
#include "Filter.h"


ImageProcessor::ImageProcessor(int w, int h, int m){
    width = w;
    height = h;
    max = m;
    image = new float**[height];
    for(int i = 0; i < height; i++){
        image[i] = new float*[width];
        for(int j = 0; j < width; j++){
            image[i][j] = new float[3];
            image[i][j][0] = 0;
            image[i][j][1] = 0;
            image[i][j][2] = 0;
        }
    }
    imageDisplayArray = NULL;
}

ImageProcessor::ImageProcessor(const char* file_name){
    
    FILE* file;
    char buff[16];
    float r, g, b;
    
    file = fopen(file_name, "r"); // open file for reading
    
    if(!file){
        fprintf(stderr, "Unable to open file %s", file_name);
        exit(1);
    }
    
    fscanf(file, "%s%*[^\n]%*c", magic_number); //read magic number and white space
    
    if(magic_number[0] != 'P' || magic_number[1] != '3'){
        printf("Incorrect file type");
        exit(1);
    }
    
    //check for comments
    fscanf(file, "%s", buff);
    while (strncmp(buff, "#", 1) == 0) {
        fscanf(file, "%s%*[^\n]%*c", buff);
    }
    
    if (fscanf(file, "%d %d %d", &width, &height, &max) != 3) {
        fprintf(stderr, "Invalid image size (error loading '%s')\n", file_name);
        exit(1);
    }
    
    image = new float **[height];
    for(int i = 0; i < height; i++) {
        image[i] = new float *[width];
        for(int j = 0; j<width; j++){
            image[i][j] = new float[3];
            if(fscanf(file, "%f %f %f", &r, &g, &b) != 3){
                fprintf(stderr, "Invalid pixel reading\n");
                exit(1);
            }
            image[i][j][0] = r/max;
            image[i][j][1] = g/max;
            image[i][j][2] = b/max;
        }
    }
    
    fclose(file);
    imageDisplayArray = NULL;
}

ImageProcessor::~ImageProcessor(void){
    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; j++){
            delete [] image[i][j];
        }
        delete [] image[i];
    }
    delete [] image;
    
    delete [] imageDisplayArray;
}

// pre: the given filter is separable
// post: convolve the image with the provided filter
ImageProcessor* ImageProcessor::blur(Filter* f) {
    
    float* f_array = f->getFilter();
    int f_rad = f->getRadius();
    
    // first create an image that blurs along the rows of the image
    // along row i, at pixel j, the filter index 0 corresponds to (j-f_rad),
    // and the end of the filter corresponds to (j+f_rad).
    ImageProcessor* h_blurred = new ImageProcessor(width, height, max);
    int image_index; // the current image index to multiply by filter

    for (int i=0; i < height; i++) {
        for (int j=0; j < width; j++) {
            // iterate through pixels which lie on the radius of the filter,
            // centered at the current pixel j
            for (int x = (j-f_rad); x < (j+f_rad+1); x++) {
                //wrap around at the edge
                if (x < 0)
                    image_index = x + width;
                else if (x > (width-1))
                    image_index = x - width;
                else
                    image_index = x;
                for (int k=0; k<3; k++)
                    h_blurred->image[i][j][k] +=
                        (f_array[x-j+f_rad] * image[i][image_index][k]);
            }
        }
    }
    
    // blur the intermediate image along the columns so the final image
    // is blurred along both the horizontal and the vertical
    ImageProcessor* blurred = new ImageProcessor(width, height, max);
    
    for (int j=0; j < width; j++) {
        for (int i=0; i < height; i++) {
            // iterate through filter centered at current pixel i. filter index
            // corresponds to x-i+f_rad
            for (int x = (i-f_rad); x < (i+f_rad+1); x++) {
                if (x < 0)
                    image_index = x + height;
                else if (x > (height-1))
                    image_index = x - height;
                else
                    image_index = x;
                for (int k=0; k<3; k++)
                    blurred->image[i][j][k] +=
                        (f_array[x-i+f_rad] * h_blurred->image[image_index][j][k]);
            }
        }
    }
    
    delete h_blurred;
    
    return blurred;
}

// post: Detects edges by subtracting a blurred image from the original. Returns
//   a new image, showing the edges
ImageProcessor* ImageProcessor::edgeDetection() {
    
    ImageProcessor* edges = new ImageProcessor(width, height, max);
    
    // create a filter and use it to blur the original image
    int f_radius = 3;
    Filter* f = new Filter(GAUSSIAN, f_radius);
    ImageProcessor* blurred = blur(f);
    
    // subtract the blurred image from the original
    for (int i=0; i < height; i++) {
        for (int j=0; j < width; j++) {
            for (int k=0; k < 3; k++)// multiply the edges by 10 for visibility
                edges->image[i][j][k] =
                    (image[i][j][k] - blurred->image[i][j][k]) * 10;
        }
    }
    
    delete f;
    return edges;
}

// post: sharpen the image by enhancing the edges. That is, find the edges of
//   the image using edgeDetection and add the edge image to the original
ImageProcessor* ImageProcessor::sharpen() {
    
    ImageProcessor* sharp = new ImageProcessor(width, height, max);
    ImageProcessor* edges = edgeDetection(); // find edges
    
    for (int i=0; i < height; i++) {
        for (int j=0; j < width; j++) {
            for (int k=0; k < 3; k++)
                sharp->image[i][j][k] = (image[i][j][k] + edges->image[i][j][k]);
        }
    }
    
    delete edges;
    return sharp;
}

// pre: w >= width and h >= height
// post: returns a new image that is the original scaled to the new width w and
//   the new height h
ImageProcessor* ImageProcessor::enlarge(int w, int h) {
    
    ImageProcessor* large = new ImageProcessor(w, h, max);

    // first enlarge the rows
    for (int i=0; i < height; i++) {
        for (int j=0; j < w; j++) {
            float orig_pixel = ( ((width*1.0/w) * (j + 0.5)) - 0.5 );
            // linear interpolation
            float next_wt = orig_pixel - floor(orig_pixel);
            float prev_wt = 1 - next_wt;
            int next_pixel = ceil(orig_pixel);
            int prev_pixel = floor(orig_pixel);
            //check boundaries
            if (next_pixel > (width-1)) next_pixel = width-1;
            if (prev_pixel < 0) prev_pixel = 0;
            for (int k=0; k < 3; k++) {
                large->image[i][j][k] = prev_wt*image[i][prev_pixel][k] +
                    next_wt*image[i][next_pixel][k];
            }
        }
    }
    
    // enlarge the columns
    // flip the direction of iteration along the height of the new image
    // to avoid overwriting the new image. another solution is to store a
    // temporary image, but this uses less space
    for (int i=(h-1); i >= 0; i--) {
        for (int j=0; j < w; j++) {
            float orig_pixel = ( ((height*1.0/h) * (i+0.5)) - 0.5);
            // linear interpolation
            float next_wt = orig_pixel - floor(orig_pixel);
            float prev_wt = 1 - next_wt;
            int next_pixel = ceil(orig_pixel);
            int prev_pixel = floor(orig_pixel);
            // check boundaries
            if (next_pixel > (height-1)) next_pixel = height-1;
            if (prev_pixel < 0) prev_pixel = 0;
            for (int k=0; k < 3; k++) {
                large->image[i][j][k] = prev_wt*large->image[prev_pixel][j][k] +
                    next_wt*large->image[next_pixel][j][k];
            }
        }
    }
    
    return large;
}

// post: returns a new ImageProcessor* that is a copy of the original image
//       with all red pixel values set to zero
ImageProcessor* ImageProcessor::removeRed(){
    
    ImageProcessor* red = new ImageProcessor(width, height, max);

    // set the pixel color values based on the original image
    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; j++){
            red->image[i][j][0] = 0; // make sure red value is zero
            red->image[i][j][1] = image[i][j][1]; // preserve green
            red->image[i][j][2] = image[i][j][2]; // preserve blue
        }
    }
    
    return red;
}

// post: returns a new ImageProcessor* that is a copy of the original image
//      with pixel values converted to grayscall based on human color perception
ImageProcessor* ImageProcessor::grayScale(){
    
    ImageProcessor* gray = new ImageProcessor(width, height, max);
    
    // set the pixel color values to gray
    float gray_value; // gray color value of current pixel
    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; j++){
            gray_value = 0.2126*image[i][j][0] + // red
                         0.7251*image[i][j][1] + // green
                         0.0722*image[i][j][2];  // blue
            for(int k = 0; k < 3; k++){
                gray->image[i][j][k] = gray_value;
            }
        }
    }
    
    return gray;
}

// post: return a new ImageProcessor* object that is an image of a checkerboard
//       with width w, height h, and num_checks squares in each row and column
ImageProcessor* ImageProcessor::makeCheck(int w, int h, int num_checks) {
    
    ImageProcessor* check = new ImageProcessor(w, h, max);
    
    // get the width and height of each colored square on the checkerboard
    int w_check = w / num_checks; // integer division
    int h_check = h / num_checks;
    int color_value = 1; // value to color the pixel. 0 for black. 1 for white.
    
    for (int i = 0; i < h; i++) {
        for (int j = 0; j < w; j++) {
            if ( ( (j / w_check) + (i / h_check) ) % 2) //if in a black row,col
                color_value = 0; // black
            else
                color_value = 1; // white
            for (int k = 0; k < 3; k++)
                check->image[i][j][k] = color_value;
        }
        
    }
    
    return check;
}

// post: returns a new ImageProcessor* object that consists of a smaller version
//      of the original image by sampling pixels with jumps equal to sample_rate
ImageProcessor* ImageProcessor::simpleScale(int sample_rate) {
    
    int new_width = (width)/sample_rate + 1; // integer division
    int new_height = (height) / sample_rate + 1; // +1 to avoid out of bounds
    ImageProcessor* scaled = new ImageProcessor(new_width, new_height, max);
    
    for (int i = 0; i < height; i++) {
        if (i % sample_rate == 0) {
            for (int j = 0; j < width; j++) {
                if (j % sample_rate == 0) // if a multiple of sample_rate
                    for (int k = 0; k < 3; k++)
                        scaled->image[i/sample_rate][j/sample_rate][k] =
                                image[i][j][k];
            }
        }
    }
    
    return scaled;
}

int ImageProcessor::getWidth(){
    return width;
}

int ImageProcessor::getHeight(){
    return height;
}

float*** ImageProcessor::getImage(){
    return image;
}

// pre: thickness is an integer for the thickness of each rotated slice,
//      spiral_factor scales the angle through which slices are rotated,
//      and ccw determines the direction of rotation: counter-clockwise if true,
//      and clockwise otherwise. For spiral_factor, multiples of pi work well
// post: returns a new ImageProcessor* that has been spiraled counter-clockwise
ImageProcessor* ImageProcessor::spiral(
                                int thickness, float spiral_factor, bool ccw) {
    
    ImageProcessor* spiraled = new ImageProcessor(width, height, max);
    
    // get coordinates of center pixel
    int x_center = width/2;
    int y_center = height/2;

    // create spiral
    for(int i = 0; i < height; i++) {
        int temp_i = i - y_center; // rotate about the origin
        for(int j = 0; j < width; j++) {
            
            int temp_j = j - x_center;
            
            //bin pixels by radius and choose rotation angle as a func of radius
            int radius = (temp_i*temp_i + temp_j*temp_j)/thickness/thickness;
            float angle = spiral_factor*radius;
            if (!ccw) angle = -angle; // reverse angle if rotation is clockwise
            
            int new_i = y_center + ( temp_j*sin(angle) + temp_i*cos(angle) );
            int new_j = x_center + ( temp_j*cos(angle) - temp_i*sin(angle) );
            
            // put old pixels into new position
            if (new_i>0 && new_i < height && new_j>0 && new_j < width) {
                for (int k = 0; k < 3; k++)
                    spiraled->image[new_i][new_j][k] = image[i][j][k];
            }
        }
    }

    return spiraled;
}

// post: overlays a second image with the original by averaging pixel values
ImageProcessor* ImageProcessor::overlay(ImageProcessor* other) {

    // new height and width are the larger of the two values
    int h = std::min(height, other->getHeight());
    int w = std::min(width, other->getWidth());
    ImageProcessor* composite = new ImageProcessor(w, h, max);

    for (int i = 0; i < h; i++){
        for (int j = 0; j < w; j++) {
            for (int k = 0; k < 3; k++) {
                // average the pixel values
                composite->image[i][j][k] =
                    0.5*(image[i][j][k] + other->image[i][j][k]);
            }
        }
    }

    return composite;
}

// post: returns an image that has been swirled in two directions and overlayed
ImageProcessor* ImageProcessor::spiralOverlay(int thickness,
                                              float spiral_factor) {
    
    ImageProcessor* cw = spiral(thickness, spiral_factor, false);
    ImageProcessor* ccw = spiral(thickness, spiral_factor, true);
    return cw->overlay(ccw);

}

// pre: image is a 3D array of size width x height x 3. The values contained
//      are the 3 rgb values at the pixel at the particular width and height
// post: returns a 1D array starting at the bottom left corner of the image
float* ImageProcessor::getImageDisplayArray() {
    
    // return if the function has already been called and work already done
    if(imageDisplayArray != NULL)
        return imageDisplayArray;
    
    imageDisplayArray = new float[width * height * 3];
    
    // iterate through every pixel in image
    // original image has (0,0) as top left pixel, so flip top-to-bottom, so
    // imageDisplayArray begins with bottom left pixel
    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; j++){
            for (int k = 0; k < 3; k++) {  // loop through colors rgb
                imageDisplayArray[ ( ((i*width) + j) * 3) + k] =
                    image[height-1-i][j][k];
            }
        }
    }
    
    return imageDisplayArray;
}

// 
void ImageProcessor::writeImage(const char* file_name){
    
    FILE* file;
    file = fopen(file_name, "w"); // open file for writing
    if(!file){
        fprintf(stderr, "Unable to open file %s", file_name);
        exit(1);
    }
    
    //getImageDisplayArray(); // create image display array
    
    // write the ppm header and image data to file
    
    // header
    fprintf(file, "P3\n"); // ppm file type
    fprintf(file, "# Creator: Sam Castle\n");
    fprintf(file, "%d %d\n", width, height);
    fprintf(file, "%d\n", max);
    
    // image data
    for(int i = 0; i < height; i++){
        for(int j = 0; j < width; j++){
            for (int k = 0; k < 3; k++) {  // loop through colors rgb
                fprintf(file, "%d\n", static_cast<int>(image[i][j][k]*max));
            }
        }
    }
    
    fclose(file);
    
}



