cmake_minimum_required(VERSION 2.8.3)
project(srdf_parser_py)
find_package(catkin REQUIRED COMPONENTS urdfdom_py)

catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS urdfdom_py
  CFG_EXTRAS srdf_parser_py-extras.cmake
)

if(CATKIN_ENABLE_TESTING)
  find_package(rostest REQUIRED)
  add_rostest(test/srdf_parser.test)
endif()
