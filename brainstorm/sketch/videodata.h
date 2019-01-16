#ifndef _VIDEODATA_
#define _VIDEODATA_

#include <stdlib.h>

typedef struct
{
    // Each of these fields will likely be 3-5 values long.
    char* name;			// Video file name.
    int* common_freqs_reals;	// Real components of DFT output.
    int* common_freqs_imags;	// Imag. " " " "
    int* common_colors_red;	// R-values for the most common colors.
    int* common_colors_grn;	// G-values " " " " "
    int* common_colors_blu;	// B-values " " " " "
} videodata;

videodata* create();		// Returns a ptr to a malloc'd videodata struct.
void build(videodata* stock);	// Fill structure and set field values.
void remove(videodata* stock);	// Free dynamically allocated data in the fields
				// of the struct and the struct itself.

#endif
