cmake_minimum_required(VERSION 2.8.3)
project(burst_calc)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  message_generation
  std_msgs
  time_server
  neuro_recv
)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  burst.msg  
  ca.msg  
  cat.msg  
  ranges.msg
)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
  neuro_recv
  time_server
)

catkin_package(
   INCLUDE_DIRS include
   LIBRARIES buffer_spike_detector
#  CATKIN_DEPENDS roscpp
#  DEPENDS system_lib
)

###########
## Build ##
###########

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

# The burst creator
add_executable(burst_creator src/burst_creator.cpp)
add_library(buffer_spike_detector src/buffer_spike_detector.cpp)
add_library(burst_checker src/burst_checker.cpp)
add_library(burst_merger src/burst_merger.cpp)
target_link_libraries(burst_creator buffer_spike_detector burst_checker burst_merger ${catkin_LIBRARIES})

# CAT creator
add_executable(cat_creator src/cat_creator.cpp)
target_link_libraries(cat_creator ${catkin_LIBRARIES})

