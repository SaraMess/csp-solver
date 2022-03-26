
import copy
import sys


class CSP :
    """ Class for CSP modelisation and solving 
    """

    def  __init__(self, path,numV, c_type='positive'):
        """ path: descriptif textual file location \n
            numV: number of variables \n
            c_type: mention "positive" for positive logic, "negative for prohibition constraints
        """
        self.c_type = c_type
        self.numV = numV
        self.varN, self.const, self.domain,self.map = self.data(path)
        self.var = list(self.map.values())
        print('csp init')
        self.sol = []
        self.DC= copy.deepcopy(self.domain)
        self.forwarding = {}
        self.iter = 0

    def data(self,path):
        """ Extracting variables, domains and constraints given file's path
        """
        with open(path) as file :
            var=[];p=0; p_var=0;domain=[0,]*self.numV; contrainte={};mapped={}
            for i in file.readlines() :
                #print('var', var)
                if  i[0] == 'v' :
                    var.append(i[2:].replace('\n',''))
                    mapped[i[2:].replace('\n','')]=p_var 
                    p_var = p_var + 1

                if i[0] == 'd' :

                    domain[p]=i[2:].replace('\n','').split(" ")
                    p=p+1

                if i[0:2] == 'cv' :
                    con=i[3:].replace(':\n','').split()
                    con=tuple([mapped[i] for i in con])

                    contrainte[con]=[]

                if i[0:2] == 'c ':

                    contrainte[con].append(i[2:].replace(':\n','').split())

        return var, contrainte, domain, mapped

    def order(self, info = 'DEFAULT'):
        """ variable scheduling optimisation, the ordering creterion is given in info \n
            'DEFAULT' ordering given numbre of constraints \n
            'domain'  ordering given domain size \n
        """

        if info ==  'DEFAULT':
            sorting=[]
            for i in self.var :
                count = 0
                for k,j in self.const.keys():
                    if k == i or j == i:
                        count = count + 1
                sorting.append((i,count,1)) #changing for the number of tuple
            sorting.sort(key = lambda tup : (tup[1],tup[0]))
            ordered = [i for i,j,k in sorting]
            self.var= copy.copy(ordered)
        if info == 'DOMAIN' :
            sorting=[(i,len(self.domain[i])) for i in self.var]
            sorting.sort(key=lambda x:x[1])
            ordered = [i for (i,j) in sorting]
            self.var = copy.copy(ordered)
        return ordered

    def check(self,p,val):
        """ test constraint satisfaction for the variable p with value val \n
            return true if satisfied
        """
        if self.c_type == 'negative':
            marqued = [ i for i,j in self.sol ]
            values =  [ j for i,j in self.sol ]
            for k,j in enumerate(marqued):
                j1,p1=j,p
                switch = False
                if (j1,p1) in list(self.const.keys()):
                    j1,p1 = p1,j1
                    switch = True
                if (p1,j1) in list(self.const.keys()):
                    test = ([val, values[k]],[values[k],val])[switch]
                    if test  in self.const[(p1,j1)]:
                        return False
            return True
  
        elif self.c_type == 'positive':
            count = 0
            exist = 0
            marqued = [ i for i,j in self.sol ]
            values =  [ j for i,j in self.sol ]
            for k,j in enumerate(marqued):
                j1,p1=j,p
                switch = False
                if (j1,p1) in list(self.const.keys()):
                    j1,p1 = p1,j1
                    switch = True
                if (p1,j1) in list(self.const.keys()): 
                    exist = exist +1
                    test = ([val, values[k]],[values[k],val])[switch] 
                    if test not in self.const[(p1,j1)]:
                        return False
            return True

    def order_val(self):
        """ Domain values scheduling optimisation for variable p
           """
        count=[]
        for p in range(self.numV):
            count=[]
            for l,a in enumerate(self.domain[p]):
                count.append([a,0])
                for i,k in self.const.items():
                    for j in k:
                        if i[1] == p and a == j[1] or i[0] == p and a == j[0]: 
                            count[l][1] =  count[l][1] + 1
            if self.c_type == 'negative':
                count.sort(key=lambda x : x[1],reverse=True)
            else :
                count.sort(key=lambda x : x[1])
            self.domain[p] = [i for i,j in count]

    def forward(self,p,val):
        """ forward checking with variable p having value val
        """
        self.forwarding[p]={}
        if self.c_type ==  'negative':
            marqued  = [i for i,j in self.sol]
            left = list(set(self.var)-set(marqued)-set([p,]))
            for i in left :
                k1,i1 = p,i
                switch = False  
                if (i1,k1) in list(self.const.keys()) :
                    k1,i1 = i,p
                    switch = True
                if (k1,i1) in list(self.const.keys()):
                    self.forwarding[p][i]=[]
                    if not switch :
                        prohib = [v2 for v1,v2 in self.const[(k1,i1)] if v1 == val and v2 in self.DC[i]]
                    else :
                        prohib = [v1 for v1,v2 in self.const[(k1,i1)] if v2 == val and v1 in self.DC[i]]
                    self.DC[i] = list(set(self.DC[i])-set(prohib))
                    self.forwarding[p][i]= copy.deepcopy(prohib)
        if self.c_type ==  'positive':
            marqued  = [i for i,j in self.sol]
            left = list(set(self.var)-set(marqued)-set([p,]))
            for i in left :
                i1=i
                k1=p
                switch = False
                if (i1,k1) in list(self.const.keys()) :
                    k1,i1 = i1,k1
                    switch = True
                self.forwarding[p][i]=[]
                if (k1,i1) in list(self.const.keys()):
                    if not switch :
                        allowed = [v2 for v1,v2 in self.const[(k1,i1)] if v1 == val and v2 in self.DC[i]]
                    else :
                        allowed = [v1 for v1,v2 in self.const[(k1,i1)] if v2 == val and v1 in self.DC[i]]
                    removed = [i for i in self.DC[i] if i not in allowed]
                    self.DC[i]= copy.copy(allowed)
                    self.forwarding[p][i]=removed
                         
    def rev_forward(self, prec ,p):
        """reversing the forward checking induced by the variable p
        """
        if prec in list(self.forwarding.keys()):
            for i,li in self.forwarding[prec].items():
                self.DC[i]=list(set(self.DC[i])|set(li))
            self.forwarding.pop(prec)
 
        self.DC[p] = copy.deepcopy(self.domain[p])
        for j in list(self.forwarding.keys()):
            for i,li in self.forwarding[j].items():
                if i == p :
                    self.DC[p]=list(set(self.DC[i])-set(li))

    def select(self,p):
        """ select a value for the variable p \n
            return true if success
        """
        #print('select',self.DC[p])
        for val in self.DC[p]:
            if self.check(p,val):
                #print('check')
                self.DC[p].remove(val)
                #print(self.DC)
                self.sol.append((p,val))
                #print('actual sol',self.sol)
                self.forward(p,val)
                return True
        return False

    def backtrack(self):
        """ backtrack algorithm for CSP sovlving with chosen scheduling optimisers
        """
        index = 0
        self.order()
        self.order_val()
        self.iter +=1
        while index <  len(self.var) and index>=0:
            p= self.var[index]
            op = self.select(p)
            if op :
                index +=1
                self.iter +=1
            else : 
                #print("backtracking")
                if self.sol:
                    prec,val=self.sol[-1]
                    self.sol.remove(self.sol[-1])
                self.rev_forward(prec,p)
                self.DC[p]=copy.copy(self.domain[p])
                index -= 1
                self.iter +=1
        if index == len(self.var) :
            self.solvable= True
            print("Solvable problem")
            return True #self.sol
        else :
            print('Unsolvable problem regarding constraints')
            self.solvable= False
            return False

    def dispSol(self):
        """ display solution if found after call to the solver
        """
        if self.solvable :
            reverse = {j:i for i,j in list(self.map.items())}
            ordered = sorted(self.sol,key=lambda x: x[0])
            result = [(reverse[i],j) for i,j in ordered]
            for i in result :
                print(i)
            print(f"Solution in {self.iter} iterations")
        else :
            print(f"Unsolvable no solution found. Iterations: {self.iter}")

    def getSol(self):
        return self.sol
