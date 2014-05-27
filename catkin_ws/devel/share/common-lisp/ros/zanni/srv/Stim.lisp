; Auto-generated. Do not edit!


(cl:in-package zanni-srv)


;//! \htmlinclude Stim-request.msg.html

(cl:defclass <Stim-request> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (signal
    :reader signal
    :initarg :signal
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (channel
    :reader channel
    :initarg :channel
    :type cl:integer
    :initform 0))
)

(cl:defclass Stim-request (<Stim-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Stim-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Stim-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name zanni-srv:<Stim-request> is deprecated: use zanni-srv:Stim-request instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <Stim-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader zanni-srv:header-val is deprecated.  Use zanni-srv:header instead.")
  (header m))

(cl:ensure-generic-function 'signal-val :lambda-list '(m))
(cl:defmethod signal-val ((m <Stim-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader zanni-srv:signal-val is deprecated.  Use zanni-srv:signal instead.")
  (signal m))

(cl:ensure-generic-function 'channel-val :lambda-list '(m))
(cl:defmethod channel-val ((m <Stim-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader zanni-srv:channel-val is deprecated.  Use zanni-srv:channel instead.")
  (channel m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Stim-request>) ostream)
  "Serializes a message object of type '<Stim-request>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'signal))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'signal))
  (cl:let* ((signed (cl:slot-value msg 'channel)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Stim-request>) istream)
  "Deserializes a message object of type '<Stim-request>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'signal) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'signal)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'channel) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Stim-request>)))
  "Returns string type for a service object of type '<Stim-request>"
  "zanni/StimRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Stim-request)))
  "Returns string type for a service object of type 'Stim-request"
  "zanni/StimRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Stim-request>)))
  "Returns md5sum for a message object of type '<Stim-request>"
  "8e9e0efb087f0d37d086778761f7e77d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Stim-request)))
  "Returns md5sum for a message object of type 'Stim-request"
  "8e9e0efb087f0d37d086778761f7e77d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Stim-request>)))
  "Returns full string definition for message of type '<Stim-request>"
  (cl:format cl:nil "Header header~%float64[] signal~%int32 channel~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Stim-request)))
  "Returns full string definition for message of type 'Stim-request"
  (cl:format cl:nil "Header header~%float64[] signal~%int32 channel~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Stim-request>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'signal) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Stim-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Stim-request
    (cl:cons ':header (header msg))
    (cl:cons ':signal (signal msg))
    (cl:cons ':channel (channel msg))
))
;//! \htmlinclude Stim-response.msg.html

(cl:defclass <Stim-response> (roslisp-msg-protocol:ros-message)
  ((done
    :reader done
    :initarg :done
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass Stim-response (<Stim-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Stim-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Stim-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name zanni-srv:<Stim-response> is deprecated: use zanni-srv:Stim-response instead.")))

(cl:ensure-generic-function 'done-val :lambda-list '(m))
(cl:defmethod done-val ((m <Stim-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader zanni-srv:done-val is deprecated.  Use zanni-srv:done instead.")
  (done m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Stim-response>) ostream)
  "Serializes a message object of type '<Stim-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'done) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Stim-response>) istream)
  "Deserializes a message object of type '<Stim-response>"
    (cl:setf (cl:slot-value msg 'done) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Stim-response>)))
  "Returns string type for a service object of type '<Stim-response>"
  "zanni/StimResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Stim-response)))
  "Returns string type for a service object of type 'Stim-response"
  "zanni/StimResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Stim-response>)))
  "Returns md5sum for a message object of type '<Stim-response>"
  "8e9e0efb087f0d37d086778761f7e77d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Stim-response)))
  "Returns md5sum for a message object of type 'Stim-response"
  "8e9e0efb087f0d37d086778761f7e77d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Stim-response>)))
  "Returns full string definition for message of type '<Stim-response>"
  (cl:format cl:nil "bool done~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Stim-response)))
  "Returns full string definition for message of type 'Stim-response"
  (cl:format cl:nil "bool done~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Stim-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Stim-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Stim-response
    (cl:cons ':done (done msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Stim)))
  'Stim-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Stim)))
  'Stim-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Stim)))
  "Returns string type for a service object of type '<Stim>"
  "zanni/Stim")