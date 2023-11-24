python train_ppo.py -use_attention 0 -domain blocksmulti > trainblocks.txt
python train_ppo.py -use_attention 0 -domain logistics > trainlogistics.txt
python train_ppo.py -use_attention 0 -domain depots > traindepots.txt
python train_ppo.py -use_attention 0 -domain blocks4
python train_ppo.py -use_attention 5 -domain droneworld_simple
python evaluate_trained_model.py -use_attention 0 -domain blocks4 -policy_path '/Users/juchulshin/project/aso/saved_models/blocks4/20_11_2023__23_53_57/PPO_best_eval_model.pt'