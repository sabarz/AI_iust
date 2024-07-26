from collections import deque
import queue
from Utility import Node
from Algorithm import Algorithm


class BFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)
    
    def bfs(self , snake) :
        
        queue = []
        visited = []
        start , finish = self.get_initstate_and_goalstate(snake)
        
        visited.append(start)
        queue.append(start)
        s = start
        
        while(len(queue) > 0) :
            s = queue.pop(0)
            
            if(finish.equal(s)) :
                self.get_path(s)

            if(s not in visited) :
                visited.append(s)

            neighbors = []
            neighbors = self.get_neighbors(s)

            for item in neighbors :
                if(item not in visited and item not in queue and not self.outside_boundary(item) and not self.inside_body(snake ,item)) :
                    item.parent = s
                    queue.append(item)
                     
        return s

    def run_algorithm(self, snake):
        #################################################################################
        if(len(self.path) == 0) :
            self.bfs(snake)
            
        if(len(self.path) != 0):
            return self.path.pop()
        else:
            return None
        #################################################################################
        
