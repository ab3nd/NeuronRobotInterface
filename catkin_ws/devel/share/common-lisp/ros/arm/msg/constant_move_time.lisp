; Auto-generated. Do not edit!


(cl:in-package arm-msg)


;//! \htmlinclude constant_move_time.msg.html

(cl:defclass <constant_move_time> (roslisp-msg-protocol:ros-message)
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
   (move
    :reader move
    :initarg :move
    :type arm-msg:constant_move
    :initform (cl:make-instance 'arm-msg:constant_move)))
)

(cl:defclass constant_move_time (<constant_move_time>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <constant_move_time>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'constant_move_time)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name arm-msg:<constant_move_time> is deprecated: use arm-msg:constant_move_time instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <constant_move_time>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:header-val is deprecated.  Use arm-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'end-val :lambda-list '(m))
(cl:defmethod end-val ((m <constant_move_time>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:end-val is deprecated.  Use arm-msg:end instead.")
  (end m))

(cl:ensure-generic-function 'move-val :lambda-list '(m))
(cl:defmethod move-val ((m <constant_move_time>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:move-val is deprecated.  Use arm-msg:move instead.")
  (move m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <constant_move_time>) ostream)
  "Serializes a message object of type '<constant_move_time>"
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
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'move) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <constant_move_time>) istream)
  "Deserializes a message object of type '<constant_move_time>"
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
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'move) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<constant_move_time>)))
  "Returns string type for a message object of type '<constant_move_time>"
  "arm/constant_move_time")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'constant_move_time)))
  "Returns string type for a message object of type 'constant_move_time"
  "arm/constant_move_time")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<constant_move_time>)))
  "Returns md5sum for a message object of type '<constant_move_time>"
  "ce3f840cc123698b1457e9ca4641494a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'constant_move_time)))
  "Returns md5sum for a message object of type 'constant_move_time"
  "ce3f840cc123698b1457e9ca4641494a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<constant_move_time>)))
  "Returns full string definition for message of type '<constant_move_time>"
  (cl:format cl:nil "# Constant movement by time message~%Header header~%time end~%constant_move move~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: arm/constant_move~%# Constant movement message~%Header header~%int8[8] states~%int8[7] speeds~%bool query~%bool quit~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'constant_move_time)))
  "Returns full string definition for message of type 'constant_move_time"
  (cl:format cl:nil "# Constant movement by time message~%Header header~%time end~%constant_move move~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: arm/constant_move~%# Constant movement message~%Header header~%int8[8] states~%int8[7] speeds~%bool query~%bool quit~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <constant_move_time>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     8
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'move))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <constant_move_time>))
  "Converts a ROS message object to a list"
  (cl:list 'constant_move_time
    (cl:cons ':header (header msg))
    (cl:cons ':end (end msg))
    (cl:cons ':move (move msg))
))
