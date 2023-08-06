include(CMakeFindDependencyMacro)

if (NOT HAMR_DIR)
  if ()
    set(HAMR_DIR "/home/bloring/work/teca/TECA_abdel/build/temp.linux-x86_64-3.10")
  else()
    set(HAMR_DIR "/home/bloring/work/teca/TECA_abdel/build/lib.linux-x86_64-3.10/teca")
  endif()
endif()
list(APPEND CMAKE_MODULE_PATH "${HAMR_DIR}")

set(HAMR_LIB_TYPE STATIC)
if (ON;FORCE)
  set(HAMR_LIB_TYPE SHARED)
endif()

set(HAMR_ENABLE_CUDA ON)
set(HAMR_CUDA_OBJECTS OFF)
set(HAMR_ENABLE_HIP OFF)
set(HAMR_HIP_OBJECTS ON)
set(HAMR_ENABLE_PYTHON OFF)
set(HAMR_VERBOSE OFF)

include(hamr)
