(define (domain kitchen) 
	(:requirements :strips :typing) 	
	(:types food item place water tea cup keetle - object

	)	
	(:predicates
		(clean ?o - cup)
		(have_c ?o - cup)
		(have_k ?o - keetle)
		(taken_t ?o - tea)
		(taken_w ?o - water)
		(boiled ?o - water)
		(made ?o - tea)
		(at_item_k ?o1 - keetle ?o2 - place)
		(at_item_c ?o1 - cup ?o2 - place)
		(at_food_w ?o1 - water ?o2 - place)
		(at_food_t ?o1 - tea ?o2 - place)
		(at_robot ?o - place)
		(takefood)
		(getitem)
		(boil)
	)  
(:action GET_ITEM_k
	:parameters (?i - keetle ?p - place)
	:precondition 	
		(and 
		(at_robot ?p)
		(at_item_k ?i ?p)

				)
	:effect
 		(and
		(not (at_item_k ?i ?p))
		(have_k ?i)
		)
	)

(:action GET_ITEM_c
	:parameters (?i - cup ?p - place)
	:precondition 	
		(and 
		(at_robot ?p)
		(at_item_c ?i ?p)

				)
	:effect
 		(and
		(not (at_item_c ?i ?p))
		(have_c ?i)

		)
	)

(:action TAKE_FOOD_t
	:parameters (?o - tea ?p - place) 		
	:precondition 	(and 
		(at_food_t ?o ?p)
		(at_robot ?p)


	)
	:effect	(and (taken_t ?o)
		(not (at_food_t ?o ?p)) 

) 	
)

(:action TAKE_FOOD_w
	:parameters (?o - water ?p - place) 		
	:precondition 	(and 
		(at_food_w ?o ?p)
		(at_robot ?p)


	)
	:effect	(and (taken_w ?o)
		(not (at_food_w ?o ?p)) 

) 	
)

(:action MOVE
	:parameters (?o - place ?d - place)
	:precondition 	(at_robot ?o)
	:effect		(and
		(at_robot ?d)
		(not (at_robot ?o))
	)
	)

(:action ACTIVITY_Boil
	:parameters (?w - water ?k - keetle)
	:precondition 	(and
		(taken_w ?w)
		(have_k ?k)



		)
	:effect		(and
		(boiled ?w)


	)
	)
(:action ACTIVITY_Make_Tea
	:parameters (?t - tea ?w - water ?c - cup)
	:precondition	(and
		(clean ?c)
		(taken_t ?t)
		(have_c ?c)
		(boiled ?w)
		)
	:effect		(and
		(made ?t)
		(not (taken_t ?t))
		(not (clean ?c))

		)
	) )


