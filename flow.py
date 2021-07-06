from abc import ABC, abstractmethod
import itertools

# TODO implement filters, including ones not given a class here yet. Might make sense to organize 
#    filters into a separate file at some point
# Remember when defining new filters to add them to the list of filters when instantiating the
#    IntersectingPolygons class
class IntersectionSequenceFilter(ABC):
    n = 5

    @abstractmethod
    def apply_filter(candidate_sequence):
        pass

class DummyFilter(IntersectionSequenceFilter):
    # this is just a dummy filter for testing, filters on sequence length
    def apply_filter(candidate_sequence):
        if len(candidate_sequence) > 3:
            #print(f"Filtered on dummy filter {candidate_sequence}")
            return True

class ParityFilter(IntersectionSequenceFilter):
    """
        relative parity must match positional parity
    """
    def apply_filter(candidate_sequence):
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
        return False

class OrderingFilter(IntersectionSequenceFilter):
    """
        the intersections of consecutive steps must have identical orderings
        ex:
          [0, 1, 3, 5], [1, 4, 3, 5] is valid under this rule
          [0, 1, 3, 5], [3, 4, 1, 5] is not valid under this rule
    """
    def apply_filter(candidate_sequence):
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
    def apply_filter(candidate_sequence):
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
    def apply_filter(candidate_sequence):
        # TODO implement
        return False

class OddLengthStepFilter(IntersectionSequenceFilter):
    """
    an odd length step should be a trunction of a valid even length step
    """
    def apply_filter(candidate_sequence):
        # TODO implement
        return False

class HappyPathFilter(IntersectionSequenceFilter):
    """
    filters out sequences that can't violate the premise
    in particular if the maximum free edges have already been used we can stop the sequence
    """
    # TODO probably could have a better name for this filter
    def apply_filter(candidate_sequence):
        # TODO implement
        return False

class IntersectingPolygons:
    n = 5
    def __init__(cls, filters):
        cls.filters = filters

    def edges(cls):
        return [i + 1 for i in range(cls.n)]

    def generate_candidate_step(cls, candidate_sequence):
        # yield candidate sequence with new element at end
        # TODO should generalize this better
        for candidate in cls.generate_full_size_steps(candidate_sequence):
            yield candidate
        if candidate_sequence:
            # I think initial step can always be full sized step
            for candidate in cls.generate_step_missing_two_edges(candidate_sequence):
                yield candidate
            for candidate in cls.generate_step_missing_three_edges(candidate_sequence):
                yield candidate

    def generate_step_missing_two_edges(cls, candidate_sequence):
        # TODO implement
        dummy_steps = [[5, 1, 2], [2, 3, 4]]
        for candidate in dummy_steps:
            c = candidate_sequence[:]
            c.append(candidate)
            yield c

    def generate_step_missing_three_edges(cls, candidate_sequence):
        # TODO implement
        dummy_steps = [[5, 1], [3, 4]]
        for candidate in dummy_steps:
            c = candidate_sequence[:]
            c.append(candidate)
            yield c

    def generate_full_size_steps(cls, candidate_sequence):
        """
        Generate candidate steps that is one smaller than the total number of edges
        """
        if candidate_sequence:
            last_step = candidate_sequence[-1]
        else:
            last_step = []
        if len(last_step) == cls.n - 1:
            # if last step is missing a single edge, and the next step is also missing a single
            #   edge then can only be missing an edge +/-1 from the last missing edge
            missing_edges = set(cls.edges()).difference(last_step)
            assert len(missing_edges) == 1
            missing_edge = missing_edges.pop()
            for new_missing_edge in [(missing_edge + 1)%cls.n, (missing_edge - 1)%cls.n]:
                if new_missing_edge == 0:
                    new_missing_edge = cls.n
                # maintained edges must retain ordering
                new_step = [x for x in last_step if x != new_missing_edge]
                for i in range(len(new_step) + 1):
                    step = new_step[:i] + [missing_edge] + new_step[i:]
                    c = candidate_sequence[:]
                    c.append(step)
                    yield c
        elif len(last_step) == 0:
            # initial steps, can aways start with a 1
            # TODO I think this even/odd approach may not be correct because I think the
            #   sense of even/oddness that is important isn't based on the number but the 
            #   relative position. Maybe it is okay for the initial step though...
            evens = [i for i in range(cls.n + 1) if i%2 == 0 and i != 0]
            odds = [i for i in range(cls.n + 1) if i%2 == 1 and i != 1]
            for even_permutation in itertools.permutations(evens, len(evens)):
                for odd_permutation in itertools.permutations(odds, len(odds)):
                    step = [1]
                    for i in range(len(evens)):
                        step.append(even_permutation[i])
                        if i < len(odd_permutation) - 1: step.append(odd_permutation[i])
                    yield [step]
        else:
            # TODO are there pre-pruning techniques that should be implemented for a full sized 
            #   step if previous step had more than one missing edge?
            # I think there is a sense of even/oddness that can be used to help, but I'm not
            #   sure I understand it well enough to implement it at this point
            # Should also be able to use the previous step to generate fewer candidates
            for step in itertools.permutations(cls.edges(), cls.n - 1):
                c = candidate_sequence[:]
                c.append(step)
                yield c

    def filter_candidate_step(cls, candidate_sequence):
        for f in cls.filters:
            if f.apply_filter(candidate_sequence):
                return True
        return False

    def end_condition(cls, candidate_sequence):
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

    def recursion(cls, candidate_sequence):
        for x in cls.generate_candidate_step(candidate_sequence):
            if cls.end_condition(x):
                print(f"theoretically met end condition {x}")
            elif not cls.filter_candidate_step(x):
                cls.recursion(x)
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


def test_ordering_filter():
    f = OrderingFilter
    assert not f.apply_filter([])
    assert not f.apply_filter([[]])
    assert not f.apply_filter([[1, 2, 3, 4]])
    assert f.apply_filter([[1, 2, 3, 4], [1, 2, 4, 3]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 5, 3]])
    assert f.apply_filter([[1, 2, 3, 4], [1, 3, 5, 2]])
    assert f.apply_filter([[2, 3, 4], [1, 3, 5, 2]])
    assert f.apply_filter([[2, 3], [1, 3, 5, 2]])
    assert not f.apply_filter([[1, 3, 4], [1, 3, 5, 2]])

def test_repeated_step_filter():
    f = RepeatedStepFilter
    assert not f.apply_filter([])
    assert not f.apply_filter([[]])
    assert not f.apply_filter([[1, 2, 3, 4]])
    assert f.apply_filter([[1, 2, 3, 4], [1, 2, 3, 4]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 4, 3]])
    assert f.apply_filter([[1, 2, 3, 4], [1, 3, 5, 2], [1, 2, 3, 4]])
    assert not f.apply_filter([[2, 3, 4], [2, 3, 4, 5]])
    assert f.apply_filter([[2, 3], [1, 3, 5, 2], [2, 3]])

#test_ordering_filter()
#test_repeated_step_filter()
