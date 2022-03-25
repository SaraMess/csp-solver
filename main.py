from csp import CSP


########################## TEST PROGRAM FOR THE LEWIS & CAROLL PROBLEM ##############################
###### try with the provided CSP discription files or test on your own examples


path = "Data/lewisCaroll.txt" 
csp = CSP(path, 25,'negative') #'positive'
print("Variables: \n", csp.map)
print("Constraints: \n",list(csp.const.keys()))
# print("Variables", csp.var)
# print('###Constraints are: \n',csp.const) 
# print('###Numerical variable are: \n',csp.varN) 
# print('###Variables domain: \n',csp.domain) 
#csp.backtrack()
#print('nrov', csp.DC[3],csp.domain[3])
csp.backtrack()
print(csp.getSol())