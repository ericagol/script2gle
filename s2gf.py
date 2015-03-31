#!/usr/bin/env python
# coding=utf-8
#
from re import search, sub, match
from os.path import join
#
###########################
# LAMBDA FUNCTIONS ########
###########################
# match a certain expression at start of string
match_start = lambda expr,line: match(r'\s*('+expr+')',line)
# strip unwanted delimiters from string
strip_d     = lambda s,d: sub(d,'',s)
# check if string is closed
s_cld 		= lambda s: not match(r'[\(\[\{]*\'',s) or match(r'[\(\[\{]*\'(.*)\'',s)
# remove strings, then count delimiters
cnt_d 		= lambda s,d: sub(r'\'.*\'','',s).count(d)
# add $ to each expression in a list (to match exactly that)
shut_l      = lambda l: [e+r'$' for e in l]
# check is string is in list
rem_esp 	= lambda l: [sub(' ','',e) for e in l]
#
###########################
# FUNCTIONS ###############
###########################
# +++++++++++++++++++++++++++++++++++++++++
# CLOSE SPLIT:
# 	close broken patterns after .split(',')
#
#	<in>:	delimiters and list coming from
#			a split along the commas
# 	<out>: 	list of strings reconstructed
#			along broken patterns
def close_split(d1,d2,lst):
	if d1=='\'':
		check = lambda s: s_cld(s)
	else:
		check = lambda s: not bool(cnt_d(s,d1)-cnt_d(s,d2))
	lst2,tmp  = [],''
	for s in lst:
		tmp += s+','
		if check(tmp):
			lst2.append(tmp[:-1])
			tmp = ''
	if not lst2:
		lst2 = lst
	elif tmp[:-1]:
		lst2.append(tmp[:-1])
	return lst2

# +++++++++++++++++++++++++++++++++++++++++
# GET FARGS :
#	get arguments of function str
#
#	<in>:	string like plot(x,y,'+r')
# 	<out>:	list of arguments
def get_fargs(line,remesp=True):
	# get core
	core = search(r'^(\w+)\((.*)(\)\s*;?\s*)$',line).group(2)
	# split core with commas
	spl  = core.split(',')
	# merge '', (), [], {} that might have been broken
	args = spl
	for delim in [['\'','\''],['(',')'],['[',']'],['{','}']]:
		args = close_split(delim[0],delim[1],args)
	if remesp: return rem_esp(args)
	else:      return args
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
		spl = left.split(' ')
		for i in range(0,spl.count('')):
			spl.remove('')
		array = spl
	return rem_esp(array)
