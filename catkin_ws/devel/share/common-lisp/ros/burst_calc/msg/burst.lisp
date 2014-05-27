; Auto-generated. Do not edit!


(cl:in-package burst_calc-msg)


;//! \htmlinclude burst.msg.html

(cl:defclass <burst> (roslisp-msg-protocol:ros-message)
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
   (dishes
    :reader dishes
    :initarg :dishes
    :type (cl:vector neuro_recv-msg:dish_state)
   :initform (cl:make-array 0 :element-type 'neuro_recv-msg:dish_state :initial-element (cl:make-instance 'neuro_recv-msg:dish_state))))
)

(cl:defclass burst (<burst>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <burst>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'burst)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name burst_calc-msg:<burst> is deprecated: use burst_calc-msg:burst instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <burst>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:header-val is deprecated.  Use burst_calc-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'end-val :lambda-list '(m))
(cl:defmethod end-val ((m <burst>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:end-val is deprecated.  Use burst_calc-msg:end instead.")
  (end m))

(cl:ensure-generic-function 'channels-val :lambda-list '(m))
(cl:defmethod channels-val ((m <burst>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:channels-val is deprecated.  Use burst_calc-msg:channels instead.")
  (channels m))

(cl:ensure-generic-function 'dishes-val :lambda-list '(m))
(cl:defmethod dishes-val ((m <burst>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:dishes-val is deprecated.  Use burst_calc-msg:dishes instead.")
  (dishes m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <burst>) ostream)
  "Serializes a message object of type '<burst>"
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
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'dishes))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'dishes))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <burst>) istream)
  "Deserializes a message object of type '<burst>"
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
  (cl:setf (cl:slot-value msg 'dishes) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'dishes)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'neuro_recv-msg:dish_state))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<burst>)))
  "Returns string type for a message object of type '<burst>"
  "burst_calc/burst")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'burst)))
  "Returns string type for a message object of type 'burst"
  "burst_calc/burst")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<burst>)))
  "Returns md5sum for a message object of type '<burst>"
  "9fc444266caceed83ebba28b36c432e7")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'burst)))
  "Returns md5sum for a message object of type 'burst"
  "9fc444266caceed83ebba28b36c432e7")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<burst>)))
  "Returns full string definition for message of type '<burst>"
  (cl:format cl:nil "# Burst message~%Header header~%time end~%int8[] channels~%neuro_recv/dish_state[] dishes~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: neuro_recv/dish_state~%# Dish state message~%Header header~%float64[60] samples~%bool last_dish~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'burst)))
  "Returns full string definition for message of type 'burst"
  (cl:format cl:nil "# Burst message~%Header header~%time end~%int8[] channels~%neuro_recv/dish_state[] dishes~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: neuro_recv/dish_state~%# Dish state message~%Header header~%float64[60] samples~%bool last_dish~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <burst>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     8
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'channels) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'dishes) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <burst>))
  "Converts a ROS message object to a list"
  (cl:list 'burst
    (cl:cons ':header (header msg))
    (cl:cons ':end (end msg))
    (cl:cons ':channels (channels msg))
    (cl:cons ':dishes (dishes msg))
))
