#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "teca_core" for configuration "Release"
set_property(TARGET teca_core APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(teca_core PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./libteca_core.so"
  IMPORTED_SONAME_RELEASE "libteca_core.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS teca_core )
list(APPEND _IMPORT_CHECK_FILES_FOR_teca_core "${_IMPORT_PREFIX}/./libteca_core.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
