#!/usr/bin/env python
# coding=utf-8
#
from re import search, sub, match
from os.path import join
import s2gd
#
###########################
# LAMBDA FUNCTIONS ########
###########################
# match a certain expression at start of string
match_start  = lambda expr,line: match(r'\s*(%s)[^a-zA-Z0-9]'%expr,line)
# strip unwanted delimiters from string
strip_d      = lambda s,d: sub(d,'',s)
# check if string is closed
s_cld 		 = lambda s: not match(r'[\(\[\{]*\'',s) or match(r'[\(\[\{]*\'(.*)\'',s)
# remove strings, then count delimiters
cnt_d 		 = lambda s,d: sub(r'\'.*\'','',s).count(d)
# add $ to each expression in a list (to match exactly that)
shut_l       = lambda l: [e+r'$' for e in l]
# check is string is in list
rem_esp 	 = lambda l: [sub(' ','',e) for e in l]
# check if pattern is open
check_open   = lambda s,d1,d2: s_cld(s) if d1=='\'' else not bool(cnt_d(s,d1)-cnt_d(s,d2))
# get first argument (cf getfargs)
getarg1      = lambda l: strip_d(get_fargs(l)[0],'\'')
# get next arg
getnextarg   = lambda lst: strip_d(lst.pop(0).lower(),'\'')
getnextargNL = lambda lst: strip_d(lst.pop(0),'\'')
#
###########################
# FUNCTIONS ###############
###########################
#
# +++++++++++++++++++++++++++++++++++++++++
# GET FARGS :
#	get arguments of function str
#
#	<in>:	string like plot(x,y,'+r')
# 	<out>:	list of arguments
def get_fargs(line):
	# get core
 	core = search(r'^\s*(?:\w+)\((.*?)(?:\)\s*;?\s*)((?:%s).*)?$'%s2gd.csd['comment'],line).group(1)
	# split core with commas
	spl  = core.split(',')
	spl  = [v.strip() for v in spl] # remove trailing spaces
	# merge '', (), [], {} that might have been broken (see CLOSE_SPLIT)
	args = spl
	for delim in [['\'','\''],['(',')'],['[',']'],['{','}']]:
		args = close_split(delim[0],delim[1],args)
	return args
