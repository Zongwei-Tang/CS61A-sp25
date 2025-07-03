(define (ascending? s)
(
    cond ((null? s) #t)
    ((null? (cdr s)) #t)
    ((> (car s) (car (cdr s))) #f)
    (else (ascending? (cdr s)))
)
)

(define (my-filter pred s)
(
    cond ((null? s) nil)
    ((pred (car s)) (append (list (car s)) (my-filter pred (cdr s))))
    (else (my-filter pred (cdr s)))
)
)

(define (interleave lst1 lst2)
(
    cond ((null? lst1) lst2)
    ((null? lst2) lst1)
    (else (append (list (car lst1) (car lst2)) (interleave (cdr lst1) (cdr lst2))))
)
)

(define (no-repeats s)
(
    cond ((null? s) nil)
    ((null? (cdr s)) s)
    (else (append (list (car s)) (no-repeats (filter (lambda (x) (not (= x (car s)))) (cdr s)))))
)
)


; Fall 2022 Q8
(define (remove-parens s)
(
    cond ((null? s) nil)
    ((list? (car s)) (append (remove-parens (car s)) (remove-parens (cdr s))))
    (else (cons (car s) (remove-parens (cdr s))))
)
)


; Spring 2022 Q11
(define (make-necklace beads length)
(
    if (= length 0) nil
    (cons (car beads) 
    (make-necklace (append (cdr beads) beads) (- length 1)))
    )
)

; Fall 2021 Q4
(define (repeated-call operator operands)
(
    if (null? operands) operator
    (repeated-call (operator (car operands)) (cdr operands))
)
)

; wtf is this question😅 I cannot do it 
(define (curry-helper num-args g)
(if (= num-args 0)
(g '())
(lambda (x) (curry-helper (- num-args 1) (lambda (s) (g (cons x s)))))
)
)

(define (one-arg s)
(
    if (numbers? s) s
    (let ((num-args (- (length s) 1)))
    (if (= num-args 1)
    (list (car s) (one-arg (cadr s)))
    (repeated-call (list (curry one-arg) (car s)) 
    (map one-arg (cdr s))
    )
    )
    )
)
)