# +++++++++++++++++++++++++++++++++++++++++++
# READ PLOT:
#	read a 'plot(...)' line, extracts matlab
#	code to output data, generates GLE bloc
#	to input in GLE figure
#
#	<in>:	line (from core part of matlab doc)
#	<out>:	returns line + output line
def read_plot(line, t_dir, figc, plotc):
	plt,tls  = {},{}
	# default options
	plt['lwidth'] = ' lwidth 0 '
	plt['msize']  = ' msize 0.2 '
	tls['line']   = ''
	tls['marker'] = ''
	tls['color']  = ' darkblue '
	# flags of options done
	flags = {'lstyle':False,'lwidth':False,'msize':False,'mface':False}
	# get plot arguments
	args = get_fargs(line)
	# JULIA ----------------------------
	# generate julia code to output data
	sta = 2;
	# case one var: plot(x), plot(x,'+r'), ...
	if len(args)==1 or match(r'^\s*\'',args[1]):
		mcode = 'x__ = 1:prod(size('+args[0]+'))\n'
		mcode+= 'y__ = '+args[0]+'\n'
		sta   = 1
	# case two vars plot(x,y,'+r')
	else:
		mcode = 'x__ = '+args[0]+'\n'
		mcode+= 'y__ = '+args[1]+'\n'
	#
	mcode+= 'c__ = [x__[:] y__[:]]\n'
	dfn   = t_dir+"datplot"+str(figc)+'_'+str(plotc)+".dat"
	mcode+= "writecsv(\"%s\",c__)\n"%dfn
	#
	plt['mcode'] = mcode
	# GLE -----------------------------
	# generate gle code to read options
	optsraw = args[sta:]
	while optsraw:
		opt = strip_d(optsraw.pop(0).lower(),'\'')
		#
		# LSTYLE
		#
		# patterns of the form '-+r'
		p_lstyle = r'^(?![ml0-9])([-:]?)([-\.]?)([\+o\*\.xs\^]?)([rgbcmykw]?)'
		lstyle = match(p_lstyle,opt)
		if lstyle and not flags['lstyle']:
			flags['lstyle']=True
			#
			# line (continuous, dashed, ...)
			l_1 = lstyle.group(1)
			l_2 = lstyle.group(2)
			if   match(r':', l_1): 	tls['line'] = '2' 	# dotted
			elif match(r'-', l_1) and \
				 match(r'\.',l_2): 	tls['line'] = '6'	# dashed-dotted
			elif match(r'-', l_1) and \
				 match(r'-', l_2): 	tls['line'] = '3'	# dashed
			elif match(r'-', l_1):	tls['line'] = '0'	# standard
			#
			# marker
			l_3 = lstyle.group(3)
			if   match(r'\+',l_3): 	tls['marker'] = 'plus'
			elif match(r'o', l_3):	tls['marker'] = 'circle'
			elif match(r'\*',l_3): 	tls['marker'] = 'star'
			elif match(r'x', l_3):	tls['marker'] = 'cross'
			elif match(r's', l_3):	tls['marker'] = 'square'
			elif match(r'\^',l_3):	tls['marker'] = 'triangle'
			#
			# color
			l_4 = lstyle.group(4)
			if   match(r'r',l_4): 	tls['color'] = 'darkred'
			elif match(r'g',l_4): 	tls['color'] = 'darkgreen'
			elif match(r'b',l_4):	tls['color'] = 'darkblue'
			elif match(r'c',l_4):	tls['color'] = 'darkcyan'
			elif match(r'm',l_4): 	tls['color'] = 'darkmagenta'
			elif match(r'y',l_4): 	tls['color'] = 'goldenrod'
			elif match(r'k',l_4):	tls['color'] = 'black'
			elif match(r'w',l_4):	tls['color'] = 'white'
		#
		# COLOR OPTION
		#
		elif opt=='color':
			tls['color'] = strip_d(optsraw.pop(0),'\'')
		#
		# LWIDTH OPTION
		#
		elif opt=='linewidth' and not flags['lwidth']:
			flags['lwidth']=True
			opt = strip_d(optsraw.pop(0).lower(),'\'')
			lw  = float(opt)
			lw  = round(((lw/3)**.7)/10,2)
			plt['lwidth'] = ' lwidth '+str(lw)+' '
		#
		# MSIZE OPTION
		#
		elif opt=='markersize' and not flags['msize']:
			flags['msize']=True
			opt = strip_d(optsraw.pop(0).lower(),'\'')
			ms  = float(opt)
			ms  = round(((ms/5)**.5)/5,2)
			plt['msize'] = ' msize '+str(ms)+' '
		#
		# MFACE OPTION
		#
		elif opt=='markerfacecolor' and not flags['mface']:
			flags['mface']=True
			optsraw.pop(0) # actually we don't care what color is given

	# if just marker no line, if no marker no line -> lstyle 0
	lb,mb  = bool(tls['line']),bool(tls['marker'])
	lbool  = lb or not mb
	lsty   = tls['line']+'0'*(not lb)
	line   = ('lstyle '+lsty)*lbool
	fill   = 'f'*(tls['marker'] in ['circle','square','triangle'])*flags['mface']
	marker = 'marker '*mb+fill+tls['marker']
	color  = 'color '+tls['color']
	plt['lstyle'] = ' '+line+' '+marker+' '+color+' '
	return plt
