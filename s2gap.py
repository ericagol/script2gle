from s2gc import *
from re import search, sub

import s2gf

addscrvar   = lambda name,expr: '%s=%s%s\n'%(name,expr,s2gd.csd['EOL'])
addscrwrite = lambda vn,dfn:    '%s%s\n'%(s2gd.csd['writevar'].format(dfn,vn),s2gd.csd['EOL']) 
checkfig  	= lambda cf: 		 cf.fignum+1*(cf.plotcntr>0)
checkplot   = lambda cf: 		 1 if (cf.flags['holdon'] or not cf.plotcntr) else 0

# PARSE FUNCTIONS
# return syntax is: 
#
#	return NEWFIG, NEWLINE
#
# where 
#	 > NEWFIG is 0 if no new fig needs to be created, 
#			  a new S2GFIG otherwise,
#	 > NEWLINE is the rest of the line to be treated,
#			  (usually just an empty string)	

# -----------------------------------------------------------------------------
def parse_figure(curfig,line,**xargs):
	# increment fig counter if needed
	fn = checkfig(curfig)
	# 
	regex = r'\s*figure\s*?;?'
	#
	if curfig.plotcntr:
		xargs['figlist'].append(curfig)
	#
	# return a new S2G figure
	return S2GFIG(fn,xargs['no_tex']),sub(regex,'',line)
# -----------------------------------------------------------------------------
def parse_fill(curfig,line,**xargs):
	#
	args = s2gf.get_fargs(line)
	#
	x  = search(r'\[\s*([a-zA-Z][a-zA-Z0-9]*)\s*',args[0]).group(1)
	y1 = search(r'\[(.*?)[,\s]\s*fliplr',args[1]).group(1)
	y2 = search(r'fliplr\((.*?)\)\s*\]', args[1]).group(1)
	#
	# convert to "fillbetween" syntax
	line  = 'fillbetween(%s,%s,%s'%(x,y1,y2)
	line += '' if len(args)<3 else ','.join(args[2:])
	line += ')\n'
	#
	# feed to fillbetween parser
	return parse_fillbetween(curfig,line,script=xargs['script'])
# -----------------------------------------------------------------------------
def parse_fillbetween(curfig,line,**xargs):
	# increment plot counter if figure held or if was 0
	curfig.plotcntr += checkplot(curfig)
	#
	fill = {
			'expr'		: [],
			'color'		: 'gray',
			'alpha'		: False,
	}
	# syntax: fillbetween(x,y1,y2,...)
	args 	= s2gf.get_fargs(line)
	x,y1,y2 = args[0:3]
	optsraw = '' if len(args)<4 else args[3:]
	# name of data file
	dfn 	= '%sdatfill%i_%i.dat'%(s2gd.tind,curfig.fignum,curfig.plotcntr)
	# preparation of script to output relevant data
	script  = ''
	script += addscrvar('x__', x)
	script += addscrvar('y1__',y1)
	script += addscrvar('y2__',y2)
	# > col vectors
	vx,vy1,vy2 = [s2gd.csd['vec']%e for e in ['x__','y1__','y2__']]
	# > cbind col vectors
	script += addscrvar('c__', s2gd.csd['cbind2']([vx, vy1, vy2]))
	# > write vars
	script += addscrwrite('c__',dfn)
	# > write script
	xargs['script'].write(script)
	# 
	# options treatment
	#
	# SHOULD BE MORE SYSTEMATIC READING OF OPTIONS
	a='1'
	while optsraw:
		opt =  getnextarg(optsraw)
		if opt in ['r','g','b','c','m','y','k','w']:
			fill['color']=s2gd.md[opt]
		elif opt=='color':
			fill['color'],a,optsraw = s2gf.get_color(optsraw)
	if not a=='1': curfig.trsp = True 
	#
	return 0,''



	# fill['expr'].append('x__',  search(r'\[\s*([a-zA-Z][a-zA-Z0-9]*)\s*',args[0]).group(1), 'vec')
	# fill['expr'].append('y1__', search(r'\[(.*?)[,\s]\s*fliplr',args[1]).group(1), 			'vec')
	# fill['expr'].append('y2__', search(r'fliplr\((.*?)\)\s*\]', args[1]).group(1), 			'vec')
	#
