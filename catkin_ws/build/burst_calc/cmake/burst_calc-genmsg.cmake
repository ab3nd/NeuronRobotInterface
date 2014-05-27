# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "burst_calc: 4 messages, 0 services")

set(MSG_I_FLAGS "-Iburst_calc:/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg;-Istd_msgs:/opt/ros/hydro/share/std_msgs/cmake/../msg;-Ineuro_recv:/home/dpickler/Work/neurobotics/catkin_ws/src/neuro_recv/msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(genlisp REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(burst_calc_generate_messages ALL)

#
#  langs = gencpp;genlisp;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/ca.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/burst_calc
)
_generate_msg_cpp(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/burst.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg;/home/dpickler/Work/neurobotics/catkin_ws/src/neuro_recv/msg/dish_state.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/burst_calc
)
_generate_msg_cpp(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/ranges.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/burst_calc
)
_generate_msg_cpp(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/cat.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg;/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/ca.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/burst_calc
)

### Generating Services

### Generating Module File
_generate_module_cpp(burst_calc
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/burst_calc
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(burst_calc_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(burst_calc_generate_messages burst_calc_generate_messages_cpp)

# target for backward compatibility
add_custom_target(burst_calc_gencpp)
add_dependencies(burst_calc_gencpp burst_calc_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS burst_calc_generate_messages_cpp)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/ca.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/burst_calc
)
_generate_msg_lisp(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/burst.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg;/home/dpickler/Work/neurobotics/catkin_ws/src/neuro_recv/msg/dish_state.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/burst_calc
)
_generate_msg_lisp(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/ranges.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/burst_calc
)
_generate_msg_lisp(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/cat.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg;/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/ca.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/burst_calc
)

### Generating Services

### Generating Module File
_generate_module_lisp(burst_calc
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/burst_calc
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(burst_calc_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(burst_calc_generate_messages burst_calc_generate_messages_lisp)

# target for backward compatibility
add_custom_target(burst_calc_genlisp)
add_dependencies(burst_calc_genlisp burst_calc_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS burst_calc_generate_messages_lisp)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/ca.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/burst_calc
)
_generate_msg_py(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/burst.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg;/home/dpickler/Work/neurobotics/catkin_ws/src/neuro_recv/msg/dish_state.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/burst_calc
)
_generate_msg_py(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/ranges.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/burst_calc
)
_generate_msg_py(burst_calc
  "/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/cat.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/hydro/share/std_msgs/cmake/../msg/Header.msg;/home/dpickler/Work/neurobotics/catkin_ws/src/burst_calc/msg/ca.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/burst_calc
)

### Generating Services

### Generating Module File
_generate_module_py(burst_calc
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/burst_calc
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(burst_calc_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(burst_calc_generate_messages burst_calc_generate_messages_py)

# target for backward compatibility
add_custom_target(burst_calc_genpy)
add_dependencies(burst_calc_genpy burst_calc_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS burst_calc_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/burst_calc)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/burst_calc
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
add_dependencies(burst_calc_generate_messages_cpp std_msgs_generate_messages_cpp)
add_dependencies(burst_calc_generate_messages_cpp neuro_recv_generate_messages_cpp)

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/burst_calc)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/burst_calc
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
add_dependencies(burst_calc_generate_messages_lisp std_msgs_generate_messages_lisp)
add_dependencies(burst_calc_generate_messages_lisp neuro_recv_generate_messages_lisp)

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/burst_calc)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/burst_calc\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/burst_calc
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
add_dependencies(burst_calc_generate_messages_py std_msgs_generate_messages_py)
add_dependencies(burst_calc_generate_messages_py neuro_recv_generate_messages_py)
