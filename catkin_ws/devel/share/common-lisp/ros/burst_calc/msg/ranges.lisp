; Auto-generated. Do not edit!


(cl:in-package burst_calc-msg)


;//! \htmlinclude ranges.msg.html

(cl:defclass <ranges> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (baselines
    :reader baselines
    :initarg :baselines
    :type (cl:vector cl:float)
   :initform (cl:make-array 60 :element-type 'cl:float :initial-element 0.0))
   (thresholds
    :reader thresholds
    :initarg :thresholds
    :type (cl:vector cl:float)
   :initform (cl:make-array 60 :element-type 'cl:float :initial-element 0.0))
   (min_volts
    :reader min_volts
    :initarg :min_volts
    :type (cl:vector cl:float)
   :initform (cl:make-array 60 :element-type 'cl:float :initial-element 0.0))
   (max_volts
    :reader max_volts
    :initarg :max_volts
    :type (cl:vector cl:float)
   :initform (cl:make-array 60 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass ranges (<ranges>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ranges>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ranges)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name burst_calc-msg:<ranges> is deprecated: use burst_calc-msg:ranges instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <ranges>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:header-val is deprecated.  Use burst_calc-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'baselines-val :lambda-list '(m))
(cl:defmethod baselines-val ((m <ranges>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:baselines-val is deprecated.  Use burst_calc-msg:baselines instead.")
  (baselines m))

(cl:ensure-generic-function 'thresholds-val :lambda-list '(m))
(cl:defmethod thresholds-val ((m <ranges>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:thresholds-val is deprecated.  Use burst_calc-msg:thresholds instead.")
  (thresholds m))

(cl:ensure-generic-function 'min_volts-val :lambda-list '(m))
(cl:defmethod min_volts-val ((m <ranges>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:min_volts-val is deprecated.  Use burst_calc-msg:min_volts instead.")
  (min_volts m))

(cl:ensure-generic-function 'max_volts-val :lambda-list '(m))
(cl:defmethod max_volts-val ((m <ranges>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader burst_calc-msg:max_volts-val is deprecated.  Use burst_calc-msg:max_volts instead.")
  (max_volts m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ranges>) ostream)
  "Serializes a message object of type '<ranges>"
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
   (cl:slot-value msg 'baselines))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'thresholds))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'min_volts))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'max_volts))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ranges>) istream)
  "Deserializes a message object of type '<ranges>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:setf (cl:slot-value msg 'baselines) (cl:make-array 60))
  (cl:let ((vals (cl:slot-value msg 'baselines)))
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
  (cl:setf (cl:slot-value msg 'thresholds) (cl:make-array 60))
  (cl:let ((vals (cl:slot-value msg 'thresholds)))
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
  (cl:setf (cl:slot-value msg 'min_volts) (cl:make-array 60))
  (cl:let ((vals (cl:slot-value msg 'min_volts)))
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
  (cl:setf (cl:slot-value msg 'max_volts) (cl:make-array 60))
  (cl:let ((vals (cl:slot-value msg 'max_volts)))
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
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ranges>)))
  "Returns string type for a message object of type '<ranges>"
  "burst_calc/ranges")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ranges)))
  "Returns string type for a message object of type 'ranges"
  "burst_calc/ranges")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ranges>)))
  "Returns md5sum for a message object of type '<ranges>"
  "4760225b9a5eb17caa1ce5a89eca2bc9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ranges)))
  "Returns md5sum for a message object of type 'ranges"
  "4760225b9a5eb17caa1ce5a89eca2bc9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ranges>)))
  "Returns full string definition for message of type '<ranges>"
  (cl:format cl:nil "# Ranges message~%Header header~%float64[60] baselines~%float64[60] thresholds~%float64[60] min_volts~%float64[60] max_volts~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ranges)))
  "Returns full string definition for message of type 'ranges"
  (cl:format cl:nil "# Ranges message~%Header header~%float64[60] baselines~%float64[60] thresholds~%float64[60] min_volts~%float64[60] max_volts~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ranges>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'baselines) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'thresholds) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'min_volts) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'max_volts) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ranges>))
  "Converts a ROS message object to a list"
  (cl:list 'ranges
    (cl:cons ':header (header msg))
    (cl:cons ':baselines (baselines msg))
    (cl:cons ':thresholds (thresholds msg))
    (cl:cons ':min_volts (min_volts msg))
    (cl:cons ':max_volts (max_volts msg))
))
