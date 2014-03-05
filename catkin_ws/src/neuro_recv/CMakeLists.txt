cmake_minimum_required(VERSION 2.8.3)
project(neuro_recv)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  practical_socket
  message_generation
)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  dish_state.msg
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
#  LIBRARIES neuro_recv
  CATKIN_DEPENDS roscpp message_runtime
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

# Yes, those add_dependencies lines say that you have to build the messages
# for this node before building the code. 
# Yes, catkin is a shitshow. 
add_executable(net_recv src/net_recv.cpp)
add_dependencies(net_recv neuro_recv_generate_messages practical_socket)
target_link_libraries(net_recv ${catkin_LIBRARIES})

add_executable(csv_recv src/csv_recv.cpp)
add_dependencies(csv_recv neuro_recv_generate_messages practical_socket)
target_link_libraries(csv_recv ${catkin_LIBRARIES})

add_executable(mock_recv src/mock_recv.cpp)
add_dependencies(mock_recv neuro_recv_generate_messages practical_socket)
target_link_libraries(mock_recv ${catkin_LIBRARIES})

