import itertools

class PolygonIntersectionGenerator:
    def __init__(self, n):
        self.n = n

    def edges(self):
        return [i + 1 for i in range(self.n)]

    def generate_candidate_step(self, candidate_sequence):
        # yield candidate sequence with new element at end
        # TODO should generalize this better
        for candidate in self.generate_full_size_steps(candidate_sequence):
            yield candidate
        if candidate_sequence:
            # I think initial step can always be full sized step. TODO - verify
            for candidate in self.generate_step_missing_k_edges(2, candidate_sequence):
                yield candidate
            for candidate in self.generate_step_missing_k_edges(3, candidate_sequence):
                yield candidate

    def generate_step_missing_k_edges(self, k, candidate_sequence):
        edge_count = self.n - k
        #   select n - k edges to include
        for new_edges in itertools.combinations(self.edges(), edge_count):
            #   find intersection of that set of edges with edges from previous step in sequence
            #   order intersection by ordering in previous step
            previous_step = candidate_sequence[-1]
            ordered_edges = [e for e in previous_step if e in new_edges]
            #   randomly place remaining edges (possibly subject to pre-filtering criteria)
            remaining_edges = [e for e in new_edges if e not in ordered_edges]
            for placement_permutation in itertools.permutations(range(edge_count), len(remaining_edges)):
                candidate = [-1]*(edge_count) # initialize candidate to correct length
                for i in range(len(remaining_edges)):
                    candidate[placement_permutation[i]] = remaining_edges[i]
                next_edge_ix = 0
                for i, e in enumerate(candidate):
                    if e == -1:
                        candidate[i] = ordered_edges[next_edge_ix]
                        next_edge_ix += 1
                c = candidate_sequence[:]
                c.append(candidate)
                yield c

    def generate_initial_full_size_step(self):
        # initial steps, can aways start with a 1
        # TODO I think this even/odd approach may not be correct because I think the
        #   sense of even/oddness that is important isn't based on the number but the 
        #   relative position. Maybe it is okay for the initial step though...
        evens = [i for i in range(self.n + 1) if i%2 == 0 and i != 0]
        odds = [i for i in range(self.n + 1) if i%2 == 1 and i != 1]
        for even_permutation in itertools.permutations(evens, len(evens)):
            for odd_permutation in itertools.permutations(odds, len(odds)):
                step = [1]
                for i in range(len(evens)):
                    step.append(even_permutation[i])
                    if i < len(odd_permutation) - 1: step.append(odd_permutation[i])
                yield [step]
    
    def generate_full_size_step_from_smaller(self, candidate_sequence):
        # TODO are there pre-pruning techniques that should be implemented for a full sized 
        #   step if previous step had more than one missing edge?
        # I think there is a sense of even/oddness that can be used to help, but I'm not
        #   sure I understand it well enough to implement it at this point
        # Should also be able to use the previous step to generate fewer candidates
        for step in self.generate_step_missing_k_edges(1, candidate_sequence):
            yield step
        #for step in itertools.permutations(self.edges(), self.n - 1):
        #    c = candidate_sequence[:]
        #    c.append(step)
        #    yield c
    
    def generate_full_size_step_from_full(self, candidate_sequence):            
        # if last step is missing a single edge, and the next step is also missing a single
        #   edge then can only be missing an edge +/-1 from the last missing edge
        last_step = candidate_sequence[-1]
        missing_edges = set(self.edges()).difference(last_step)
        assert len(missing_edges) == 1
        missing_edge = missing_edges.pop()
        for new_missing_edge in [(missing_edge + 1)%self.n, (missing_edge - 1)%self.n]:
            if new_missing_edge == 0:
                new_missing_edge = self.n
            # maintained edges must retain ordering
            new_step = [x for x in last_step if x != new_missing_edge]
            for i in range(len(new_step) + 1):
                step = new_step[:i] + [missing_edge] + new_step[i:]
                c = candidate_sequence[:]
                c.append(step)
                yield c

    def generate_full_size_steps(self, candidate_sequence):
        """
        Generate candidate steps that is one smaller than the total number of edges
        """
        if candidate_sequence:
            last_step = candidate_sequence[-1]
        else:
            last_step = []
        if len(last_step) == self.n - 1:
            for step in self.generate_full_size_step_from_full(candidate_sequence):
                yield step
        elif len(last_step) == 0:
            for step in self.generate_initial_full_size_step():
                yield step
        else:
            for step in self.generate_full_size_step_from_smaller(candidate_sequence):
                yield step
    
