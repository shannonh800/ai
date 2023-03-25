import copy

# function to clean input
def format_input(fileName):
    file = open(fileName, "r")
    inputText = file.read()
    
    inputAndBackMatter = inputText.split("0")
    
    inputBackMatter = inputAndBackMatter[1]

    inputToUse = inputAndBackMatter[0].strip("\n")    # capture everything in before the line with "0"
    inputLines = inputToUse.split("\n")
    stringClauses = [line.strip() for line in inputLines]    # remove extra whitespace
    stringClauses = [clause.split() for clause in stringClauses]    # turn each atom of the clauses into a list element
    
    # convert input clauses to integers
    inputClauses = []
    for clause in stringClauses:
        inputClauses.append(list(map(int, clause)))

    # convert atoms to integers
    atoms = []
    for clause in inputClauses:
        for atom in clause:
            propAtom = abs(int(atom))
            if propAtom not in atoms:
                atoms.append(propAtom)
    # print(atoms)
    inputAtomsAndClausesAndBackMatter = [atoms, inputClauses, inputBackMatter]
    # print(inputAtomsAndClauses)
    return inputAtomsAndClausesAndBackMatter


'''
inputs:
    * ATOMS - set of propositional atoms
    * S - Set of propositional clauses in CNF
returns:
    * either a valuation on ATOMS satisfying S or NIL if none exists
'''
def dpll_algo(atoms, S):
    V = {atom: "UNBOUND" for atom in atoms}    # let V be an array of the atoms value assignments, initialized to "UNBOUND" for each atom

    #print("s length:", len(S))

    return dp1(atoms,S,V)
    #return dp1(atoms, [[1,2],[],[3]], V)

def dp1(atoms,S,V):     # call S,V by value
    #print("inside V:", V)
    # BASE OF THE RECURSION: SOLUTION FOUND OR FAILURE 
    recursionBase(atoms, S, V)

    # EASY CASES: PURE LITERAL ELIMINATION AND FORCED ASSIGNMENT
    pureLiteralExists = True
    singletonExists = True
    while pureLiteralExists or singletonExists:
        #print("STARTING PURE SEARCH")
        # check if there are pure literals
        # go through and find all the pure literals first, add them to an array called pureLiterals
        pureLiterals = []
        #print("current S:", S)
        for atom in atoms:
            if V[atom] == "UNBOUND":
                #print("iterating on next unbound atom", atom)
                pure = False
                sign = "unassigned"
                print("S for pure literals:", S)
                for clause in S:
                    #print("current clause:", clause)
                    #print("sign:", sign)
                    #print("pure:", pure)
                    if atom in clause or (atom*-1) in clause:
                        if atom in clause:
                            #print("atom in clause")
                            if sign == "unassigned":
                                sign = "positive"
                                pure = True
                            elif sign == "negative":
                                pure = False
                        elif atom*-1 in clause:
                            #print("atom*-1 in clause")
                            if sign == "unassigned":
                                sign = "negative"
                                pure = True
                            elif sign == "positive":
                                pure = False
                    #print("pure:", pure)
                if pure == True:
                    print("found pure literal, atom:", atom)
                    if sign == "positive":
                        literal = atom
                    elif sign == "negative":
                        literal = atom*-1
                    pureLiterals.append([atom, literal])
        #print("pureLiterals:", pureLiterals)
        # if pure literals exist, then propogate
        if len(pureLiterals) != 0:
            for atom, literal in pureLiterals:
                V = obviousAssign(atom, literal, V)
                #print("atom's assignment:", V)
                for clause in copy.deepcopy(S):    # delete every clause containing L from S
                    #print("S:", S)
                    #print("checking clause:", clause)
                    #print("literal:", literal)
                    if literal in clause:
                        #print("literal in clause")
                        S.remove(clause)
                    # BASE OF THE RECURSION: SOLUTION FOUND OR FAILURE 
                result = recursionBase(atoms, S, V)
                if result != None:
                    return result
        elif len(pureLiterals) == 0:
            pureLiteralExists = False
        
        #print("pure literals exist:", pureLiteralExists)

        #print("DONE PURE LITERALS SEARCH")
        #print("V:", V)
        #print("S:", S)

        # if there exists a literal L in S with only one sign appearing in S (pure literal elimination)
        #print("STARTING SINGLETONS SEARCH")
        singletons = []
        for clause in S:
            #print("current clause:", clause)
            if len(clause) == 1:
                #print("clause length == 1")
                singletonClause = clause[0]
                if singletonClause < 0:
                    singletons.append([singletonClause*-1, singletonClause])
                elif singletonClause > 0:
                    singletons.append([singletonClause, singletonClause])
        print("singletons:", singletons)
        if len(singletons) != 0:      # Forced assignment if singleton clauses exist
            for atom, literal in singletons:
                if V[atom] == "UNBOUND":
                    V = obviousAssign(atom, literal, V)
                    #print("atom's assignment:", atom, V[atom])
                    print("atom to propogate:", atom)
                    S = propagate(atom, S, V)
                    #print("S here:", S)
                    result = recursionBase(atoms, S, V)
                    if result != None:
                        return result
        elif len(singletons) == 0:
            singletonExists = False
        
        #print("DONE SINGLETONS SEARCH")
        #print("singletonExists:", singletonExists)
        print("V after easy cases:", V)
        print("S after easy cases:", S)

    #print("STARTING HARD CASES")
    # HARD CASE: PICK An ATOM AND TRY EACH VALUE ASSIGNMENT IN TURN 
    atomToAssign = 1
    atomChosen = False
    while not atomChosen:
        if V[atomToAssign] == "UNBOUND":
            #print("Atom to be assigned true:", atom)
            atomChosen = True
            VCopy = copy.deepcopy(V)
            V[atomToAssign] = True      # Try one assignment
            print("atom that was assigned hard case:", atomToAssign)
            print("S here:", S)
            print("V here:", V)
            print("\n")
            S1 = copy.deepcopy(S)

            print("")
            S1 = propagate(atomToAssign, S1, V)
            print("S1:", S1)
            VNEW = dp1(atoms, S1, V)
            if (VNEW != "NIL"):
                return(VNEW)        # Found a satisfying valuation
            
            print("failure somewhere, VNEW:", VNEW)
            
            # If V[atom] = TRUE didn't work, try V[atom] = FALSE;
            VCopy[atomToAssign] = False
            S1 = copy.deepcopy(S)
            print("S1 that we backed up to:", S1)
            print("V that we backed up to:", VCopy)
            S1 = propagate(atomToAssign, S1, VCopy)
            print("S1 after propogating the False value for the atom:", atomToAssign, S1)
            print("V after we propogated the False value for the atom:", VCopy)
            return(dp1(atoms,S1,VCopy))     # Either found a satisfying valuation or backtrack
            # end dp1
        atomToAssign += 1


