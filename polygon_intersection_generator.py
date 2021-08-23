import itertools

    
class PolygonIntersectionGenerator:
    def __init__(self, n):
        assert n%2==1, f"n must be odd, got {n}"
        self.n = n# n is the number of edges of P
        
        # TODO max_freedoms is also defined in filters, better if only be defined in one place
        # allowed freedoms is the total amount that steps are less than full sized and so potentially
        #   break the conjecture by having two polygons with greater than the proposed number of
        #   intersections
        # this conjecture allows for n - 3 so we don't need to check those because they are allowed
        #   we also don't need to consider n - 4 since that would not lead to a valid polygon since
        #   it would imply the sequence was currently inside the polygon but with no freedom to
        #   get back outside
        self.allowed_freedoms = self.n - 5

    def remaining_freedoms(self, candidate_sequence):
        return self.allowed_freedoms - sum([(self.n - 1) - len(step) for step in candidate_sequence])

    def edges(self):#edges is a list 1,...,n of the edges of P
        return [i + 1 for i in range(self.n)]

    def generate_candidate_step(self, candidate_sequence):
        # yield candidate sequence with new element at end
        if not candidate_sequence: # the first term in the sequence is special
            for candidate in self.generate_initial_full_size_step():
                print(candidate)
                yield candidate
        elif self.is_outside_polygon(candidate_sequence):
            # a sequence that is currently inside the polygon cannot have the next step
            # be full sized
            for candidate in self.generate_full_size_steps(candidate_sequence):
                yield candidate
        
        if candidate_sequence: 
        # The initial step can always be full sized step, so only need to do this after
        #   there is at least one step
            for num_fewer_edges in range(1, self.remaining_freedoms(candidate_sequence) + 1):
            # TODO I think this is correct, but would be good to verify with tests
                for candidate in self.generate_step_missing_k_edges(num_fewer_edges + 1, candidate_sequence):
                    # num_fewer_edges + 1 since a full sized step is missing 1
                    yield candidate

    def is_outside_polygon(self, candidate_sequence):
        """
        A sequence will always start outside of the polygon, any step with an odd number
          of intersections will be inside the polygon.
        """
        return sum([len(step) for step in candidate_sequence])%2 == 0

    def generate_step_missing_k_edges(self, k, candidate_sequence):
        """
        Generates candidate steps with n-k itersections
        Preserves ordering relative to previous step
        """
        edge_count = self.n - k
        last_step = candidate_sequence[-1]
        #   select n - k edges to include
        if k==2 and len(last_step)==self.n-1:
            #if the previous step is a full step, then this is just a truncation of a valid
            # full sequence successor   
            
            #two candidate steps are truncations of previous step
            c = candidate_sequence[:]
            c.append(last_step[1:])
            yield c
            c = candidate_sequence[:]
            c.append(last_step[:-1])
            yield c

            missing_edges = set(self.edges()).difference(last_step)
            assert len(missing_edges) == 1
            missing_edge = missing_edges.pop()
            for new_missing_edge in [(missing_edge + 1)%self.n, (missing_edge - 1)%self.n]:
                if new_missing_edge == 0:
                    new_missing_edge = self.n
            
                new_step= [missing_edge if x==new_missing_edge else x for x in last_step]
                if not(last_step[0]==new_missing_edge):
                    c = candidate_sequence[:]
                    c.append(new_step[1:])
                    yield c
                if not(last_step[-1]==new_missing_edge):
                    c = candidate_sequence[:]
                    c.append(new_step[:-1])
                    yield c

        else:
            for new_edges in itertools.combinations(self.edges(), edge_count):
                #   find intersection of that set of edges with edges from previous step in sequence
                #   order intersection by ordering in previous step
                
                # TODO consider if we can/should bother to improve efficiency here over `e in _edges` which is n^2
                ordered_edges = [e for e in last_step if e in new_edges]
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
        #We can assume that the initial step is full-sized and misses edge n
        evens = [i for i in range(2,self.n, 2)]
        odds = [i for i in range(1, self.n-1, 2)]
        for even_permutation in itertools.permutations(evens, len(evens)):
            for odd_permutation in itertools.permutations(odds, len(odds)):
                step = []
                for i in range(len(evens)):
                    step.append(odd_permutation[i])
                    step.append(even_permutation[i])
                yield [step]
    
    def generate_full_size_step_from_smaller(self, candidate_sequence):
        # TODO are there pre-pruning techniques that should be implemented for a full sized 
        #   step if previous step had more than one missing edge?
        # I think there is a sense of even/oddness that can be used to help, but I'm not
        #   sure I understand it well enough to implement it at this point
        # Should also be able to use the previous step to generate fewer candidates
        for step in self.generate_step_missing_k_edges(1, candidate_sequence):
            yield step
    
    def generate_full_size_step_from_full(self, candidate_sequence):            
        """
        Generates n-1 length candidate steps when previous step also had n-1 length
        Preserves ordering of previous step

        This is special cased because if last step is missing a single edge,
          and the next step is also missing a single edge then can only be missing
          an edge +/-1 from the last missing edge. Furthermore, the new step is just the old step
          with the new edge inserted in the exact spot that was occupied by the new missing edge 
        """
        last_step = candidate_sequence[-1]
        missing_edges = set(self.edges()).difference(last_step)
        assert len(missing_edges) == 1
        missing_edge = missing_edges.pop()
        for new_missing_edge in [(missing_edge + 1)%self.n, (missing_edge - 1)%self.n]:
            if new_missing_edge == 0:
                new_missing_edge = self.n
            
            new_step= [missing_edge if x==new_missing_edge else x for x in last_step]
            c = candidate_sequence[:]
            c.append(new_step)
            yield c

    def generate_full_size_steps(self, candidate_sequence):
        """
        Generate candidate steps that is one smaller than the total number of edges
        Successive steps preserve ordering of previous step

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
