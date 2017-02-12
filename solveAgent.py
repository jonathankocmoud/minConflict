""" Source: https://github.com/kushjain/Min-Conflicts
    This file contains different Solving Agents for CSP Problems """

def minConflict(problem, numIter=200000):
    
    """Min Conflict : Solves Constraint Satisfaction Problems.
    Given a possible assignment of all variables in CSP, it re-assigns all variables iteratively untill all contraints are satisfied
    INPUTS:
    problem: CSP Problem
    numIter: Number of maximum Iterations Allowed
    OUTPUT
    Solution to CSP, or failure
    """
    
    print 'number of iterations =', numIter
    state = problem.getStartState()
    print "Initial State"
    problem.visualize(state)

    for i in range(numIter):
        
        var = problem.getVar(state)      #Get the next conflicted variable randomly

        #No conflict, i.e. We have solved the problem
        if var == -1:
            print "Solution state found in", i, "iterations"
            problem.visualize(state)
            return state
        # Try a new state
        state = problem.getNewState(state, var)
    
    print "With " + str(numIter) + " iterations, the problem was not solved completely."
    return []
