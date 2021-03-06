cmake_minimum_required(VERSION 2.8.3)
project(arm)

find_package(catkin REQUIRED COMPONENTS
   roscpp
   message_generation
   std_msgs
   time_server
)

################################################
## Declare ROS messages, services and actions ##
################################################

## To declare and build messages, services or actions from within this
## package, follow these steps:
## * Let MSG_DEP_SET be the set of packages whose message types you use in
##   your messages/services/actions (e.g. std_msgs, actionlib_msgs, ...).
## * In the file package.xml:
##   * add a build_depend and a run_depend tag for each package in MSG_DEP_SET
##   * If MSG_DEP_SET isn't empty the following dependencies might have been
##     pulled in transitively but can be declared for certainty nonetheless:
##     * add a build_depend tag for "message_generation"
##     * add a run_depend tag for "message_runtime"
## * In this file (CMakeLists.txt):
##   * add "message_generation" and every package in MSG_DEP_SET to
##     find_package(catkin REQUIRED COMPONENTS ...)
##   * add "message_runtime" and every package in MSG_DEP_SET to
##     catkin_package(CATKIN_DEPENDS ...)
##   * uncomment the add_*_files sections below as needed
##     and list every .msg/.srv/.action file to be processed
##   * uncomment the generate_messages entry below
##   * add every package in MSG_DEP_SET to generate_messages(DEPENDENCIES ...)

## Generate messages in the 'msg' folder
add_message_files(
   FILES
   cartesian_move.msg
   cartesian_moves.msg
   constant_move.msg
   constant_move_time.msg
)

## Generate added messages and services with any dependencies listed here
generate_messages(
   DEPENDENCIES
   std_msgs
   time_server
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
#  LIBRARIES arm
#  CATKIN_DEPENDS other_catkin_pkg
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

## Part that actually controls the movement of the arm
add_executable(arm_control src/arm_control.cpp)
add_dependencies(arm_control burst_calc_generate_messages)
add_dependencies(arm_control arm_generate_messages)
target_link_libraries(arm_control ${catkin_LIBRARIES})

add_library(ManusArm src/ManusArm.cpp)
target_link_libraries(arm_control ManusArm)

## Control the arm from the keyboard
add_executable(teleop_arm_key src/teleop_arm_key.cpp)
add_dependencies(teleop_arm_key burst_calc_generate_messages)
add_dependencies(teleop_arm_key arm_generate_messages)
target_link_libraries(teleop_arm_key ${catkin_LIBRARIES})

## Control the arm from a MEA
add_executable(teleop_arm_dish src/teleop_arm_dish.cpp)
add_dependencies(teleop_arm_dish burst_calc_generate_messages)
add_dependencies(teleop_arm_dish arm_generate_messages)
target_link_libraries(teleop_arm_dish ${catkin_LIBRARIES})


