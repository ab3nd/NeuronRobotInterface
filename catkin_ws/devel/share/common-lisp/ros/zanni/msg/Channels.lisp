; Auto-generated. Do not edit!


(cl:in-package zanni-msg)


;//! \htmlinclude Channels.msg.html

(cl:defclass <Channels> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (voltages
    :reader voltages
    :initarg :voltages
    :type (cl:vector cl:float)
   :initform (cl:make-array 64 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass Channels (<Channels>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Channels>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Channels)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name zanni-msg:<Channels> is deprecated: use zanni-msg:Channels instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <Channels>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader zanni-msg:header-val is deprecated.  Use zanni-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'voltages-val :lambda-list '(m))
(cl:defmethod voltages-val ((m <Channels>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader zanni-msg:voltages-val is deprecated.  Use zanni-msg:voltages instead.")
  (voltages m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Channels>) ostream)
  "Serializes a message object of type '<Channels>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'voltages))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Channels>) istream)
  "Deserializes a message object of type '<Channels>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:setf (cl:slot-value msg 'voltages) (cl:make-array 64))
  (cl:let ((vals (cl:slot-value msg 'voltages)))
    (cl:dotimes (i 64)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Channels>)))
  "Returns string type for a message object of type '<Channels>"
  "zanni/Channels")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Channels)))
  "Returns string type for a message object of type 'Channels"
  "zanni/Channels")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Channels>)))
  "Returns md5sum for a message object of type '<Channels>"
  "4ba4d67545a8fff72339631e17bfda86")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Channels)))
  "Returns md5sum for a message object of type 'Channels"
  "4ba4d67545a8fff72339631e17bfda86")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Channels>)))
  "Returns full string definition for message of type '<Channels>"
  (cl:format cl:nil "Header header~%float32[64] voltages~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Channels)))
  "Returns full string definition for message of type 'Channels"
  (cl:format cl:nil "Header header~%float32[64] voltages~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Channels>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'voltages) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Channels>))
  "Converts a ROS message object to a list"
  (cl:list 'Channels
    (cl:cons ':header (header msg))
    (cl:cons ':voltages (voltages msg))
))
