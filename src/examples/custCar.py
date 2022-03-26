import sys
sys.path.insert(1, '../')
from csp import CSP 

########################## TEST PROGRAM FOR CAR CUSTOMIZATION PROBLEM ##############################

path = "../../Data/custCar_n.txt" 
csp = CSP(path, 3,'negative')
print("Variables: \n", csp.map)
print("Constraints: \n",list(csp.const.keys()))
csp.backtrack()
csp.dispSol()