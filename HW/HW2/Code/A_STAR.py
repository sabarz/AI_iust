from lib2to3.pytree import Node
from operator import indexOf
from platform import node
from Algorithm import Algorithm


class A_STAR(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        #################################################################################
        self.frontier = []
        self.explored_set = []
        self.path = []
        start , finish = self.get_initstate_and_goalstate(snake)
        self.frontier.append(start)
        while(len(self.frontier) > 0):
            hold = min(self.frontier,key=lambda x:x.f)
            self.frontier.remove(hold)
            self.explored_set.append(hold)

            neighbors = []
            neighbors = self.get_neighbors(hold)
            
            if finish.equal(hold):
                return self.get_path(hold)

            for item in neighbors :    
                if(not self.outside_boundary(item) and not self.inside_body(snake ,item) and item not in self.explored_set and item not in self.frontier):
                    
                    item.g = hold.g + 1
                    item.h = self.manhattan_distance(item , finish)
                    item.f = item.g + item.h
                    item.parent = hold
                    
                    self.frontier.append(item)
        #################################################################################
        return None
