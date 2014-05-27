# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "neuro_recv: 1 messages, 0 services")

set(MSG_I_FLAGS "-Ineuro_recv:/home/dpickler/Work/neurobotics/catkin_ws/src/neuro_recv/msg;-Istd_msgs:/opt/ros/hydro/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(neuro_recv_generate_messages ALL)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(neuro_recv
  "/home/dpickler/Work/neurobotics/catkin_ws/src/neuro_recv/msg/dish_state.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/neuro_recv
)

### Generating Services

### Generating Module File
_generate_module_cpp(neuro_recv
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/neuro_recv
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(neuro_recv_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(neuro_recv_generate_messages neuro_recv_generate_messages_cpp)

# target for backward compatibility
add_custom_target(neuro_recv_gencpp)
add_dependencies(neuro_recv_gencpp neuro_recv_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS neuro_recv_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(neuro_recv
  "/home/dpickler/Work/neurobotics/catkin_ws/src/neuro_recv/msg/dish_state.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/neuro_recv
)

### Generating Services

### Generating Module File
_generate_module_lisp(neuro_recv
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/neuro_recv
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(neuro_recv_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(neuro_recv_generate_messages neuro_recv_generate_messages_lisp)

# target for backward compatibility
add_custom_target(neuro_recv_genlisp)
add_dependencies(neuro_recv_genlisp neuro_recv_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS neuro_recv_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(neuro_recv
  "/home/dpickler/Work/neurobotics/catkin_ws/src/neuro_recv/msg/dish_state.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/neuro_recv
)

### Generating Services

### Generating Module File
_generate_module_py(neuro_recv
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/neuro_recv
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(neuro_recv_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(neuro_recv_generate_messages neuro_recv_generate_messages_py)

# target for backward compatibility
add_custom_target(neuro_recv_genpy)
add_dependencies(neuro_recv_genpy neuro_recv_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS neuro_recv_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/neuro_recv)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/neuro_recv
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(neuro_recv_generate_messages_cpp std_msgs_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/neuro_recv)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/neuro_recv
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(neuro_recv_generate_messages_lisp std_msgs_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/neuro_recv)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/neuro_recv\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/neuro_recv
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(neuro_recv_generate_messages_py std_msgs_generate_messages_py)
