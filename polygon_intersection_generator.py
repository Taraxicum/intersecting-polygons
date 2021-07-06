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
            # I think initial step can always be full sized step
            for candidate in self.generate_step_missing_two_edges(candidate_sequence):
                yield candidate
            for candidate in self.generate_step_missing_three_edges(candidate_sequence):
                yield candidate

    def generate_step_missing_two_edges(self, candidate_sequence):
        # TODO implement
        dummy_steps = [[5, 1, 2], [2, 3, 4]]
        for candidate in dummy_steps:
            c = candidate_sequence[:]
            c.append(candidate)
            yield c

    def generate_step_missing_three_edges(self, candidate_sequence):
        # TODO implement
        dummy_steps = [[5, 1], [3, 4]]
        for candidate in dummy_steps:
            c = candidate_sequence[:]
            c.append(candidate)
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
            # if last step is missing a single edge, and the next step is also missing a single
            #   edge then can only be missing an edge +/-1 from the last missing edge
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
        elif len(last_step) == 0:
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
        else:
            # TODO are there pre-pruning techniques that should be implemented for a full sized 
            #   step if previous step had more than one missing edge?
            # I think there is a sense of even/oddness that can be used to help, but I'm not
            #   sure I understand it well enough to implement it at this point
            # Should also be able to use the previous step to generate fewer candidates
            for step in itertools.permutations(self.edges(), self.n - 1):
                c = candidate_sequence[:]
                c.append(step)
                yield c
