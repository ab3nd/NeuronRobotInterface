cmake_minimum_required(VERSION 2.8.3)
project(burst_calc)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  message_generation
  neuro_recv
  std_msgs
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
)

catkin_package(
   INCLUDE_DIRS include
   LIBRARIES buffer_spike_detector
   CATKIN_DEPENDS roscpp message_runtime
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
add_dependencies(burst_creator neuro_recv_generate_messages_cpp)
add_library(buffer_spike_detector src/buffer_spike_detector.cpp)
add_library(burst_checker src/burst_checker.cpp)
add_library(burst_merger src/burst_merger.cpp)
target_link_libraries(burst_creator buffer_spike_detector burst_checker burst_merger ${catkin_LIBRARIES})

# CAT creator
add_executable(cat_creator src/cat_creator.cpp)
add_dependencies(cat_creator neuro_recv_generate_messages_cpp)
target_link_libraries(cat_creator ${catkin_LIBRARIES})