# +++++++++++++++++++++++++++++++++++++++++
# CLOSE SPLIT:
# 	close broken patterns after .split(',')
#
#	<in>:	delimiters and list coming from
#			a split along the commas
# 	<out>: 	list of strings reconstructed
#			along broken patterns
def close_split(d1,d2,lst):
	lst2,tmp  = [],''
	for s in lst:
		tmp += s+','
		if check_open(tmp,d1,d2):
			lst2.append(tmp[:-1])
			tmp = ''
	if not lst2:
		lst2 = lst
	elif tmp[:-1]:
		lst2.append(tmp[:-1])
	return lst2
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
#	read a 'plot(...)' line, extracts script
#	code to output data, generates GLE bloc
#	to input in GLE figure
#
#	<in>:	line (from core part of script doc)
#	<out>:	returns line + output line
def read_plot(line, figc, plotc):
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
	# ------------------------------------------
	# SCRIPT -----------------------------------
	# generate script to output appropriate data
	sta = 2; # index of args where options start
	# case one var: plot(x), plot(x,'+r'), ...
	if len(args)==1 or match(r'^\s*\'',args[1]):
		script = 'x__ = %s%s\n'%(s2gd.csd['span']%args[0],s2gd.csd['EOL'])
		script+= 'y__ = %s%s\n'%(args[0],s2gd.csd['EOL'])
		sta    = 1
	# case two vars plot(x,y,'+r')
	else:
		script = 'x__ = %s%s\n'%(args[0],s2gd.csd['EOL'])
		script+= 'y__ = %s%s\n'%(args[1],s2gd.csd['EOL'])
	#
	vecx   = s2gd.csd['vec']%'x__'
	vecy   = s2gd.csd['vec']%'y__'
	script+= 'c__ = %s%s\n'%(s2gd.csd['cbind']%(vecx,vecy),s2gd.csd['EOL'])
	dfn    = ".__datplot%i_%i.dat"%(figc,plotc)
	script+= "%s%s\n"%(s2gd.csd['writevar'].format(dfn,'c__'),s2gd.csd['EOL'])
	#
	plt['script'] = script
	# ---------------------------------
	# GLE -----------------------------
	# generate gle code to read options
	if len(args)>sta:
		optsraw = args[sta:]
		while optsraw:
			opt = getnextarg(optsraw)
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
				tls['color'] = s2gd.md.setdefault(l_4,'blue')
			#
			# COLOR OPTION
			#
			elif opt=='color':
				tls['color'] = getnextarg(optsraw)
				if tls['color'] in ['r','g','b','c','m','y','k','w']:
					tls['color'] = s2gd.md[tls['color']]
			#
			# LWIDTH OPTION
			#
			elif opt=='linewidth' and not flags['lwidth']:
				flags['lwidth']=True
				opt = getnextarg(optsraw)
				lw  = float(opt)
				lw  = round(((lw/3)**.7)/10,2) # magic...
				plt['lwidth'] = ' lwidth '+str(lw)+' '
			#
			# MSIZE OPTION
			#
			elif opt=='markersize' and not flags['msize']:
				flags['msize']=True
				opt = getnextarg(optsraw)
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
#
# +++++++++++++++++++++++++++++++++++++++++++
# READ FILL:
#	read a 'fill(...)' line, extracts script
#	code to output data, generates GLE bloc
#	to input in GLE figure
#
#	<in>:	line (from core part of script doc)
#	<out>:	returns line + output line
def read_fill(line,figc,plotc):
	fill = {}
	# default options
 	fill['color'] = 'gray'
 	fill['alpha'] = False
 	# get plot arguments
 	args = get_fargs(line)
 	# ------------------------------------------
 	# SCRIPT -----------------------------------
 	# generate script to output appropriate data
 	# > syntax:
 	# 	command: fill([x,fliplr(x)],[y,fliplr(y2)],...)
 	#				...,matlabcol|rgb|rgba
 	#				...,'color',svgname,'alpha'?,0.8
 	#
 	xname  = search(r'\[\s*([a-zA-Z][a-zA-Z0-9]*)\s*',args[0]).group(1)
 	yname1 = search(r'\[(.*?),\s*fliplr',args[1]).group(1)
 	yname2 = search(r',\s*fliplr\((.*?)\)\s*\]',args[1]).group(1)
 	a=1 # alpha
 	if len(args)>2:
		optsraw = args[2:]
		while optsraw:
			opt = getnextarg(optsraw)
			if opt in ['r','g','b','c','m','y','k','w']:
				fill['color']=s2gd.md[opt]
			elif opt=='color':
	 			opt  = getnextarg(optsraw) # colname
	 			# option given form [r,g,b,a?]
				rgbsearch  = search(r'\[\s*([0-9]*\.?[0-9]*)\s*,?\s*([0-9]*\.?[0-9]*)\s*,?\s*([0-9]*\.?[0-9]*)(.*)',opt)
				if rgbsearch:
		 			r,g,b=rgbsearch.group(1,2,3)
		 			alphasearch = search(r'\s*([0-9]*\.?[0-9]*)',rgbsearch.group(4))
		 			a = 1 if not alphasearch else alphasearch.group(1)
		 			fill['color']='rgba(%s,%s,%s,%s)'%(r,g,b,a)
	 			elif optsraw and strip_d(optsraw[0].lower(),'\'')=='alpha': # col->rgba
	 				optsraw.pop(0)
	 				opta  = getnextarg(optsraw)
	 				r,g,b = s2gd.srd.setdefault(opt,(128,128,128))
	 				a     = float(opta)*100
	 				fill['color']='rgba255(%i,%i,%i,%f)'%(r,g,b,a)
	 			else: # just colname
	 				fill['color']=opt 	
 	#
 	if not a==1: fill['alpha']=True
 	#
	script = 'x__  = %s%s\n'%(xname ,s2gd.csd['EOL'])
	script+= 'y1__ = %s%s\n'%(yname1,s2gd.csd['EOL'])
	script+= 'y2__ = %s%s\n'%(yname2,s2gd.csd['EOL'])
  	#
  	vecx   = s2gd.csd['vec']%'x__'
  	vecy1  = s2gd.csd['vec']%'y1__'
  	vecy2  = s2gd.csd['vec']%'y2__'
 	script+= 'c__ = %s%s\n'%(s2gd.csd['cbind']%(s2gd.csd['cbind']%(vecx,vecy1),vecy2),s2gd.csd['EOL'])
	dfn    = '.__datfill%i_%i.dat'%(figc,plotc)
  	script+= '%s%s\n'%(s2gd.csd['writevar'].format(dfn,'c__'),s2gd.csd['EOL'])
 	#
 	fill['script'] = script
 	return fill
