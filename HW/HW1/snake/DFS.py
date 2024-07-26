
from inspect import stack
from re import S
from Utility import Node
from Algorithm import Algorithm


class DFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def dfs(self , snake) :
        
        stack = []
        visited = []
        start , finish = self.get_initstate_and_goalstate(snake)
        
        visited.append(start)
        stack.append(start)
        s = start

        while(len(stack) > 0) :
            s = stack.pop()
            
            if(finish.equal(s)) :
                self.get_path(s)

            if(s not in visited) :
                visited.append(s)

            neighbors = []
            neighbors = self.get_neighbors(s)

            for item in neighbors :
                if(item not in visited and item not in stack and not self.outside_boundary(item) and not self.inside_body(snake ,item)) :
                    item.parent = s
                    stack.append(item)
                     
        return s

    def run_algorithm(self, snake):
        #################################################################################
        if(len(self.path) == 0) :
            self.dfs(snake)
        
        if(len(self.path) != 0):
            return self.path.pop()
        else:
            return None      

