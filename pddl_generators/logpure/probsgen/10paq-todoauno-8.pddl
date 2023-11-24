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
(att pos1)
(at obj0 pos4)
(at obj1 pos7)
(at obj2 pos7)
(at obj3 pos8)
(at obj4 pos1)
(at obj5 pos9)
(at obj6 pos3)
(at obj7 pos4)
(at obj8 pos6)
(at obj9 pos5)
)
(:goal (and
(at obj0 pos1)
(at obj1 pos1)
(at obj2 pos1)
(at obj3 pos1)
(at obj4 pos1)
(at obj5 pos1)
(at obj6 pos1)
(at obj7 pos1)
(at obj8 pos1)
(at obj9 pos1)
))
)
