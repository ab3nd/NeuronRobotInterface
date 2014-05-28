; Auto-generated. Do not edit!


(cl:in-package arm-msg)


;//! \htmlinclude constant_move.msg.html

(cl:defclass <constant_move> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (states
    :reader states
    :initarg :states
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 8 :element-type 'cl:fixnum :initial-element 0))
   (speeds
    :reader speeds
    :initarg :speeds
    :type (cl:vector cl:fixnum)
   :initform (cl:make-array 7 :element-type 'cl:fixnum :initial-element 0))
   (query
    :reader query
    :initarg :query
    :type cl:boolean
    :initform cl:nil)
   (quit
    :reader quit
    :initarg :quit
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass constant_move (<constant_move>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <constant_move>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'constant_move)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name arm-msg:<constant_move> is deprecated: use arm-msg:constant_move instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <constant_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:header-val is deprecated.  Use arm-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'states-val :lambda-list '(m))
(cl:defmethod states-val ((m <constant_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:states-val is deprecated.  Use arm-msg:states instead.")
  (states m))

(cl:ensure-generic-function 'speeds-val :lambda-list '(m))
(cl:defmethod speeds-val ((m <constant_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:speeds-val is deprecated.  Use arm-msg:speeds instead.")
  (speeds m))

(cl:ensure-generic-function 'query-val :lambda-list '(m))
(cl:defmethod query-val ((m <constant_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:query-val is deprecated.  Use arm-msg:query instead.")
  (query m))

(cl:ensure-generic-function 'quit-val :lambda-list '(m))
(cl:defmethod quit-val ((m <constant_move>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arm-msg:quit-val is deprecated.  Use arm-msg:quit instead.")
  (quit m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <constant_move>) ostream)
  "Serializes a message object of type '<constant_move>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    ))
   (cl:slot-value msg 'states))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    ))
   (cl:slot-value msg 'speeds))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'query) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'quit) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <constant_move>) istream)
  "Deserializes a message object of type '<constant_move>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:setf (cl:slot-value msg 'states) (cl:make-array 8))
  (cl:let ((vals (cl:slot-value msg 'states)))
    (cl:dotimes (i 8)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))))
  (cl:setf (cl:slot-value msg 'speeds) (cl:make-array 7))
  (cl:let ((vals (cl:slot-value msg 'speeds)))
    (cl:dotimes (i 7)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))))
    (cl:setf (cl:slot-value msg 'query) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'quit) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<constant_move>)))
  "Returns string type for a message object of type '<constant_move>"
  "arm/constant_move")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'constant_move)))
  "Returns string type for a message object of type 'constant_move"
  "arm/constant_move")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<constant_move>)))
  "Returns md5sum for a message object of type '<constant_move>"
  "87f1d9135e20ae2be6861b3a526c5653")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'constant_move)))
  "Returns md5sum for a message object of type 'constant_move"
  "87f1d9135e20ae2be6861b3a526c5653")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<constant_move>)))
  "Returns full string definition for message of type '<constant_move>"
  (cl:format cl:nil "# Constant movement message~%Header header~%int8[8] states~%int8[7] speeds~%bool query~%bool quit~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'constant_move)))
  "Returns full string definition for message of type 'constant_move"
  (cl:format cl:nil "# Constant movement message~%Header header~%int8[8] states~%int8[7] speeds~%bool query~%bool quit~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <constant_move>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'states) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'speeds) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 1)))
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <constant_move>))
  "Converts a ROS message object to a list"
  (cl:list 'constant_move
    (cl:cons ':header (header msg))
    (cl:cons ':states (states msg))
    (cl:cons ':speeds (speeds msg))
    (cl:cons ':query (query msg))
    (cl:cons ':quit (quit msg))
))
