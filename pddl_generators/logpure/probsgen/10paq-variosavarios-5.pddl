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
pos12 - place
pos13 - place
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
(att pos2)
(at obj0 pos0)
(at obj1 pos0)
(at obj2 pos0)
(at obj3 pos2)
(at obj4 pos2)
(at obj5 pos2)
(at obj6 pos10)
(at obj7 pos10)
(at obj8 pos10)
(at obj9 pos10)
)
(:goal (and
(at obj0 pos8)
(at obj1 pos8)
(at obj2 pos8)
(at obj3 pos11)
(at obj4 pos11)
(at obj5 pos11)
(at obj6 pos9)
(at obj7 pos9)
(at obj8 pos9)
(at obj9 pos9)
))
)
