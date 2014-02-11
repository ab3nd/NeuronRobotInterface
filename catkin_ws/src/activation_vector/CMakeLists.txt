cmake_minimum_required(VERSION 2.8.3)
project(activation_vector)

find_package(catkin REQUIRED COMPONENTS roscpp burst_calc neuro_recv arm)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES activation_vector
#  CATKIN_DEPENDS other_catkin_pkg
#  DEPENDS system_lib
)

###########
## Build ##
###########

include_directories(include ${catkin_INCLUDE_DIRS}) 

#The activation vector controller node
add_executable(act_vector src/act_vector.cpp)
target_link_libraries(act_vector ${catkin_LIBRARIES} buffer_spike_detector)

