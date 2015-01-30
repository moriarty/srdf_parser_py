cmake_minimum_required(VERSION 2.8.3)
project(srdf_parser_py)
find_package(catkin REQUIRED)

catkin_python_setup()

if(CATKIN_ENABLE_TESTING)
  find_package(rostest REQUIRED)
  add_rostest(test/srdf_parser.test)
endif()
