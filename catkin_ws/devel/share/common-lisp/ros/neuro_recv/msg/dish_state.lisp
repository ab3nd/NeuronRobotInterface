; Auto-generated. Do not edit!


(cl:in-package neuro_recv-msg)


;//! \htmlinclude dish_state.msg.html

(cl:defclass <dish_state> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (samples
    :reader samples
    :initarg :samples
    :type (cl:vector cl:float)
   :initform (cl:make-array 60 :element-type 'cl:float :initial-element 0.0))
   (last_dish
    :reader last_dish
    :initarg :last_dish
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass dish_state (<dish_state>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <dish_state>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'dish_state)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name neuro_recv-msg:<dish_state> is deprecated: use neuro_recv-msg:dish_state instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <dish_state>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader neuro_recv-msg:header-val is deprecated.  Use neuro_recv-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'samples-val :lambda-list '(m))
(cl:defmethod samples-val ((m <dish_state>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader neuro_recv-msg:samples-val is deprecated.  Use neuro_recv-msg:samples instead.")
  (samples m))

(cl:ensure-generic-function 'last_dish-val :lambda-list '(m))
(cl:defmethod last_dish-val ((m <dish_state>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader neuro_recv-msg:last_dish-val is deprecated.  Use neuro_recv-msg:last_dish instead.")
  (last_dish m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <dish_state>) ostream)
  "Serializes a message object of type '<dish_state>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'samples))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'last_dish) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <dish_state>) istream)
  "Deserializes a message object of type '<dish_state>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:setf (cl:slot-value msg 'samples) (cl:make-array 60))
  (cl:let ((vals (cl:slot-value msg 'samples)))
    (cl:dotimes (i 60)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits)))))
    (cl:setf (cl:slot-value msg 'last_dish) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<dish_state>)))
  "Returns string type for a message object of type '<dish_state>"
  "neuro_recv/dish_state")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'dish_state)))
  "Returns string type for a message object of type 'dish_state"
  "neuro_recv/dish_state")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<dish_state>)))
  "Returns md5sum for a message object of type '<dish_state>"
  "c08ea80d278c864525005be19edfdf2f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'dish_state)))
  "Returns md5sum for a message object of type 'dish_state"
  "c08ea80d278c864525005be19edfdf2f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<dish_state>)))
  "Returns full string definition for message of type '<dish_state>"
  (cl:format cl:nil "# Dish state message~%Header header~%float64[60] samples~%bool last_dish~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'dish_state)))
  "Returns full string definition for message of type 'dish_state"
  (cl:format cl:nil "# Dish state message~%Header header~%float64[60] samples~%bool last_dish~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <dish_state>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'samples) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <dish_state>))
  "Converts a ROS message object to a list"
  (cl:list 'dish_state
    (cl:cons ':header (header msg))
    (cl:cons ':samples (samples msg))
    (cl:cons ':last_dish (last_dish msg))
))
