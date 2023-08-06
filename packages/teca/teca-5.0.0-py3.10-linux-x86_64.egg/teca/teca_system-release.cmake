#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "teca_system" for configuration "Release"
set_property(TARGET teca_system APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(teca_system PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/./libteca_system.so"
  IMPORTED_SONAME_RELEASE "libteca_system.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS teca_system )
list(APPEND _IMPORT_CHECK_FILES_FOR_teca_system "${_IMPORT_PREFIX}/./libteca_system.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
