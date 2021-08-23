from filters import *
from polygon_intersection_generator import *
import time

class IntersectingPolygons:
    steps_count = 0
    def __init__(self, n, filter_manager):
        self.n = n
        self.filter_manager = filter_manager
        self.generator = PolygonIntersectionGenerator(self.n)
        self.start_time = time.time()
    
    def end_condition(self, candidate_sequence):
        """
        We are looking for a sequence that has final step the reverse of the initial step
        """
        # I think this is sufficiently implemented in conjuction with the filters (once they 
        #   are fully implemented)
        if len(candidate_sequence) > 1:
            first_step = candidate_sequence[0]
            last_step = candidate_sequence[-1]
            if len(last_step) == len(first_step):
                return all([last_step[-(1 + i)] == first_step[i] for i in range(len(last_step))])
        return False

    def recursion(self, candidate_sequence):
        self.steps_count += 1
        if self.steps_count %500000 == 0: 
            elapsed_time = time.time() - self.start_time
            print(f"Sequence count {self.steps_count}, time {elapsed_time:.1f}, sequence {candidate_sequence}", flush=True)
        #if self.steps_count > 100000: return
        new_candidate_sequence = self.generator.generate_candidate_step(candidate_sequence)
        for x in new_candidate_sequence:
            if not self.filter_manager.filter_candidate_step(x):
                if self.end_condition(x):
                    print(f"theoretically met end condition {x}")
                else:
                    self.recursion(x)
            else:
                #print(f"filtered out {x}")
                pass


n=7
fm = FilterManager(n, [
    ParityFilter,
    Lemma1Filter,
    MaxFullLengthStepFilter,
    RepeatedStepFilter,
    ])
instance = IntersectingPolygons(n, fm)
instance.recursion([])
