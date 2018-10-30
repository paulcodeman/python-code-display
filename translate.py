import sys
import dis
import json
import inspect

name = sys.argv[1]
cmd = sys.argv[2]


def getBytecode(code):
	const = code.co_consts
	array = []
	for v in const:
		if type(v).__name__=='code':
			v = getBytecode(v)
		array.append(v)
		#co_varnames
	return [list(code.co_names),list(array),list(code.co_code),list(code.co_varnames)]

def getJson(code):
	d = dis.Bytecode(code)
	array = []
	oCode = 0
	for v in d:
	
		# omission text string name
		if oCode:
			oCode = 0
			continue
			#----
			
		val = v.argval
		if type(val).__name__=='code':
			val = getJson(val)
			oCode = 1
			
			
		#params = inspect.getargspec(code)
		
		# omission import function
		if v.opname == 'IMPORT_NAME':
			del array[len(array)-1];
			del array[len(array)-1];
			#----
		
		array.append([v.opname,val,v.arg,v.offset,v.argrepr,oCode,list(code.co_varnames),code.co_argcount])
	return array
	
f = open(name,"r")
code = f.read()
o = compile(code,"<string>","exec")

if cmd=='json':
	print(json.dumps(getJson(o)))
	
if cmd=='bytecode':
	print(json.dumps(getBytecode(o)))