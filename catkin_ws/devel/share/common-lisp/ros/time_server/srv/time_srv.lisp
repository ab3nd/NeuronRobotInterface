; Auto-generated. Do not edit!


(cl:in-package time_server-srv)


;//! \htmlinclude time_srv-request.msg.html

(cl:defclass <time_srv-request> (roslisp-msg-protocol:ros-message)
  ((target
    :reader target
    :initarg :target
    :type cl:real
    :initform 0))
)

(cl:defclass time_srv-request (<time_srv-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <time_srv-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'time_srv-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name time_server-srv:<time_srv-request> is deprecated: use time_server-srv:time_srv-request instead.")))

(cl:ensure-generic-function 'target-val :lambda-list '(m))
(cl:defmethod target-val ((m <time_srv-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader time_server-srv:target-val is deprecated.  Use time_server-srv:target instead.")
  (target m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <time_srv-request>) ostream)
  "Serializes a message object of type '<time_srv-request>"
  (cl:let ((__sec (cl:floor (cl:slot-value msg 'target)))
        (__nsec (cl:round (cl:* 1e9 (cl:- (cl:slot-value msg 'target) (cl:floor (cl:slot-value msg 'target)))))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 0) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __nsec) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <time_srv-request>) istream)
  "Deserializes a message object of type '<time_srv-request>"
    (cl:let ((__sec 0) (__nsec 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 0) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __nsec) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'target) (cl:+ (cl:coerce __sec 'cl:double-float) (cl:/ __nsec 1e9))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<time_srv-request>)))
  "Returns string type for a service object of type '<time_srv-request>"
  "time_server/time_srvRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'time_srv-request)))
  "Returns string type for a service object of type 'time_srv-request"
  "time_server/time_srvRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<time_srv-request>)))
  "Returns md5sum for a message object of type '<time_srv-request>"
  "538088de2280801645bd68bcaa6d0173")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'time_srv-request)))
  "Returns md5sum for a message object of type 'time_srv-request"
  "538088de2280801645bd68bcaa6d0173")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<time_srv-request>)))
  "Returns full string definition for message of type '<time_srv-request>"
  (cl:format cl:nil "~%time target~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'time_srv-request)))
  "Returns full string definition for message of type 'time_srv-request"
  (cl:format cl:nil "~%time target~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <time_srv-request>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <time_srv-request>))
  "Converts a ROS message object to a list"
  (cl:list 'time_srv-request
    (cl:cons ':target (target msg))
))
;//! \htmlinclude time_srv-response.msg.html

(cl:defclass <time_srv-response> (roslisp-msg-protocol:ros-message)
  ((actual
    :reader actual
    :initarg :actual
    :type cl:real
    :initform 0)
   (delta
    :reader delta
    :initarg :delta
    :type cl:real
    :initform 0))
)

(cl:defclass time_srv-response (<time_srv-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <time_srv-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'time_srv-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name time_server-srv:<time_srv-response> is deprecated: use time_server-srv:time_srv-response instead.")))

(cl:ensure-generic-function 'actual-val :lambda-list '(m))
(cl:defmethod actual-val ((m <time_srv-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader time_server-srv:actual-val is deprecated.  Use time_server-srv:actual instead.")
  (actual m))

(cl:ensure-generic-function 'delta-val :lambda-list '(m))
(cl:defmethod delta-val ((m <time_srv-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader time_server-srv:delta-val is deprecated.  Use time_server-srv:delta instead.")
  (delta m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <time_srv-response>) ostream)
  "Serializes a message object of type '<time_srv-response>"
  (cl:let ((__sec (cl:floor (cl:slot-value msg 'actual)))
        (__nsec (cl:round (cl:* 1e9 (cl:- (cl:slot-value msg 'actual) (cl:floor (cl:slot-value msg 'actual)))))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 0) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __nsec) ostream))
  (cl:let ((__sec (cl:floor (cl:slot-value msg 'delta)))
        (__nsec (cl:round (cl:* 1e9 (cl:- (cl:slot-value msg 'delta) (cl:floor (cl:slot-value msg 'delta)))))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 0) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __nsec) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <time_srv-response>) istream)
  "Deserializes a message object of type '<time_srv-response>"
    (cl:let ((__sec 0) (__nsec 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 0) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __nsec) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'actual) (cl:+ (cl:coerce __sec 'cl:double-float) (cl:/ __nsec 1e9))))
    (cl:let ((__sec 0) (__nsec 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 0) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __nsec) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'delta) (cl:+ (cl:coerce __sec 'cl:double-float) (cl:/ __nsec 1e9))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<time_srv-response>)))
  "Returns string type for a service object of type '<time_srv-response>"
  "time_server/time_srvResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'time_srv-response)))
  "Returns string type for a service object of type 'time_srv-response"
  "time_server/time_srvResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<time_srv-response>)))
  "Returns md5sum for a message object of type '<time_srv-response>"
  "538088de2280801645bd68bcaa6d0173")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'time_srv-response)))
  "Returns md5sum for a message object of type 'time_srv-response"
  "538088de2280801645bd68bcaa6d0173")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<time_srv-response>)))
  "Returns full string definition for message of type '<time_srv-response>"
  (cl:format cl:nil "time actual~%duration delta~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'time_srv-response)))
  "Returns full string definition for message of type 'time_srv-response"
  (cl:format cl:nil "time actual~%duration delta~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <time_srv-response>))
  (cl:+ 0
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <time_srv-response>))
  "Converts a ROS message object to a list"
  (cl:list 'time_srv-response
    (cl:cons ':actual (actual msg))
    (cl:cons ':delta (delta msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'time_srv)))
  'time_srv-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'time_srv)))
  'time_srv-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'time_srv)))
  "Returns string type for a service object of type '<time_srv>"
  "time_server/time_srv")