#
# +++++++++++++++++++++++++++++++++++++++++++
# READ HIST:
#	read a 'hist(...)' line, extracts script
#	code to output data, generates GLE bloc
#	to input in GLE figure
#
#	<in>:	line (from core part of script doc)
#	<out>:	returns line + output line
def read_hist(line,figc,plotc):
	hist = {}
	# default options
 	hist['edgecolor'] = 'white'
 	hist['facecolor'] = 'cornflowerblue'
 	hist['alpha'] 	  = False
 	hist['norm']	  = 'count'
 	hist['from'] 	  = ''
 	hist['to']		  = ''
 	nbins 			  = 0
 	# get plot arguments
 	args = get_fargs(line)
 	# ------------------------------------------
 	# SCRIPT -----------------------------------
 	# generate script to output appropriate data
 	# > syntax:
 	# 	command: hist(x,...)
 	#	 			...,'Normalization','count|countdensity|probability|pdf|cumcount|cdf'
 	#				...,'Facecolor',svgcol|matlabcol|rgb|rgba,'Alpha'?,0.8
 	#				...,'Edgecolor',svgcol|matlabcol|rgb
 	#
 	xname  = strip_d(args.pop(0),'\'')
 	a=1 # alpha
 	if args:
	 	optsraw = args
	 	while optsraw:
	 		opt = getnextarg(optsraw)
	 		if   opt == 'normalization':
	 			normalization = getnextarg(optsraw)
	 			if normalization in ['count','probability','countdensity','pdf']:
	 				hist['norm'] = normalization
	 			elif normalization in ['cumcount','cdf']:
					print '\nwarning::S2G::HIST::cumcount/cdf not handled, going default (count)\n'
	 			else:
					print '\nwarning::S2G::HIST::unknown normalization, going default (count)\n'
			elif opt == 'nbins' or opt.isdigit():
				if opt == 'nbins':
					opt = getnextargNL(optsraw)
				nbins = opt
			elif opt == 'from':
				hist['from'] = getnextargNL(optsraw)
			elif opt == 'to':
				hist['to'] = getnextargNL(optsraw)
	 		elif opt in ['r','g','b','c','m','y','k','w']:
				hist['facecolor']=s2gd.md[opt]
			elif opt in ['color','facecolor']:
	 			opt  = getnextarg(optsraw) # colname
	 			# option given form [r,g,b,a?]
				rgbsearch  = search(r'\[\s*([0-9]*\.?[0-9]*)\s*,?\s*([0-9]*\.?[0-9]*)\s*,?\s*([0-9]*\.?[0-9]*)(.*)',opt)
				if rgbsearch:
		 			r,g,b=rgbsearch.group(1,2,3)
		 			alphasearch = search(r'\s*([0-9]*\.?[0-9]*)',rgbsearch.group(4))
		 			a = 1 if not alphasearch else alphasearch.group(1)
		 			hist['facecolor']='rgba(%s,%s,%s,%s)'%(r,g,b,a)
	 			elif optsraw and strip_d(optsraw[0].lower(),'\'')=='alpha': # col->rgba
	 				optsraw.pop(0)
	 				opta  = getnextarg(optsraw)
	 				r,g,b = s2gd.srd.setdefault(opt,(128,128,128))
	 				a     = float(opta)*100
	 				hist['facecolor']='rgba255(%i,%i,%i,%f)'%(r,g,b,a)
	 			else: # just colname
	 				hist['facecolor']=opt
	 				if hist['facecolor'] in ['r','g','b','c','m','y','k','w']:
						hist['facecolor']=s2gd.md['facecolor']
	 		elif opt=='edgecolor':
	 			opt = getnextarg(optsraw) # colname, no transp
	 			# option given form [r,g,b,a?]
				rgbsearch  = search(r'\[\s*([0-9]*\.?[0-9]*)\s*,?\s*([0-9]*\.?[0-9]*)\s*,?\s*([0-9]*\.?[0-9]*)(.*)',opt)
				if rgbsearch:
		 			r,g,b=rgbsearch.group(1,2,3)
		 			hist['edgecolor']='rgba(%s,%s,%s,%s)'%(r,g,b,a)
	 			else: # just colname
	 				hist['edgecolor']=opt
	 				if hist['edgecolor'] in ['r','g','b','c','m','y','k','w']:
						hist['edgecolor']=s2gd.md[hist['edgecolor']]
	#
 	if not a==1: hist['alpha']=True
 	#
	script = 'x__  = %s%s\n'%(xname ,s2gd.csd['EOL'])
  	#
  	# NEEDS WORKING, NOT JUST VEC IT, IF MULTI COLUMN THEN STACK
  	# 
  	vecx   = s2gd.csd['vec']%'x__'
 	script+= 'c__ = %s%s\n'%(vecx,s2gd.csd['EOL'])
	dfn    = ".__dathist%i_%i.dat"%(figc,plotc)
  	script+= "%s%s\n"%(s2gd.csd['writevar'].format(dfn,'c__'),s2gd.csd['EOL'])
  	if not hist['from']:
  		script+= 'xmin__ = %s%s\n'%(s2gd.csd['minvec']%vecx,s2gd.csd['EOL'])
 	else:
 		script+= 'xmin__ = %s%s\n'%(hist['from'],s2gd.csd['EOL'])
 	if not hist['to']:
 		script+= 'xmax__ = %s%s\n'%(s2gd.csd['maxvec']%vecx,s2gd.csd['EOL'])
	else:
	 	script+= 'xmax__ = %s%s\n'%(hist['to'],s2gd.csd['EOL'])
 	if not nbins:
 		script+='nbins__ = %s%s\n'%(s2gd.csd['autobins'].format(s2gd.csd['lenvec']%vecx),s2gd.csd['EOL'])
 	else:
 		script+='nbins__ = %s%s\n'%(nbins,s2gd.csd['EOL'])
 	script+= 'c2__ = %s%s\n'%(s2gd.csd['rbind']%(s2gd.csd['rbind']%('xmin__','xmax__'),'nbins__'),s2gd.csd['EOL']) 
	dfn2   = ".__dathist%i_%i_side.dat"%(figc,plotc)
  	script+= "%s%s\n"%(s2gd.csd['writevar'].format(dfn2,'c2__'),s2gd.csd['EOL'])
 	#
 	hist['script'] = script
 	return hist
