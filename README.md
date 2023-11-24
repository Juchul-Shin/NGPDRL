# Generalized Planning with Deep Reinforcement Learning

Using Graph Neural Networks and Deep Reinforcement Learning to solve large generalized planning problems

![5 blocks blocksworld](images/blocksworld_solution_gifs/blocksworld_5.gif)   
![50 blocks blocksworld](images/blocksworld_solution_gifs/blocksworld_50.gif)


## Paper
For more details, please see our paper [Generalized Planning with Deep Reinforcement Learning](https://arxiv.org/abs/2005.02305). If this code is useful for your work, please cite our paper:

```
@article{rivlin2020generalized,
  title={Generalized Planning With Deep Reinforcement Learning},
  author={Rivlin, Or and Hazan, Tamir and Karpas, Erez},
  journal={arXiv preprint arXiv:2005.02305},
  year={2020}
}
``` 

## Dependencies

* Python>=3.6
* NumPy
* SciPy
* [PyTorch](http://pytorch.org/)>=1.1
* [PyTorch Geometric](https://github.com/rusty1s/pytorch_geometric)
* Networkx
* Pyperplan
* Fast-downward
* Tensorboard
* Matplotlib

In addition, this repository contains slightly modified versions of several pddl task generators, taken from [this repository](https://github.com/AI-Planning/pddl-generators).

## Installation
First, create a root directory
```bash
mkdir generalized_planning_with_drl_root
```
Then clone the repository + pyperplan and fast-downward inside
```bash
cd generalized_planning_with_drl_root
git clone https://github.com/orrivlin/generalized-planning-with-drl.git
git clone https://github.com/drwiner/Pyperplan.git
git clone https://github.com/danfis/fast-downward.git
```
Follow the installation instructions for fast-downward at the [official website](http://www.fast-downward.org/).
Next, compile the pddl-generators:
```bash
cd generalized-planning-with-drl/pddl_generators
./build_all
```

## Training
To train a model on the blocksworld domain:
```bash
python3 train_ppo.py -domain blocks4
```
The script will save the trained model in the saved_model directory

## Evaluation
To evaluate the trained model against fast-downward:
```bash
python3 evaluate_trained_mdel.py -domain blocks4 -policy_path <path to model directory>/PPO_best_eval_model.pt
```
This will take quite a while...



