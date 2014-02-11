cmake_minimum_required(VERSION 2.8.3)
project(volt_distr)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  neuro_recv  
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES volt_distr
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

add_executable(volt_distr src/volt_distr.cpp)
add_dependencies(volt_distr neuro_recv_generate_messages)
add_library(volt_distr_creator src/volt_distr_creator.cpp)
add_dependencies(volt_distr_creator neuro_recv_generate_messages)
add_library(volt_distr_viz src/volt_distr_viz.cpp)
add_dependencies(volt_distr_viz neuro_recv_generate_messages)
target_link_libraries(volt_distr_viz plotter Xaw Xmu Xt SM ICE Xext X11 png z m ${catkin_LIBRARIES})
target_link_libraries(volt_distr volt_distr_creator volt_distr_viz ${catkin_LIBRARIES})

