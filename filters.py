from abc import ABC, abstractmethod

# TODO implement filters, including ones not given a class here yet. Might make sense to organize 
#    filters into a separate file at some point
# Remember when defining new filters to add them to the list of filters when instantiating the
#    IntersectingPolygons class

class IntersectionSequenceFilter(ABC):
    def __init__(self, n):
        self.n = n

    @abstractmethod
    def apply_filter(self, candidate_sequence):
        pass

class DummyFilter(IntersectionSequenceFilter):
    # this is just a dummy filter for testing, filters on sequence length
    def apply_filter(self, candidate_sequence):
        if len(candidate_sequence) > 3:
            #print(f"Filtered on dummy filter {candidate_sequence}")
            return True

class ParityFilter(IntersectionSequenceFilter):
    """
        relative parity must match positional parity
    """
    def apply_filter(self, candidate_sequence):
        """Returns True if step should be filtered out, returns False otherwise
        """
        return False

class Lemma1Filter(IntersectionSequenceFilter):
    """
    filter on lemma 1 from paper (probably should update this description along with implementing)
    """
    def apply_filter(self, candidate_sequence):
        """Returns True if step should be filtered out, returns False otherwise
        """
        # TODO implement
        return False

class OrderingFilter(IntersectionSequenceFilter):
    """
        the intersections of consecutive steps must have identical orderings
        ex:
          [0, 1, 3, 5], [1, 4, 3, 5] is valid under this rule
          [0, 1, 3, 5], [3, 4, 1, 5] is not valid under this rule
    """
    def apply_filter(self, candidate_sequence):
        if len(candidate_sequence) > 1:
            last_step = candidate_sequence[-1]
            second_to_last_step = candidate_sequence[-2]
            index = 0
            max_index = 0
            for edge in second_to_last_step:
                if edge in last_step:
                    index = last_step.index(edge)
                    if index < max_index:
                        #print(f"filtered on ordering {candidate_sequence}")
                        return True
                    max_index = index
        return False
    
class RepeatedStepFilter(IntersectionSequenceFilter):
    """
    A sequence should never have a repeated step
    We'll assume that only the last step in the sequence might introduce a repeat
        i.e. assume the previous steps have already been validated
    """
    def apply_filter(self, candidate_sequence):
        if len(candidate_sequence) > 1:
            last_step = candidate_sequence[-1]
            for step in candidate_sequence[:-1]:
                if( len(step) == len(last_step) 
                        and all([last_step[i] == step[i] for i in range(len(step))]) ):
                    #print(f"Filter on repeated step {candidate_sequence}")
                    return True
        return False

class MaxFullLengthStepFilter(IntersectionSequenceFilter):
    """
    a sequence should never have more than three consecutive n-1 length steps
    """
    def apply_filter(self, candidate_sequence):
        if len(candidate_sequence)>3:
            if all([len(candidate_sequence[-(i+1)])==IntersectionSequenceFilter.n-1 for i in range(4)]):
                return True
        return False

class OddLengthStepFilter(IntersectionSequenceFilter):
    """
    an odd length step should be a trunction of a valid even length step
    """
    def apply_filter(self, candidate_sequence):
        # TODO implement
        return False

class HappyPathFilter(IntersectionSequenceFilter):
    """
    filters out sequences that can't violate the premise
    in particular if the maximum free edges have already been used we can stop the sequence
    """
    # TODO probably could have a better name for this filter
    def __init__(self, n):
        self.n = n
        # can have this fewer than this many intersections under full accumulated in a sequence and still
        #  potentially reach a contradictory example
        self.max_freedoms = self.n - 3 

    def apply_filter(self, candidate_sequence):
        if sum([(self.n - 1) - len(step) for step in candidate_sequence]) >= self.max_freedoms:
            #print(f"filtered for happy path {candidate_sequence}")
            return True
        return False

