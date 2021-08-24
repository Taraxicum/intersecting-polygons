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
    def update_edge_indices(self, index_cache, step, step_index):
        """
        """
        if step_index in index_cache:
            return #already indexed this step
        index_cache[step_index] = dict()
        for ix, edge in enumerate(step):
            index_cache[step_index][edge] = ix

    def has_too_many_direction_changes(self, index_cache, step_a, step_b, step_b_index):
        """
        checks directions changes if step_b is pointing at step_a, more than one direction change is too many
        """
        intersection=[edge for edge in step_a if edge in index_cache[step_b_index]]
        if len(intersection)<4: # can't have more than one direction change with at most 3 edges
            return False
        if index_cache[step_b_index][intersection[1]]>index_cache[step_b_index][intersection[0]]:
            direction=1
        else:
            direction=0
        
        direction_changes=0
        for k in range(2,len(intersection)):#go through the edges on step, left-to-right, and check for direction changes on step_b
            if index_cache[step_b_index][intersection[k]]>index_cache[step_b_index][intersection[k-1]]:
                new_direction=1
            else:
                new_direction=0
            if new_direction!=direction:
                direction=new_direction
                direction_changes+=1
            if direction_changes>1:
                return True
        return False

    def apply_filter(self,candidate_sequence):
        """Returns True if step should be filtered out, returns False otherwise
        """
        step_count=len(candidate_sequence)
        if step_count<=2:
            return False

        last_step=candidate_sequence[-1]
        last_step_index = step_count-1
        index_cache = dict()
        self.update_edge_indices(index_cache, last_step, last_step_index)

        for step_index in range(step_count-2):#If this is run in conjunction with OrderingFilter then we don't need to look at candidate_sequence[step_count-2] 
            step=candidate_sequence[step_index]
            self.update_edge_indices(index_cache, step, step_index)

            if self.has_too_many_direction_changes(index_cache, step, last_step, last_step_index): # first suppose last_step points at step
                #now suppose that step points at last_step
                return self.has_too_many_direction_changes(index_cache, last_step, step, step_index)
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
    #TODO move into generator
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
