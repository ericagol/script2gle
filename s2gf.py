from re import search, sub, match
from os.path import join
#
import s2gc
import s2gd
#
###########################
# LAMBDA FUNCTIONS ########
###########################
# match a certain expression at start of string
match_start  = lambda expr,line: match(r'\s*(%s)[^a-zA-Z0-9]'%expr,line)
# ----------
# RECONSIDER
# ----------
# strip unwanted delimiters from string
strip_d      = lambda s,d: sub(d,'',s)
# get first argument (cf getfargs)
getarg1      = lambda l: strip_d(get_fargs(l)[0],'\'')
# get next arg
getnextarg   = lambda lst: lst.pop(0).lower().strip('\'')
getnextargNL = lambda lst: lst.pop(0).strip('\'')
#
###########################
# FUNCTIONS ###############
###########################
#
# # +++++++++++++++++++++++++++++++++++++++++
# # GET FARGS :
# #	get arguments of function str
# #
# #	<in>:	string like plot(x,y,'linewidth',2.0)
# # 	<out>:	list of arguments ['x','y','linewidth','2.0']
def get_fargs(l):
	cur_stack,arg_list,cur_arg = search(r'^\s*(?:\w+)\(\s*(.*)',l).group(1),[],''
	#
	while cur_stack:
		cur_char = cur_stack[0]
		#
		is_open  = cur_char in s2gd.keyopen
		if is_open:
			cur_arg 	    += cur_char
			closed_s,rest,f  = find_delim(cur_stack[1:],cur_char,s2gd.keyclose[cur_char])
			if f: raise s2gc.S2GSyntaxError(l,'<::found %s but could not close it::>'%cur_char)
			cur_arg	        += closed_s+s2gd.keyclose[cur_char]
			cur_stack 	     = rest
			continue
		#
		# out of isopen
		if cur_char == ',': # splitting comma
			arg_list.append(cur_arg)
			cur_arg   = ''
			cur_stack = cur_stack[1:]
			if not cur_stack:
				raise s2gc.S2GSyntaxError(l,'<::misplaced comma::>')
		elif cur_char == ')':
			break
		else:
			cur_arg   += cur_char
			cur_stack  = cur_stack[1:] # can throw syntax error (no end parens)
	#
	return arg_list
#
# Side function
def find_delim(s,d_open,d_close):
	cur_idx 	= 0
	inside_open = 1
	cur_string  = ''
	while cur_idx < len(s):
		cur_char = s[cur_idx]
		#
		cur_idx += 1
		#
		if 		 cur_char == d_close: inside_open -= 1
		elif 	 cur_char == d_open:  inside_open += 1
		#
		if not inside_open: break
		else:
			cur_string += cur_char
	#
	return cur_string,'' if cur_idx==len(s) else s[cur_idx:],inside_open
#
# +++++++++++++++++++++++++++++++++++++++++++
# SAFE_POP
#	tries to pop list, if error, return clarifying
# 	message
def safe_pop(lst,lbl=''):
	try:
		return lst.pop(0)
	except IndexError,e:
		raise s2gc.S2GSyntaxError(line,'<::found %s but no value(s)?::>'%lbl)
#
# +++++++++++++++++++++++++++++++++++++++++++
# ARRAY X
# 	extract numbers in array string '[a b c]'
#
#	<in>: 	string like '[2.0 -2,3]'
#	<out>:	numbers ['2.0','-2','3']
#	<rmk>:	does not interpret expressions
def array_x(s):
	array = []
	# strip ends (-[-stuff-]- extract stuff)
	core = match(r'(\s*\[?)([^\[^\]]+)(\]?\s*)',s).group(2)
	# replace ',' by space
	left = sub(',',' ',core)
	# ATTEMPT - if sequence
	nc = left.count(':')
	if nc==1: # 1:5
		spl        = match(r'(^[^:]+):([^:]+$)',left);
		first,last = float(spl.group(1)), float(spl.group(2))
		seq,cur    = [str(first)], first
		while cur<=last-1:
			cur+=1
			seq.append(str(cur))
		array = seq
	elif nc==2:
		spl             = match(r'(^[^:]+):([^:]+):([^:]+$)',left)
		first,step,last = float(spl.group(1)), float(spl.group(2)), float(spl.group(3))
		seq,cur         = [str(first)],first
		while cur<=last-step:
			cur+=step
			seq.append(str(cur))
		array = seq
	else:
		array = left.split(' ')
	return [sub(' ','',e) for e in array]
#
# +++++++++++++++++++++++++++++++++++++++++++
# GET COLOR:
# 	(internal) read a 'color' option and
#	return something in GLE format
def get_color(optstack):
	#!<DEV:EXPR>
	opt   = getnextarg(optstack)
	color = ''
	a     = 0
	# option given form [r,g,b,a?]
	rgbsearch  = search(r'\[\s*([0-9]+\.?[0-9]*|\.[0-9]*)\s*[,\s]\s*([0-9]+\.?[0-9]*|\.[0-9]*)\s*[,\s]\s*([0-9]+\.?[0-9]*|\.[0-9]*)(.*)',opt)
	if rgbsearch:
		r,g,b  		= rgbsearch.group(1,2,3)
		alphasearch = search(r'([0-9]+\.?[0-9]*|\.[0-9]*)',rgbsearch.group(4))
		a = '1' if not alphasearch else alphasearch.group(1)
		color = 'rgba(%s,%s,%s,%s)'%(r,g,b,a)
	# option is x11 name + 'alpha'
	elif optstack and optstack[0].lower().strip('\'')=='alpha':
		optstack.pop(0)
		opta  = getnextarg(optstack)
		# col -> rgba (using svg2rgb dictionary see s2gd.srd)
		r,g,b = s2gd.srd.get(opt,(128,128,128))
		a     = round(float(opta)*100)
		color = 'rgba255(%i,%i,%i,%2.1f)'%(r,g,b,a)
	else: # just colname
		color = opt
		# if in matlab format (otherwise x11 name)
		if color in ['r','g','b','c','m','y','k','w']:
			color = s2gd.md[color]
	trsp = False if a==0 or a=='1' else True
	return color,trsp,optstack
#
# +++++++++++++++++++++++++++++++++++++++++++
def close_ellipsis(l,script_stack):
	# gather lines in case continuation (...)
	regex   = r'(.*?)(?:\.\.\.\s*(?:%s.*)?$)'%s2gd.csd['comment']
	srch_cl = search(regex,l)
	if srch_cl:
		line_open = True
		nloops = 0
		l = srch_cl.group(1)
		while line_open and nloops<100:
			nloops += 1
			lt      = script_stack.pop(0)
			srch_cl = search(regex,lt)
			if srch_cl:
				l  += srch_cl.group(1)
			else:
				line_open = False
				l+=lt
		if line_open:
			raise s2gc.S2GSyntaxError(l,'<::line not closed::>')
	return l, script_stack
