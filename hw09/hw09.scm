(define (curry-cook formals body)
(
  cond ((null? formals) body)
  (else `(lambda (,(car formals)) ,(curry-cook (cdr formals) body) ))
)
)

(define (curry-consume curry args)
(
  cond ((null? args) curry)
  (else (curry-consume (curry (car args)) (cdr args)))
)
)

(define-macro (switch expr options)
  (switch-to-cond (list 'switch expr options)))

(define (switch-to-cond switch-expr)
  (cons 'cond
        (map (lambda (option)
               (cons `(equal? ,(car (cdr switch-expr)) ,(car option)) (cdr option)))
             (car (cdr (cdr switch-expr))))))


; Fall 2019 Q9
(define-macro (partial call)
`(lambda (y) ,(append call '(y)))
)

; Im tired i dont want to do other exam practice😭