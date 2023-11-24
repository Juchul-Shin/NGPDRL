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
pos16 - place
pos17 - place
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
(att pos8)
(at obj0 pos3)
(at obj1 pos17)
(at obj2 pos13)
(at obj3 pos3)
(at obj4 pos12)
(at obj5 pos2)
(at obj6 pos4)
(at obj7 pos10)
(at obj8 pos17)
(at obj9 pos8)
)
(:goal (and
(at obj0 pos15)
(at obj1 pos4)
(at obj2 pos6)
(at obj3 pos12)
(at obj4 pos15)
(at obj5 pos3)
(at obj6 pos14)
(at obj7 pos13)
(at obj8 pos2)
(at obj9 pos9)
))
)
