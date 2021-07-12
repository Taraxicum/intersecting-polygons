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
        the parity filter only applies to connected chains of edges
        ex:
        if you hit edges 1,2,3,5,6,7 of a 9-gon then the parity filter 
          could apply to each of the two chains {1,2,3} and {5,6,7} of the 9-gon.
        In particular it would disallow  [1,3,2,5,6,7] since 1 and 3 can't be
          adjacent since they have equal relative parity (so they can't have opposite
          positional parity)
        Note we do need to pay attention to wrapping around (e.g. in a 9-gon {8, 9, 1} 
          would be a connected chain of edges - that would be allowed in that order)
    """
    def apply_filter(self, candidate_sequence):
        """Returns True if step should be filtered out, returns False otherwise
        """
        return False

class Lemma1Filter(IntersectionSequenceFilter):
    """
    filter on lemma 1 from paper (probably should update this description along with implementing)
    """
    def apply_filter(candidate_sequence):
        """Returns True if step should be filtered out, returns False otherwise
        """
        # TODO implement
        k=len(candidate_sequence)
        if k>2:
            last_step=candidate_sequence[-1]
            for i in range(k-2):#If this is run in conjunction with OrderingFilter then we don't need to look at candidate_sequence[k-2] 
                direction_changes=0
                too_many_directions=False
                step=candidate_sequence[i]
                intersection=[edge for edge in step if edge in last_step]#first suppose that last_step points at step
                #for edge in step:
                #    if edge in last_step:
                if last_step.index(intersection[1])>last_step.index(intersection[0]):
                    direction=1
                else:
                    direction=0
                for i in range(2,len(intersection)):#go through the edges on step, left-to-right, and check for direction changes on last_step
                    if last_step.index(intersection[i])>last_step.index(intersection[i-1]):
                        new_direction=1
                    else:
                        new_direction=0
                    if new_direction!=direction:
                        direction=new_direction
                        direction_changes+=1
                    if direction_changes>1:
                        too_many_directions=True
                        break
                if too_many_directions:
                    intersection=[edge for edge in last_step if edge in step]#now suppose that step points at last_step
                    if step.index(intersection[1])>step.index(intersection[0]):
                        direction=1#1 means right, 0 means left
                    else: 
                        direction=0
                    for i in range(2,len(intersection)):
                        if step.index(intersection[i])>step.index(intersection[i-1]):
                            new_direction=1
                        else:
                            new_direction=0
                        if new_direction!=direction:
                            direction=new_direction
                            direction_changes+=1
                        if direction_changes>1:
                            return True
   
        return False


class OrderingFilter(IntersectionSequenceFilter):
    """
        the intersections of consecutive steps must have identical orderings
        ex:
          [0, 1, 3, 5], [1, 4, 3, 5] is valid under this rule
          [0, 1, 3, 5], [3, 4, 1, 5] is not valid under this rule
    """
    #TODO this is probably better to enforce in the generation stage rather than the filtering stage
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
                        print(f"filtered on ordering {candidate_sequence}")
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
            if all([len(candidate_sequence[-(i+1)])==self.n-1 for i in range(4)]):
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

