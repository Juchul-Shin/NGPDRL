for a in '5' 
do
	for i in 'ascensor' 'logistics'
	do
		echo $i att $a
		python evaluate_trained_model.py -domain $i -use_attention $a -policy /home/linuxremote/Escritorio/tfm/generalized-planning-with-drl-master/saved_models/$i/att_$a/PPO_best_eval_model.pt -max_time 600 -eval_k 50
	done
done

read
