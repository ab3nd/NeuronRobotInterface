; Auto-generated. Do not edit!


(cl:in-package img_slicer-srv)


;//! \htmlinclude ImageSlicer-request.msg.html

(cl:defclass <ImageSlicer-request> (roslisp-msg-protocol:ros-message)
  ((slices
    :reader slices
    :initarg :slices
    :type cl:integer
    :initform 0))
)

(cl:defclass ImageSlicer-request (<ImageSlicer-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ImageSlicer-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ImageSlicer-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name img_slicer-srv:<ImageSlicer-request> is deprecated: use img_slicer-srv:ImageSlicer-request instead.")))

(cl:ensure-generic-function 'slices-val :lambda-list '(m))
(cl:defmethod slices-val ((m <ImageSlicer-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader img_slicer-srv:slices-val is deprecated.  Use img_slicer-srv:slices instead.")
  (slices m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ImageSlicer-request>) ostream)
  "Serializes a message object of type '<ImageSlicer-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'slices)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'slices)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'slices)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'slices)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 32) (cl:slot-value msg 'slices)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 40) (cl:slot-value msg 'slices)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 48) (cl:slot-value msg 'slices)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 56) (cl:slot-value msg 'slices)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ImageSlicer-request>) istream)
  "Deserializes a message object of type '<ImageSlicer-request>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'slices)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'slices)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'slices)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'slices)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 32) (cl:slot-value msg 'slices)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 40) (cl:slot-value msg 'slices)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 48) (cl:slot-value msg 'slices)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 56) (cl:slot-value msg 'slices)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ImageSlicer-request>)))
  "Returns string type for a service object of type '<ImageSlicer-request>"
  "img_slicer/ImageSlicerRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ImageSlicer-request)))
  "Returns string type for a service object of type 'ImageSlicer-request"
  "img_slicer/ImageSlicerRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ImageSlicer-request>)))
  "Returns md5sum for a message object of type '<ImageSlicer-request>"
  "22f4a733c28b262cbf68bf518359370a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ImageSlicer-request)))
  "Returns md5sum for a message object of type 'ImageSlicer-request"
  "22f4a733c28b262cbf68bf518359370a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ImageSlicer-request>)))
  "Returns full string definition for message of type '<ImageSlicer-request>"
  (cl:format cl:nil "uint64 slices~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ImageSlicer-request)))
  "Returns full string definition for message of type 'ImageSlicer-request"
  (cl:format cl:nil "uint64 slices~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ImageSlicer-request>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ImageSlicer-request>))
  "Converts a ROS message object to a list"
  (cl:list 'ImageSlicer-request
    (cl:cons ':slices (slices msg))
))
;//! \htmlinclude ImageSlicer-response.msg.html

(cl:defclass <ImageSlicer-response> (roslisp-msg-protocol:ros-message)
  ((pixelCount
    :reader pixelCount
    :initarg :pixelCount
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0)))
)

(cl:defclass ImageSlicer-response (<ImageSlicer-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ImageSlicer-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ImageSlicer-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name img_slicer-srv:<ImageSlicer-response> is deprecated: use img_slicer-srv:ImageSlicer-response instead.")))

(cl:ensure-generic-function 'pixelCount-val :lambda-list '(m))
(cl:defmethod pixelCount-val ((m <ImageSlicer-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader img_slicer-srv:pixelCount-val is deprecated.  Use img_slicer-srv:pixelCount instead.")
  (pixelCount m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ImageSlicer-response>) ostream)
  "Serializes a message object of type '<ImageSlicer-response>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'pixelCount))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:write-byte (cl:ldb (cl:byte 8 0) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 32) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 40) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 48) ele) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 56) ele) ostream))
   (cl:slot-value msg 'pixelCount))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ImageSlicer-response>) istream)
  "Deserializes a message object of type '<ImageSlicer-response>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'pixelCount) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'pixelCount)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 32) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 40) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 48) (cl:aref vals i)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 56) (cl:aref vals i)) (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ImageSlicer-response>)))
  "Returns string type for a service object of type '<ImageSlicer-response>"
  "img_slicer/ImageSlicerResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ImageSlicer-response)))
  "Returns string type for a service object of type 'ImageSlicer-response"
  "img_slicer/ImageSlicerResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ImageSlicer-response>)))
  "Returns md5sum for a message object of type '<ImageSlicer-response>"
  "22f4a733c28b262cbf68bf518359370a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ImageSlicer-response)))
  "Returns md5sum for a message object of type 'ImageSlicer-response"
  "22f4a733c28b262cbf68bf518359370a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ImageSlicer-response>)))
  "Returns full string definition for message of type '<ImageSlicer-response>"
  (cl:format cl:nil "uint64[] pixelCount~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ImageSlicer-response)))
  "Returns full string definition for message of type 'ImageSlicer-response"
  (cl:format cl:nil "uint64[] pixelCount~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ImageSlicer-response>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'pixelCount) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ImageSlicer-response>))
  "Converts a ROS message object to a list"
  (cl:list 'ImageSlicer-response
    (cl:cons ':pixelCount (pixelCount msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'ImageSlicer)))
  'ImageSlicer-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'ImageSlicer)))
  'ImageSlicer-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ImageSlicer)))
  "Returns string type for a service object of type '<ImageSlicer>"
  "img_slicer/ImageSlicer")