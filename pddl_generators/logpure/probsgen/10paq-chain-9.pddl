(define (problem logistics-generated)
(:domain logistics)
(:objects
pos0 - place
pos1 - place
pos2 - place
pos3 - place
pos4 - place
pos5 - place
pos6 - place
pos7 - place
pos8 - place
pos9 - place
pos10 - place
obj0 - package
obj1 - package
obj2 - package
obj3 - package
obj4 - package
obj5 - package
obj6 - package
obj7 - package
obj8 - package
obj9 - package
)
(:init
(load)
(nfull)
(att pos7)
(at obj0 pos6)
(at obj1 pos6)
(at obj2 pos9)
(at obj3 pos10)
(at obj4 pos3)
(at obj5 pos9)
(at obj6 pos5)
(at obj7 pos9)
(at obj8 pos9)
(at obj9 pos3)
)
(:goal (and
(at obj0 pos6)
(at obj1 pos9)
(at obj2 pos10)
(at obj3 pos3)
(at obj4 pos9)
(at obj5 pos5)
(at obj6 pos9)
(at obj7 pos9)
(at obj8 pos3)
(at obj9 pos0)
))
)
