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
pos11 - place
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
(att pos9)
(at obj0 pos9)
(at obj1 pos9)
(at obj2 pos9)
(at obj3 pos7)
(at obj4 pos7)
(at obj5 pos7)
(at obj6 pos8)
(at obj7 pos8)
(at obj8 pos8)
(at obj9 pos8)
)
(:goal (and
(at obj0 pos4)
(at obj1 pos4)
(at obj2 pos4)
(at obj3 pos3)
(at obj4 pos3)
(at obj5 pos3)
(at obj6 pos11)
(at obj7 pos11)
(at obj8 pos11)
(at obj9 pos11)
))
)
