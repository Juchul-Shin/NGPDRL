(define (problem logistics-generated)
(:domain logistics)
(:objects
pos0 - place
pos1 - place
pos2 - place
pos3 - place
pos4 - place
pos5 - place
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
(at obj1 pos4)
(at obj2 pos0)
(at obj3 pos2)
(at obj4 pos2)
(at obj5 pos4)
(at obj6 pos3)
(at obj7 pos2)
(at obj8 pos0)
(at obj9 pos4)
)
(:goal (and
(at obj0 pos3)
(at obj1 pos4)
(at obj2 pos0)
(at obj3 pos4)
(at obj4 pos2)
(at obj5 pos5)
(at obj6 pos3)
(at obj7 pos2)
(at obj8 pos3)
(at obj9 pos2)
))
)
