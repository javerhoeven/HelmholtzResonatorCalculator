import threading
from calculation.optimizer import Optimizer

def optimizer(f_target, q_target):
    optimizer = Optimizer(f_target=f_target, q_target=q_target)
    best_result = optimizer.search_optimal()
    
    
    
    # Result
    print_n = 1
    for res in optimizer.best_results[:print_n]:
        _sim = optimizer.create_default_sim(res)
        optimizer.display_results(_sim)
        
    return optimizer.create_default_sim(best_result)