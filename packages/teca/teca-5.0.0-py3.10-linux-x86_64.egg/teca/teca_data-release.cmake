#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "teca_data" for configuration "Release"
set_property(TARGET teca_data APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(teca_data PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./libteca_data.so"
  IMPORTED_SONAME_RELEASE "libteca_data.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS teca_data )
list(APPEND _IMPORT_CHECK_FILES_FOR_teca_data "${_IMPORT_PREFIX}/./libteca_data.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
