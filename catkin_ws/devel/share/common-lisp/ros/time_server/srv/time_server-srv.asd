
(cl:in-package :asdf)

(defsystem "time_server-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "time_srv" :depends-on ("_package_time_srv"))
    (:file "_package_time_srv" :depends-on ("_package"))
  ))