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
pos18 - place
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
(att pos6)
(at obj0 pos17)
(at obj1 pos2)
(at obj2 pos17)
(at obj3 pos15)
(at obj4 pos2)
(at obj5 pos12)
(at obj6 pos14)
(at obj7 pos14)
(at obj8 pos18)
(at obj9 pos11)
)
(:goal (and
(at obj0 pos2)
(at obj1 pos17)
(at obj2 pos15)
(at obj3 pos2)
(at obj4 pos12)
(at obj5 pos14)
(at obj6 pos14)
(at obj7 pos18)
(at obj8 pos11)
(at obj9 pos18)
))
)