
(cl:in-package :asdf)

(defsystem "zanni-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Channels" :depends-on ("_package_Channels"))
    (:file "_package_Channels" :depends-on ("_package"))
  ))