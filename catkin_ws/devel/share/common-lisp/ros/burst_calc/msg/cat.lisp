; Auto-generated. Do not edit!


(cl:in-package burst_calc-msg)


;//! \htmlinclude cat.msg.html

(cl:defclass <cat> (roslisp-msg-protocol:ros-message)
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
   (channels
    :reader channels
    :initarg :channels
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 0 :element-type 'cl:fixnum :initial-element 0))
   (cas
    :reader cas
    :initarg :cas
    :type (cl:vector burst_calc-msg:ca)
   :initform (cl:make-array 0 :element-type 'burst_calc-msg:ca :initial-element (cl:make-instance 'burst_calc-msg:ca))))
)

(cl:defclass cat (<cat>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <cat>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'cat)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name burst_calc-msg:<cat> is deprecated: use burst_calc-msg:cat instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <cat>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:header-val is deprecated.  Use burst_calc-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'end-val :lambda-list '(m))
(cl:defmethod end-val ((m <cat>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:end-val is deprecated.  Use burst_calc-msg:end instead.")
  (end m))

(cl:ensure-generic-function 'channels-val :lambda-list '(m))
(cl:defmethod channels-val ((m <cat>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:channels-val is deprecated.  Use burst_calc-msg:channels instead.")
  (channels m))

(cl:ensure-generic-function 'cas-val :lambda-list '(m))
(cl:defmethod cas-val ((m <cat>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:cas-val is deprecated.  Use burst_calc-msg:cas instead.")
  (cas m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <cat>) ostream)
  "Serializes a message object of type '<cat>"
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
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'channels))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    ))
   (cl:slot-value msg 'channels))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'cas))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'cas))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <cat>) istream)
  "Deserializes a message object of type '<cat>"
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
  (cl:setf (cl:slot-value msg 'channels) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'channels)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256)))))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'cas) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'cas)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'burst_calc-msg:ca))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<cat>)))
  "Returns string type for a message object of type '<cat>"
  "burst_calc/cat")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'cat)))
  "Returns string type for a message object of type 'cat"
  "burst_calc/cat")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<cat>)))
  "Returns md5sum for a message object of type '<cat>"
  "a9e7efbd18f40d368e9f31f27d0c183b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'cat)))
  "Returns md5sum for a message object of type 'cat"
  "a9e7efbd18f40d368e9f31f27d0c183b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<cat>)))
  "Returns full string definition for message of type '<cat>"
  (cl:format cl:nil "# Center of activity trajectory message~%Header header~%time end~%int8[] channels~%ca[] cas~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: burst_calc/ca~%# Center of activity message~%Header header~%float64 x~%float64 y ~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'cat)))
  "Returns full string definition for message of type 'cat"
  (cl:format cl:nil "# Center of activity trajectory message~%Header header~%time end~%int8[] channels~%ca[] cas~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: burst_calc/ca~%# Center of activity message~%Header header~%float64 x~%float64 y ~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <cat>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     8
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'channels) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'cas) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <cat>))
  "Converts a ROS message object to a list"
  (cl:list 'cat
    (cl:cons ':header (header msg))
    (cl:cons ':end (end msg))
    (cl:cons ':channels (channels msg))
    (cl:cons ':cas (cas msg))
))