def propagate(atom,S,V):
    clausesToDelete = []
    for index in range(len(S)):
        if (atom in S[index] and V[atom] == True) or (atom*-1 in S[index] and V[atom] == False):
            #print("HERE")
            clausesToDelete.append(S[index])
        elif (atom in S[index] and V[atom] == False):
            #print("OR HERE")
            S[index].remove(atom)
        elif (atom*-1 in S[index] and V[atom] == True):
            #print("HERE 3")
            S[index].remove(atom*-1)
    #print("Atom Indices:", atomInClausesToDelete)
    #print("clause Indices:", clausesToDelete)
    for clause in clausesToDelete:
        #print("S inside:", S)
        S.remove(clause)
    print("new new S:", S)
    
    return S


# Given a literal L with atom A, make V[A] the sign indicated by L.
def obviousAssign(atom, literal, V):
    if literal > 0:
        V[atom] = True
    elif literal < 0:
        V[atom] = False
    return V

def recursionBase(atoms, S, V):
    #print("CHECKING FOR RECURSION BASE")
    #print("current S", S)
    #print("current V:", V)
    
    # BASE OF THE RECURSION: SOLUTION FOUND OR FAILURE 
    if len(S) == 0:      # SUCCESS: S is empty, all clauses are satisfied, solution found   
        for atom in atoms:
            if V[atom] == "UNBOUND":
                V[atom] = True     # arbitrarily assign all atoms that can be either value to be TRUE
        #print("Final V:", V)
        #print("SUCCESS")
        return V

    #print("S:", S)
    for clause in S:
        #print("clause:", clause)
        if clause == []:    #  FAILURE: at least one clause in S is empty
            #print("FAILURE")
            return "NIL"    # unsatisfiable under V 


# FIX OUTPUT FORMAT
def dpll_main():
    inputText = format_input("sample.txt")
    #print("inputText is:", inputText)

    atoms = inputText[0]    # let atoms be an array of the atoms
    S = inputText[1]
    inputBackMatter = inputText[2]

    #print("atoms, S:", atoms, S)
    result = dpll_algo(atoms, S)

    '''
    if result != "NIL":
        for atom in result:
            print(atom, end=" ")
            if result[atom] == False:
                print("F")
            elif result[atom] == True:
                print("T")
    # if no solution found for input clauses, simply output 0
    print("0", end="")
    print(inputBackMatter)
    '''
    
    # output result into a new file called dpll_output.txt
    f = open("dpll_output.txt", "w")
    if result != "NIL":
        for atom in result:
            f.write(str(atom) + " ")
            if result[atom] == False:
                f.write("F\n")
            elif result[atom] == True:
                f.write("T\n")
    # if no solution found for input clauses, simply output 0
    f.write("0")
    f.write(inputBackMatter)
    f.close()

dpll_main()