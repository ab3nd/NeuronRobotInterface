
(cl:in-package :asdf)

(defsystem "zanni-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Stim" :depends-on ("_package_Stim"))
    (:file "_package_Stim" :depends-on ("_package"))
  ))