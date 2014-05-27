# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/dpickler/Work/neurobotics/catkin_ws/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/dpickler/Work/neurobotics/catkin_ws/build

# Include any dependencies generated for this target.
include burst_calc/CMakeFiles/burst_merger.dir/depend.make

# Include the progress variables for this target.
include burst_calc/CMakeFiles/burst_merger.dir/progress.make

# Include the compile flags for this target's objects.
include burst_calc/CMakeFiles/burst_merger.dir/flags.make

burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o: burst_calc/CMakeFiles/burst_merger.dir/flags.make
burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o: /home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/src/burst_merger.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/dpickler/Work/neurobotics/catkin_ws/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o"
	cd /home/dpickler/Work/neurobotics/catkin_ws/build/burst_calc && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o -c /home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/src/burst_merger.cpp

burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/burst_merger.dir/src/burst_merger.cpp.i"
	cd /home/dpickler/Work/neurobotics/catkin_ws/build/burst_calc && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/src/burst_merger.cpp > CMakeFiles/burst_merger.dir/src/burst_merger.cpp.i

burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/burst_merger.dir/src/burst_merger.cpp.s"
	cd /home/dpickler/Work/neurobotics/catkin_ws/build/burst_calc && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/src/burst_merger.cpp -o CMakeFiles/burst_merger.dir/src/burst_merger.cpp.s

burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o.requires:
.PHONY : burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o.requires

burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o.provides: burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o.requires
	$(MAKE) -f burst_calc/CMakeFiles/burst_merger.dir/build.make burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o.provides.build
.PHONY : burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o.provides

burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o.provides.build: burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o

# Object files for target burst_merger
burst_merger_OBJECTS = \
"CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o"

# External object files for target burst_merger
burst_merger_EXTERNAL_OBJECTS =

/home/dpickler/Work/neurobotics/catkin_ws/devel/lib/libburst_merger.so: burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o
/home/dpickler/Work/neurobotics/catkin_ws/devel/lib/libburst_merger.so: burst_calc/CMakeFiles/burst_merger.dir/build.make
/home/dpickler/Work/neurobotics/catkin_ws/devel/lib/libburst_merger.so: burst_calc/CMakeFiles/burst_merger.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX shared library /home/dpickler/Work/neurobotics/catkin_ws/devel/lib/libburst_merger.so"
	cd /home/dpickler/Work/neurobotics/catkin_ws/build/burst_calc && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/burst_merger.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
burst_calc/CMakeFiles/burst_merger.dir/build: /home/dpickler/Work/neurobotics/catkin_ws/devel/lib/libburst_merger.so
.PHONY : burst_calc/CMakeFiles/burst_merger.dir/build

burst_calc/CMakeFiles/burst_merger.dir/requires: burst_calc/CMakeFiles/burst_merger.dir/src/burst_merger.cpp.o.requires
.PHONY : burst_calc/CMakeFiles/burst_merger.dir/requires

burst_calc/CMakeFiles/burst_merger.dir/clean:
	cd /home/dpickler/Work/neurobotics/catkin_ws/build/burst_calc && $(CMAKE_COMMAND) -P CMakeFiles/burst_merger.dir/cmake_clean.cmake
.PHONY : burst_calc/CMakeFiles/burst_merger.dir/clean

burst_calc/CMakeFiles/burst_merger.dir/depend:
	cd /home/dpickler/Work/neurobotics/catkin_ws/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/dpickler/Work/neurobotics/catkin_ws/src /home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc /home/dpickler/Work/neurobotics/catkin_ws/build /home/dpickler/Work/neurobotics/catkin_ws/build/burst_calc /home/dpickler/Work/neurobotics/catkin_ws/build/burst_calc/CMakeFiles/burst_merger.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : burst_calc/CMakeFiles/burst_merger.dir/depend

