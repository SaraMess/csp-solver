import sys
sys.path.insert(1, '../')
from csp import CSP 

########################## TEST PROGRAM FOR THE LEWIS & CAROLL PROBLEM ##############################

### postive logic
print("##### POSITIVE LOGIC #####")
path = "../../Data/lewisCaroll_p.txt" 
csp = CSP(path, 25,'positive')
print("Variables: \n", csp.map)
print("Constraints: \n",list(csp.const.keys()))
csp.backtrack()
csp.dispSol()

### negative logic 
print("\n##### NEGATIVE LOGIC #####")
path = "../../Data/lewisCaroll_n.txt" 
csp = CSP(path, 25,'negative')
print("Variables: \n", csp.map)
print("Constraints: \n",list(csp.const.keys()))
csp.backtrack()
csp.dispSol()