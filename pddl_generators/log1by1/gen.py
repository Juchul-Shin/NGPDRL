

from random import randrange

num = randrange(9)

if num == 0:
	print("(define (problem logistics-4-0)\n(:domain logistics)\n(:objects\n apt1 apt2\n pos2 pos1 - place\n obj23 obj22 obj21 obj13 obj12 obj11 - package)\n\n(:init (load) (nfull) (att pos2) (at obj11 pos1) \n (at obj21 apt1)\n\n )\n\n(:goal  (and (at obj11 apt1) (at obj21 pos1) ) )\n)")
elif num == 1:
	print("(define (problem logistics-4-0)\n(:domain logistics)\n(:objects\n apt1 apt2\n pos2 pos1 - place\n obj23 obj22 obj21 obj13 obj12 obj11 - package)\n\n(:init (load) (nfull) (att pos1) (at obj11 pos1)\n (at obj13 pos1) (at obj21 pos2) \n (at obj23 pos2) \n )\n\n(:goal (and (at obj11 apt1) (at obj23 pos1) (at obj13 apt1) (at obj21 pos1)))\n)")
elif num == 2:
	print("(define (problem logistics-5-0)\n(:domain logistics)\n(:objects\n  apt2 apt1\n  pos2 pos1 - place\n  obj23 obj22 obj21 obj13 obj12 obj11 - package)\n\n(:init (load) (nfull) (att pos1) (at obj11 pos1)\n (at obj12 pos1) (at obj13 pos1) (at obj22 pos2)\n (at obj23 pos2) \n )\n(:goal (and (at obj23 apt2) (at obj22 apt1) (at obj13 apt2) (at obj12 pos2)\n            (at obj11 pos2)))\n)")
elif num == 3:
	print("(define (problem logistics-6-0)\n(:domain logistics)\n(:objects\n  apt2 apt1\n  pos2 pos1 - place\n  obj23 obj22 obj21 obj13 obj12 obj11 - package)\n\n(:init (load) (nfull) (att pos1) (at obj11 pos1)\n (at obj12 pos1) (at obj13 pos1) (at obj21 pos2)\n (at obj23 pos2) \n )\n\n(:goal (and (at obj12 apt2) (at obj23 apt1) (at obj21 apt2) \n            (at obj13 pos2) (at obj11 apt2)))\n)")
elif num == 4:
	print("(define (problem logistics-7-0)\n(:domain logistics)\n(:objects\n  apt3 apt2 apt1 pos3 pos2 pos1 - place\n  obj33 obj32 obj31 obj23 obj22 obj21 obj13 obj12 obj11 - package)\n\n(:init (load) (nfull) (att pos1)\n (at obj12 pos1) (at obj13 pos1)\n (at obj23 pos2) \n (at obj31 pos3) (at obj32 pos3) (at obj33 pos3) \n \n )\n\n(:goal (and  (at obj33 apt1) (at obj12 pos2) (at obj13 apt3)\n            (at obj31 apt2) (at obj23 apt1) (at obj32 pos1)))\n)")
elif num == 5:
	print("(define (problem logistics-8-0)\n\n(:domain logistics)\n(:objects\n  apt3 apt2 apt1\n   pos3 pos2 pos1 - place\n   obj33 obj32 obj31 obj23 obj22 obj21 obj13 obj12 obj11 - package)\n\n(:init (load) (nfull) (att pos1) \n (at obj11 pos1)  (at obj13 pos1)\n (at obj22 pos2) (at obj23 pos2) \n (at obj31 pos3) (at obj32 pos3)\n \n )\n\n(:goal (and (at obj11 pos3)  (at obj31 apt3) (at obj22 pos3)\n             (at obj23 apt2) (at obj13 apt2) (at obj32 apt1)))\n)")
elif num == 6:
	print("(define (problem logistics-9-0)\n(:domain logistics)\n(:objects\n  apt3 apt2 apt1\n  pos3 pos2 pos1 - place\n  obj33 obj32 obj31 obj23 obj22 obj21 obj13 obj12 obj11 - package)\n\n\n(:init (load) (nfull) (att pos1)\n (at obj11 pos1) (at obj12 pos1) (at obj13 pos1)\n (at obj21 pos2) (at obj22 pos2) (at obj23 pos2) \n (at obj31 pos3) (at obj32 pos3) (at obj33 pos3) \n \n )\n\n(:goal (and (at obj23 pos3) (at obj32 pos1) (at obj22 pos1) (at obj31 apt3)\n            (at obj11 pos1) (at obj33 pos3) (at obj13 apt3) (at obj12 pos1)\n            (at obj21 apt1)))\n)")
elif num == 7:
	print("(define (problem logistics-10-0)\n(:domain logistics)\n(:objects\n  apt1 apt4 apt3 apt2\n  pos4 pos3  pos2  pos1 - place\n  obj43 obj42 obj41 obj33 obj32 obj31 obj23 obj22 obj21 obj13 obj12 obj11 - package)\n\n(:init (load) (nfull) (att pos1) \n (at obj11 pos1) (at obj12 pos1) (at obj21 pos2)\n (at obj22 pos2) (at obj23 pos2) (at obj31 pos3) (at obj32 pos3)\n (at obj33 pos3) (at obj41 pos4) (at obj42 pos4) \n \n )\n\n(:goal (and (at obj31 pos3) (at obj33 apt3) (at obj41 apt3) (at obj23 pos4)\n            (at obj11 pos3) (at obj22 apt2) (at obj12 apt1) (at obj21 pos4)\n            (at obj42 pos4) (at obj32 pos1)))\n)")
elif num == 8:
	print("(define (problem logistics-15-0)\n(:domain logistics)\n  (:objects \n  apt5 apt4 apt3 apt2 apt1\n  pos5 pos4 pos3 pos2 pos1 - place \n  obj53 obj52 obj51 obj43 obj42 obj41 obj33 obj32\n  obj31 obj23 obj22 obj21 obj13 obj12 obj11 - package)\n\n(:init (load) (nfull) (att pos1) (at obj11 pos1)\n (at obj12 pos1) (at obj13 pos1) (at obj21 pos2) (at obj22 pos2)\n (at obj23 pos2) (at obj31 pos3) (at obj32 pos3) (at obj33 pos3)\n (at obj41 pos4) (at obj42 pos4) (at obj43 pos4) \n (at obj51 pos5) (at obj52 pos5) (at obj53 pos5) \n \n \n )\n\n(:goal (and (at obj22 apt4) (at obj31 apt4) (at obj43 pos5) (at obj13 apt1)\n            (at obj23 pos4) (at obj12 pos2) (at obj51 pos3) (at obj32 pos3)\n            (at obj11 apt3) (at obj42 apt2) (at obj52 apt4) (at obj33 apt3)\n            (at obj21 pos3) (at obj53 apt2) (at obj41 apt1)))\n)")
