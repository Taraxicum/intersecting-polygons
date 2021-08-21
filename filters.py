from abc import ABC, abstractmethod

# Remember when defining new filters to add them to the list of filters when instantiating the
#    IntersectingPolygons class
class FilterManager:
    def __init__(self, n, filters):
        self.n = n
        self.filters = []
        for f in filters:
            self.filters.append(f(self.n))
    
    def filter_candidate_step(self, candidate_sequence):
        for f in self.filters:
            if f.apply_filter(candidate_sequence):
                return True
        return False

class IntersectionSequenceFilter(ABC):
    def __init__(self, n):
        self.n = n
    def edges(self):#edges is a list 1,...,n of the edges of P
        return [i + 1 for i in range(self.n)]


    @abstractmethod
    def apply_filter(self, candidate_sequence):
        pass

class ParityFilter(IntersectionSequenceFilter):
    """
        relative parity must match positional parity
        the parity filter only applies to connected chains of edges
        ex:
        if you hit edges 1,2,3,5,6,7 of a 9-gon then the parity filter 
          could apply to each of the two chains {1,2,3} and {5,6,7} of the 9-gon.
        In particular it would disallow  [1,5,2,3,6,7] since 1 and 5 can't be
          adjacent since they have the same relative parity (so they can't have opposite
          positional parity)
        Note we do need to pay attention to wrapping around (e.g. in a 9-gon {8, 9, 1} 
          would be a connected chain of edges - which would be allowed in that order)
    """
    # TODO handle wrapping case
    def apply_filter(self, candidate_sequence):
        """
        Returns True if step should be filtered out, returns False otherwise
        Only filters on the last step, assumes previous steps have been previously filtered.
        """
        if len(candidate_sequence) < 1:
            return False
        last_step = candidate_sequence[-1]
        parities = dict()
        for ix, val in enumerate(last_step):
            parities[val] = ix%2

        for i in last_step:
            incremented = (i+1)%self.n or self.n # increments mod n, if 0 use n instead
            if incremented in parities:
                if parities[i] == parities[incremented]:
                    return True
        return False

class Lemma1Filter(IntersectionSequenceFilter):
    """
    filter on lemma 1 from paper (TODO probably should update this description)
    """
    def apply_filter(self,candidate_sequence):
        """Returns True if step should be filtered out, returns False otherwise
        """
        k=len(candidate_sequence)
        if k>2:
            last_step=candidate_sequence[-1]
            for i in range(k-2):#If this is run in conjunction with OrderingFilter then we don't need to look at candidate_sequence[k-2] 
                direction_changes=0
                too_many_directions=False
                step=candidate_sequence[i]
                intersection=[edge for edge in step if edge in last_step]#first suppose that last_step points at step
                if len(intersection)<4:
                    break
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

