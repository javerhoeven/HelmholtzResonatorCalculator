from calculation.optimizer import Optimizer

def search_optimal(f_target, q_target):
    optimizer = Optimizer(f_target=f_target, q_target=q_target)
    optimizer.search_optimal()