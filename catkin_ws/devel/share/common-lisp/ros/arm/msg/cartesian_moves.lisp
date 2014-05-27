; Auto-generated. Do not edit!


(cl:in-package arm-msg)


;//! \htmlinclude cartesian_moves.msg.html

(cl:defclass <cartesian_moves> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (end
    :reader end
    :initarg :end
    :type cl:real
    :initform 0)
   (moves
    :reader moves
    :initarg :moves
    :type (cl:vector arm-msg:cartesian_move)
   :initform (cl:make-array 0 :element-type 'arm-msg:cartesian_move :initial-element (cl:make-instance 'arm-msg:cartesian_move))))
)

(cl:defclass cartesian_moves (<cartesian_moves>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <cartesian_moves>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'cartesian_moves)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name arm-msg:<cartesian_moves> is deprecated: use arm-msg:cartesian_moves instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <cartesian_moves>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:header-val is deprecated.  Use arm-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'end-val :lambda-list '(m))
(cl:defmethod end-val ((m <cartesian_moves>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:end-val is deprecated.  Use arm-msg:end instead.")
  (end m))

(cl:ensure-generic-function 'moves-val :lambda-list '(m))
(cl:defmethod moves-val ((m <cartesian_moves>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:moves-val is deprecated.  Use arm-msg:moves instead.")
  (moves m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <cartesian_moves>) ostream)
  "Serializes a message object of type '<cartesian_moves>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__sec (cl:floor (cl:slot-value msg 'end)))
        (__nsec (cl:round (cl:* 1e9 (cl:- (cl:slot-value msg 'end) (cl:floor (cl:slot-value msg 'end)))))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 0) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __nsec) ostream))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'moves))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'moves))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <cartesian_moves>) istream)
  "Deserializes a message object of type '<cartesian_moves>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((__sec 0) (__nsec 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 0) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __nsec) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'end) (cl:+ (cl:coerce __sec 'cl:double-float) (cl:/ __nsec 1e9))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'moves) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'moves)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'arm-msg:cartesian_move))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<cartesian_moves>)))
  "Returns string type for a message object of type '<cartesian_moves>"
  "arm/cartesian_moves")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'cartesian_moves)))
  "Returns string type for a message object of type 'cartesian_moves"
  "arm/cartesian_moves")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<cartesian_moves>)))
  "Returns md5sum for a message object of type '<cartesian_moves>"
  "56c11a250225b8cc4f58b0e6670caaa1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'cartesian_moves)))
  "Returns md5sum for a message object of type 'cartesian_moves"
  "56c11a250225b8cc4f58b0e6670caaa1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<cartesian_moves>)))
  "Returns full string definition for message of type '<cartesian_moves>"
  (cl:format cl:nil "# Cartesian movement sequence message~%Header header~%time end~%cartesian_move[] moves~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: arm/cartesian_move~%# Cartesian movement message~%Header header~%float32[7] positions~%int8[7] speeds~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'cartesian_moves)))
  "Returns full string definition for message of type 'cartesian_moves"
  (cl:format cl:nil "# Cartesian movement sequence message~%Header header~%time end~%cartesian_move[] moves~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: arm/cartesian_move~%# Cartesian movement message~%Header header~%float32[7] positions~%int8[7] speeds~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <cartesian_moves>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     8
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'moves) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <cartesian_moves>))
  "Converts a ROS message object to a list"
  (cl:list 'cartesian_moves
    (cl:cons ':header (header msg))
    (cl:cons ':end (end msg))
    (cl:cons ':moves (moves msg))
))
