# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "zanni: 1 messages, 1 services")

set(MSG_I_FLAGS "-Izanni:/home/dpickler/Work/neurobotics/catkin_ws/src/zanni/msg;-Istd_msgs:/opt/ros/hydro/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(zanni_generate_messages ALL)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(zanni
  "/home/dpickler/Work/neurobotics/catkin_ws/src/zanni/msg/Channels.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/zanni
)

### Generating Services
_generate_srv_cpp(zanni
  "/home/dpickler/Work/neurobotics/catkin_ws/src/zanni/srv/Stim.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/zanni
)

### Generating Module File
_generate_module_cpp(zanni
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/zanni
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(zanni_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(zanni_generate_messages zanni_generate_messages_cpp)

# target for backward compatibility
add_custom_target(zanni_gencpp)
add_dependencies(zanni_gencpp zanni_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS zanni_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(zanni
  "/home/dpickler/Work/neurobotics/catkin_ws/src/zanni/msg/Channels.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/zanni
)

### Generating Services
_generate_srv_lisp(zanni
  "/home/dpickler/Work/neurobotics/catkin_ws/src/zanni/srv/Stim.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/zanni
)

### Generating Module File
_generate_module_lisp(zanni
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/zanni
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(zanni_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(zanni_generate_messages zanni_generate_messages_lisp)

# target for backward compatibility
add_custom_target(zanni_genlisp)
add_dependencies(zanni_genlisp zanni_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS zanni_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(zanni
  "/home/dpickler/Work/neurobotics/catkin_ws/src/zanni/msg/Channels.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/zanni
)

### Generating Services
_generate_srv_py(zanni
  "/home/dpickler/Work/neurobotics/catkin_ws/src/zanni/srv/Stim.srv"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/zanni
)

### Generating Module File
_generate_module_py(zanni
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/zanni
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(zanni_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(zanni_generate_messages zanni_generate_messages_py)

# target for backward compatibility
add_custom_target(zanni_genpy)
add_dependencies(zanni_genpy zanni_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS zanni_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/zanni)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/zanni
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(zanni_generate_messages_cpp std_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/zanni)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/zanni
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(zanni_generate_messages_lisp std_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/zanni)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/zanni\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/zanni
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(zanni_generate_messages_py std_msgs_generate_messages_py)