#	xargs['script'].write(script_translator(fill))

				# elif marker in ['fill','fillbetween']:
				# 	if marker == 'fillbetween':
				# 		fbargs = s2gf.get_fargs(l)
		 	# 			l      = 'fill([%s,foo],[%s,fliplr(%s)],%s)'%(fbargs[0],fbargs[1],fbargs[2],s2gf.strip_d(str(fbargs[3:]),r'^\[|\]$'))
		 	# 			l      = sub('"','',l)
		 	# 		#
				# 	fill = s2gf.read_fill(l,curfig.fignum,curfig.plotcntr)
				# 	# -> write to temp script file
				# 	sf_tmp.write(fill['script'])
				# 	# -> write to temp gle file
				# 	block    = 'data "%sdatfill%i_%i.dat" d%i d%i\n'%(s2gd.tind,curfig.fignum,curfig.plotcntr,curfig.plotcntr,curfig.plotcntr+1)
				# 	block   += 'fill d%i,d%i color %s'%(curfig.plotcntr,curfig.plotcntr+1,fill['color'])
				# 	curfig.plot+=block
				# 	curfig.trsp = curfig.trsp or fill['alpha']	
	# 	fill = {}
	# # default options
 # 	fill['color'] = 'gray'
 # 	fill['alpha'] = False
 # 	# get plot arguments
 # 	args = get_fargs(line)
 # 	# ------------------------------------------
 # 	# SCRIPT -----------------------------------
 # 	# generate script to output appropriate data
 # 	# > syntax:
 # 	# 	command: fill([x,fliplr(x)],[y,fliplr(y2)],...)
 # 	#				...,matlabcol|rgb|rgba
 # 	#				...,'color',svgname,'alpha'?,0.8
 # 	#
 # 	xname  = search(r'\[\s*([a-zA-Z][a-zA-Z0-9]*)\s*',args[0]).group(1)
 # 	yname1 = search(r'\[(.*?),\s*fliplr',args[1]).group(1)
 # 	yname2 = search(r',\s*fliplr\((.*?)\)\s*\]',args[1]).group(1)
 # 	a='1' # alpha
 # 	if len(args)>2:
	# 	optsraw = args[2:]
	# 	while optsraw:
	# 		opt = getnextarg(optsraw)
	# 		if opt in ['r','g','b','c','m','y','k','w']:
	# 			fill['color']=s2gd.md[opt]
	# 		elif opt=='color':
	# 			fill['color'],a,optsraw = get_color(optsraw) 	
 # 	#
 # 	if not a=='1': fill['alpha']=True
 # 	#
	# script = 'x__  = %s%s\n'%(xname ,s2gd.csd['EOL'])
	# script+= 'y1__ = %s%s\n'%(yname1,s2gd.csd['EOL'])
	# script+= 'y2__ = %s%s\n'%(yname2,s2gd.csd['EOL'])
 #  	#
 #  	vecx   = s2gd.csd['vec']%'x__'
 #  	vecy1  = s2gd.csd['vec']%'y1__'
 #  	vecy2  = s2gd.csd['vec']%'y2__'
 # 	script+= 'c__ = %s%s\n'%(s2gd.csd['cbind']%(s2gd.csd['cbind']%(vecx,vecy1),vecy2),s2gd.csd['EOL'])
	# dfn    = '%sdatfill%i_%i.dat'%(s2gd.tind,figc,plotc)
 #  	script+= '%s%s\n'%(s2gd.csd['writevar'].format(dfn,'c__'),s2gd.csd['EOL'])
 # 	#
 # 	fill['script'] = script
 # 	return fill

def parse_hold(curfig,line,**xargs):
	regex = r'hold\s*(off|on)?\s*?;?'
	#
 	srch  = search(regex,line)
 	#
	curfig.flags['holdon'] = not(srch.group(1)=='off')
	#
	return 0,sub(regex,'',line)

