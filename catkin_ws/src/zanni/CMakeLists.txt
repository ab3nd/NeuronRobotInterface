cmake_minimum_required(VERSION 2.8.3)
project(zanni)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
	message_generation
  roscpp
  std_msgs
)

## System dependencies are found with CMake's conventions
# find_package(Boost REQUIRED COMPONENTS system)

## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
# catkin_python_setup()

#######################################
## Declare ROS messages and services ##
#######################################

## Generate messages in the 'msg' folder
 add_message_files(
   FILES
   Channels.msg
 )

## Generate services in the 'srv' folder
 add_service_files(
   FILES
   Stim.srv
 )

## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   std_msgs
 )

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if you package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
   INCLUDE_DIRS include
#  LIBRARIES zanni
   CATKIN_DEPENDS roscpp std_msgs message_runtime
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
)

## Declare a cpp library
# add_library(zanni
#   src/${PROJECT_NAME}/zanni.cpp
# )


## Declare a cpp executable
# The dish reader and publisher
add_executable(zanni src/zanni.cpp)
add_dependencies(zanni ${catkin_EXPORTED_TARGETS} zanni_generate_messages)
target_link_libraries(zanni ${catkin_LIBRARIES} comedi)

# The stimulation server
add_executable(zanni_stim_server src/zanni_stim.cpp)
add_dependencies(zanni_stim_server ${catkin_EXPORTED_TARGETS})
target_link_libraries(zanni_stim_server ${catkin_LIBRARIES} comedi)

# A test listener for the dish reader
add_executable(zanni_listener src/zanni_listener.cpp)
add_dependencies(zanni_listener ${catkin_EXPORTED_TARGETS} zanni_generate_messages)
target_link_libraries(zanni_listener ${catkin_LIBRARIES} ncurses)

# A test client for the stimulation server
add_executable(zanni_stim_client src/zanni_stim_client.cpp)
add_dependencies(zanni_stim_client ${catkin_EXPORTED_TARGETS} )
target_link_libraries(zanni_stim_client ${catkin_LIBRARIES})

# Translator into dish states for arm control
#include_directories("../../../../arm_project/neuro_recv/msg_gen/cpp/include/")
add_executable(zanni_translate src/zanni_to_dishstate.cpp)
add_dependencies(zanni_translate ${catkin_EXPORTED_TARGETS} zanni_generate_messages)
target_link_libraries(zanni_translate ${catkin_LIBRARIES})

## Specify libraries to link a library or executable target against
# target_link_libraries(zanni_node
#   ${catkin_LIBRARIES}
# )

#############
## Install ##
#############

# all install targets should use catkin DESTINATION variables
# See http://ros.org/doc/api/catkin/html/adv_user_guide/variables.html

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
# install(PROGRAMS
#   scripts/my_python_script
#   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

## Mark executables and/or libraries for installation
# install(TARGETS zanni zanni_node
#   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

## Mark cpp header files for installation
# install(DIRECTORY include/${PROJECT_NAME}/
#   DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
#   FILES_MATCHING PATTERN "*.h"
#   PATTERN ".svn" EXCLUDE
# )

## Mark other files for installation (e.g. launch and bag files, etc.)
# install(FILES
#   # myfile1
#   # myfile2
#   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
# )

#############
## Testing ##
#############

## Add gtest based cpp test target and link libraries
# catkin_add_gtest(${PROJECT_NAME}-test test/test_zanni.cpp)
# if(TARGET ${PROJECT_NAME}-test)
#   target_link_libraries(${PROJECT_NAME}-test ${PROJECT_NAME})
# endif()

## Add folders to be run by python nosetests
# catkin_add_nosetests(test)
