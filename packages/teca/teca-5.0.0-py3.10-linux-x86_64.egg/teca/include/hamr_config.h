#ifndef config_h
#define config_h

#define HAMR_EXPORT __attribute__ ((visibility ("default")))
#define HAMR_PRIVATE __attribute__ ((visibility ("hidden")))

#define HAMR_ENABLE_CUDA
/* #undef HAMR_CUDA_OBJECTS */
/* #undef HAMR_ENABLE_HIP */
#define HAMR_HIP_OBJECTS
/* #undef HAMR_ENABLE_OPENMP */
#define HAMR_OPENMP_OBJECTS
#define HAMR_OPENMP_LOOP 
/* #undef HAMR_ENABLE_PYTHON */
/* #undef HAMR_VERBOSE */

#endif
