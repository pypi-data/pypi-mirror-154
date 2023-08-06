#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "teca_io" for configuration "Release"
set_property(TARGET teca_io APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(teca_io PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./libteca_io.so"
  IMPORTED_SONAME_RELEASE "libteca_io.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS teca_io )
list(APPEND _IMPORT_CHECK_FILES_FOR_teca_io "${_IMPORT_PREFIX}/./libteca_io.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
