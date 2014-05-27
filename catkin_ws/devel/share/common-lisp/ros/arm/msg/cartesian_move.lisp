; Auto-generated. Do not edit!


(cl:in-package arm-msg)


;//! \htmlinclude cartesian_move.msg.html

(cl:defclass <cartesian_move> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (positions
    :reader positions
    :initarg :positions
    :type (cl:vector cl:float)
   :initform (cl:make-array 7 :element-type 'cl:float :initial-element 0.0))
   (speeds
    :reader speeds
    :initarg :speeds
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 7 :element-type 'cl:fixnum :initial-element 0)))
)

(cl:defclass cartesian_move (<cartesian_move>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <cartesian_move>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'cartesian_move)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name arm-msg:<cartesian_move> is deprecated: use arm-msg:cartesian_move instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <cartesian_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:header-val is deprecated.  Use arm-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'positions-val :lambda-list '(m))
(cl:defmethod positions-val ((m <cartesian_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:positions-val is deprecated.  Use arm-msg:positions instead.")
  (positions m))

(cl:ensure-generic-function 'speeds-val :lambda-list '(m))
(cl:defmethod speeds-val ((m <cartesian_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:speeds-val is deprecated.  Use arm-msg:speeds instead.")
  (speeds m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <cartesian_move>) ostream)
  "Serializes a message object of type '<cartesian_move>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'positions))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    ))
   (cl:slot-value msg 'speeds))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <cartesian_move>) istream)
  "Deserializes a message object of type '<cartesian_move>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:setf (cl:slot-value msg 'positions) (cl:make-array 7))
  (cl:let ((vals (cl:slot-value msg 'positions)))
    (cl:dotimes (i 7)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits)))))
  (cl:setf (cl:slot-value msg 'speeds) (cl:make-array 7))
  (cl:let ((vals (cl:slot-value msg 'speeds)))
    (cl:dotimes (i 7)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<cartesian_move>)))
  "Returns string type for a message object of type '<cartesian_move>"
  "arm/cartesian_move")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'cartesian_move)))
  "Returns string type for a message object of type 'cartesian_move"
  "arm/cartesian_move")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<cartesian_move>)))
  "Returns md5sum for a message object of type '<cartesian_move>"
  "77c36474a679935981d0084acfe955fd")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'cartesian_move)))
  "Returns md5sum for a message object of type 'cartesian_move"
  "77c36474a679935981d0084acfe955fd")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<cartesian_move>)))
  "Returns full string definition for message of type '<cartesian_move>"
  (cl:format cl:nil "# Cartesian movement message~%Header header~%float32[7] positions~%int8[7] speeds~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'cartesian_move)))
  "Returns full string definition for message of type 'cartesian_move"
  (cl:format cl:nil "# Cartesian movement message~%Header header~%float32[7] positions~%int8[7] speeds~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <cartesian_move>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'positions) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'speeds) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <cartesian_move>))
  "Converts a ROS message object to a list"
  (cl:list 'cartesian_move
    (cl:cons ':header (header msg))
    (cl:cons ':positions (positions msg))
    (cl:cons ':speeds (speeds msg))
))
