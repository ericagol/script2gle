import ast

with open('rwdict.dat','r') as f:
	stack = f.readlines()
	dic = ast.literal_eval(''.join(stack))

print dic['nbins']==100
print round(dic['xmin'])==0.0
print round(dic['xmax'])==1.0