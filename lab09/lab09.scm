;(define (over-or-under num1 num2) 
;(cond ((< num1 num2) -1) ((= num1 num2) 0) ((> num1 num2) 1)
;))

(define (over-or-under num1 num2) (if (< num1 num2) -1 (if (= num1 num2) 0 1)))

(define (make-adder num)
(lambda (inc) (+ num inc)
))

(define (composed f g)
(lambda (x) (f (g x)))
)

(define (repeat f n)
(define (helper x) 
(cond ((= n 1) (f x))
(else ((composed f (repeat f (- n 1))) x))
)
)
helper
)

(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b)
(
  cond ((> a b) (if (zero? (modulo a b)) b (gcd b (modulo a b))))
        ((< a b) (if (zero? (modulo b a)) a (gcd a (modulo b a))))
        (else a)
)
)
