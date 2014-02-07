cmake_minimum_required(VERSION 2.4.6)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

# Set the build type.  Options are:
#  Coverage       : w/ debug symbols, w/o optimization, w/ code-coverage
#  Debug          : w/ debug symbols, w/o optimization
#  Release        : w/o debug symbols, w/ optimization
#  RelWithDebInfo : w/ debug symbols, w/ optimization
#  MinSizeRel     : w/o debug symbols, w/ optimization, stripped binaries
#set(ROS_BUILD_TYPE RelWithDebInfo)

rosbuild_init()

#set the default path for built executables to the "bin" directory
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
#set the default path for built libraries to the "lib" directory
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

#uncomment if you have defined messages
#rosbuild_genmsg()
#uncomment if you have defined services
rosbuild_gensrv()

#common commands for building c++ executables and libraries
#rosbuild_add_library(${PROJECT_NAME} src/example.cpp)
#target_link_libraries(${PROJECT_NAME} another_library)
#rosbuild_add_boost_directories()
#rosbuild_link_boost(${PROJECT_NAME} thread)


rosbuild_add_executable(img_slicer src/ImageSlicer.cpp)
rosbuild_add_library(practical_socket ../../common/PracticalSocket.cpp)

rosbuild_add_executable(slicer_test src/slicerTest.cpp)
target_link_libraries(slicer_test plotter Xaw Xmu Xt SM ICE Xext X11 png z m practical_socket)

include_directories("../../zanni/catkin_ws/devel/include/" "../../zanni/catkin_ws/src/zanni/src/")
rosbuild_add_executable(zanni_slices src/slicerToZanni.cpp)
target_link_libraries(zanni_slices plotter Xaw Xmu Xt SM ICE Xext X11 png z m)

#target_link_libraries(example ${PROJECT_NAME})
