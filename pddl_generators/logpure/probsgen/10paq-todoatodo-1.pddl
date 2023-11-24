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
pos14 - place
pos15 - place
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
(at obj0 pos5)
(at obj1 pos12)
(at obj2 pos13)
(at obj3 pos11)
(at obj4 pos13)
(at obj5 pos7)
(at obj6 pos4)
(at obj7 pos11)
(at obj8 pos15)
(at obj9 pos10)
)
(:goal (and
(at obj0 pos11)
(at obj1 pos1)
(at obj2 pos3)
(at obj3 pos13)
(at obj4 pos15)
(at obj5 pos5)
(at obj6 pos10)
(at obj7 pos10)
(at obj8 pos0)
(at obj9 pos4)
))
)
