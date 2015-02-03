@[if DEVELSPACE]@
set(_srdf_parser_py
  @(CMAKE_CURRENT_SOURCE_DIR)/src
)
@[else]@
set(_srdf_parser_py
  ${srdf_parser_py_DIR}/../../../@(CATKIN_PACKAGE_BIN_DESTINATION)/srdf_parser_py
)
@[end if]@


