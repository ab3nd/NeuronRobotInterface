# generated from genmsg/cmake/pkg-msg-paths.cmake.em

# message include dirs in installspace
_prepend_path("${arm_DIR}/.." "msg" arm_MSG_INCLUDE_DIRS UNIQUE)
set(arm_MSG_DEPENDENCIES std_msgs;time_server)
