(define (domain rovers)
(:requirements :typing)
(:types waypoint  )

(:predicates 
        (at ?y - waypoint)
        (at_lander ?y - waypoint)
        (empty)
        (have_rock_analysis ?w - waypoint)
        (have_soil_analysis ?w - waypoint)
        (full)
        (communicated_soil_data ?w - waypoint)
        (communicated_rock_data ?w - waypoint)
        (at_soil_sample ?w - waypoint)
        (at_rock_sample ?w - waypoint)
        (have_image ?w - waypoint)
        (calibrated ?c - waypoint) 
        (communicated_image_data ?p - waypoint)
        (mode)
        (sended)
        (ssend)
        (dummy ?w1 - waypoint ?w2 - waypoint)
)


(:action navigate
:parameters (?y - waypoint ?z - waypoint)
:precondition (and (at ?y) )
:effect (and (not (at ?y)) (at ?z) )
)

(:action sample_soil
:parameters (?p - waypoint)
:precondition (and (at ?p) (at_soil_sample ?p) (empty) (sended) )
:effect (and (not (empty)) (full) (have_soil_analysis ?p) (not (at_soil_sample ?p)) )
)

(:action sample_rock
:parameters (?p - waypoint)
:precondition (and (at ?p) (at_rock_sample ?p) (empty) (sended) )
:effect (and (not (empty)) (full) (have_rock_analysis ?p) (not (at_rock_sample ?p)) )
)

(:action drop
:parameters ()
:precondition (and (full) )
:effect (and (not (full)) (empty) )
)

(:action communicate_rock_data
:parameters (?p - waypoint ?x - waypoint)
:precondition (and (at ?x)(at_lander ?x)(have_rock_analysis ?p) )
:effect (and (communicated_rock_data ?p) (not (have_rock_analysis ?p)) (not (sended)) )
)

(:action communicate_soil_data
:parameters (?p - waypoint ?x - waypoint)
:precondition (and (at ?x) (at_lander ?x) (have_soil_analysis ?p) )
:effect (and (communicated_soil_data ?p) (not (have_soil_analysis ?p)) (not (sended)) )
)

(:action calibrate_cam
:parameters ( ?w - waypoint)
:precondition (and (at ?w) )
:effect (calibrated ?w) )

(:action take_image
:parameters ( ?p - waypoint )
:precondition (and (calibrated ?p) (sended) (at ?p) )
:effect (and (have_image ?p) (not (calibrated ?p)) )
)

(:action communicate_image_data
:parameters (?x - waypoint ?p - waypoint)
:precondition (and (at ?x) (at_lander ?x) (have_image ?p))
:effect (and (communicated_image_data ?p) (not (sended)) (not (have_image ?p)) )
)

)
