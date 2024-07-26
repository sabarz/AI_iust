from sre_parse import State


def hill_climbing(problem , state):
    ''' Returns a state as the solution of the problem '''
    current = []
    current = state

    neighbor = problem.neighbors(current)
    ans = problem.value(state)
    nmd = current
    for i in neighbor:
        if(problem.value(i)<= ans):
            ans = problem.value(i)
            nmd = i
    if(ans > problem.value(current)):
        return current 
    else:
        return nmd


def hill_climbing_random_restart(problem, limit = 10):
    state = problem.initial()
    cnt = 0
    while problem.goal_test(state) == False and cnt < limit:
        state = hill_climbing(problem , state)
        cnt += 1
    return state
