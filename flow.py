from filters import *
from polygon_intersection_generator import PolygonIntersectionGenerator

class IntersectingPolygons:
    # TODO ultimately n should probably be a parameter that gets passed in to initializer rather
    #   than being hardcoded here
    n = 5
    steps_count = 0
    def __init__(self, filters):
        self.filters = []
        for f in filters:
            self.filters.append(f(self.n))
        self.generator = PolygonIntersectionGenerator(IntersectingPolygons.n)

    def filter_candidate_step(self, candidate_sequence):
        for f in self.filters:
            if f.apply_filter(candidate_sequence):
                return True
        return False

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
        if self.steps_count %1000 == 0: print(f"Step count {self.steps_count}, sequence {candidate_sequence}")
        for x in self.generator.generate_candidate_step(candidate_sequence):
            if not self.filter_candidate_step(x):
                if self.end_condition(x):
                    print(f"theoretically met end condition {x}")
                else:
                    self.recursion(x)
            else:
                #print(f"filtered out {x}")
                pass

instance = IntersectingPolygons([
    DummyFilter,
    ParityFilter,
    Lemma1Filter,
    OrderingFilter,
    MaxFullLengthStepFilter,
    RepeatedStepFilter,
    OddLengthStepFilter,
    HappyPathFilter,
    ])
instance.recursion([])
# when running this it's generating 4 initial options for 5 edges, I seem to remember only 2 are valid, but I'm not sure what the rule
#   that eliminates two of them is (I think the two that contain edge 5 are the ones that shouldn't be included)


