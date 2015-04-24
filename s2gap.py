from s2gc import *
from re import search, sub, match

import s2gf
from s2ge import *

#
# SUPPORT FUNCTIONS
#
addscrvar   = lambda name,expr: '%s=%s%s\n'%(name,expr,s2gd.csd['EOL'])
addscrwrite = lambda vn,dfn:    '%s%s\n'%(s2gd.csd['writevar'].format(dfn,vn),s2gd.csd['EOL']) 
checkfig  	= lambda cf: 		 cf.fignum+1*(cf.cntr>0)
checkplot   = lambda cf: 		 1 if (cf.flags['holdon'] or not cf.cntr) else 0
printdict   = lambda d: 		 ''.join([' %s %s'%v if v[1] else '' for v in d.items()])+'\n'
#
# PARSE FUNCTIONS
#
# >> return syntax is: return NEWFIG, NEWLINE
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
	if curfig.cntr:
		xargs['figlist'].append(curfig)
	#
	# return a new S2G figure + rest of line
	return S2GFIG(fn,xargs['no_tex']),sub(regex,'',line)
# -----------------------------------------------------------------------------
def parse_hold(curfig,line,**xargs):
	regex = r'hold\s*(off|on)?\s*?;?'
	#
 	srch  = search(regex,line)
 	#
	curfig.flags['holdon'] = not(srch.group(1)=='off')
	#
	# no new fig, rest of line
	return 0,sub(regex,'',line)
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
	line += '' if len(args)<3 else ','+','.join(args[2:])
	line += ')\n'
	#
	# feed to fillbetween parser
	return parse_fillbetween(curfig,line,script=xargs['script'])
# -----------------------------------------------------------------------------
def parse_fillbetween(curfig,line,**xargs):
	# increment plot counter if figure held or if was 0
	curfig.cntr += checkplot(curfig)
	#
	# syntax: fillbetween(x,y1,y2,...)
	args 	= s2gf.get_fargs(line)
	x,y1,y2 = args[0:3]
	optsraw = '' if len(args)<4 else args[3:]
	# treat options
	# > default dictionaries
	opt_style = { 
		'color'	: 'gray',	# default fill color
	}
	opt_comp = {
		'alpha'	: False,	# default transparency
	}
	while optsraw:
		opt = s2gf.getnextarg(optsraw)
		# color / style
		if opt in ['r','g','b','c','m','y','k','w']:
			opt_style['color'] = s2gd.md[opt]
		elif opt == 'color':
			opt_style['color'],alpha,optsraw     = s2gf.get_color(optsraw)
			opt_comp['alpha'] = opt_comp['alpha'] or alpha
		else:
			raise S2GSyntaxError(line,'<::unknown option in fill::>')
	#
	# name of data file
	dfn 	= '%sdatfill%i_%i.dat'%(s2gd.tind,curfig.fignum,curfig.cntr)
	#
	# <ADD TO SCRIPT FILE>
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
	# <ADD TO GLE FILE>
	curfig.plot += 'data "%s" d%i d%i\n'%(dfn,curfig.cntr,curfig.cntr+1)
	curfig.plot += 'fill d%i,d%i'%(curfig.cntr,curfig.cntr+1)
	# > write style options
	curfig.plot += ''.join([' %s %s'%v for v in opt_style.items()])+'\n'
	# > flags
	curfig.trsp = curfig.trsp or opt_comp['alpha']
	#
	# no newfig, no rest of line
	return 0,''
# -----------------------------------------------------------------------------
def parse_histogram(curfig,line,**xargs):
	# increment plot counter if figure held or if was 0
	curfig.cntr += checkplot(curfig)
	#
	# syntax: hist(x,...)
	args    = s2gf.get_fargs(line)
	x       = args[0]
	optsraw = '' if len(args)<2 else args[1:]
	# treat options
	# > default dictionaries
	opt_style = { 
		'color'	: 'white',		# default edge color
		'fill'	: 'salmon', 	# default face color
	}
	opt_comp = {
		'alpha'	: False, 		# default transparency
		'norm'	: 'count',		# default normalization
		'from'	: '',
		'to'	: '',
	}
	nbins = 0
	while optsraw:
		opt = s2gf.getnextarg(optsraw)
		# color / style
		if opt in ['r','g','b','c','m','y','k','w']:
			opt_style['color'] = s2gd.md[opt]
		elif opt in ['color','facecolor']:
			opt_style['fill'],alpha,optsraw = s2gf.get_color(optsraw)
			opt_comp['alpha'] = opt_comp['alpha'] or alpha
		elif opt == 'edgecolor':
			opt_style['color'],alpha,optsraw = s2gf.get_color(optsraw)
			opt_comp['alpha'] = opt_comp['alpha'] or alpha
		# computations
		elif opt in ['norm','normalization']:
			normalization = s2gf.getnextarg(optsraw)
			if normalization in ['count','probability','countdensity','pdf']:
 				opt_comp['norm'] = normalization
 			elif normalization in ['cumcount','cdf']:
				print '\nwarning::S2G::HIST::cumcount/cdf not handled, going default (count)\n'
 			else:
				print '\nwarning::S2G::HIST::unknown normalization, going default (count)\n'
		elif opt == 'from':
			xmin = s2gf.getnextargNL(optsraw)
		elif opt == 'to':
			xmax = s2gf.getnextargNL(optsraw)
		elif opt.isdigit():
			nbins = opt
		elif opt == 'nbins':
			nbins = s2gf.getnextargNL(nbins)
		else:
			raise S2GSyntaxError(line,'<::unknown option in hist::>')			
	#
	# name of data files
	dfn     = '%sdathist%i_%i.dat'%(s2gd.tind,curfig.fignum,curfig.cntr)
	dfn_sup = sub('hist','hist_sup',dfn)
	#
	# <ADD TO SCRIPT FILE>
	script  = ''
	script += addscrvar('x__',x)
	# > col vector
	script += addscrvar('xv__',s2gd.csd['vec']%'x__')
	# > write var
	script += addscrwrite('xv__',dfn)
	# > Range
	if opt_comp['from']: script += addscrvar('xmin__',opt_comp['from'])
	else:			 	 script += addscrvar('xmin__',s2gd.csd['minvec']%'xv__')
	if opt_comp['to']:	 script += addscrvar('xmax__',opt_comp['to'])
	else:			 	 script += addscrvar('xmax__',s2gd.csd['maxvec']%'xv__')
	# > Nbins
	if nbins:	 	 	 script += addscrvar('nbins__',nbins)
	else:			 	 script += addscrvar('nbins__',s2gd.csd['autobins'].format(s2gd.csd['lenvec']%'xv__'))
	# > write support information (MATCH ORDER WITH LINES BELOW)
	script += addscrvar('c2__',s2gd.csd['rbind2'](
					[
						'xmin__', # 1
						'xmax__', # 2
						'nbins__' # 3
					]))
	script += addscrwrite('c2__',dfn_sup)
	# > write script
	xargs['script'].write(script)
	#
	# <ADD TO GLE FILE>
	# -- reading support file
	curfig.plot += 'data "%s" d%i\n'%(dfn_sup,curfig.cntr)
	curfig.plot += 'xmin_  = datayvalue(d%i,1)\n'%curfig.cntr # 1
	curfig.plot += 'xmax_  = datayvalue(d%i,2)\n'%curfig.cntr # 2
	curfig.plot += 'nbins_ = datayvalue(d%i,3)\n'%curfig.cntr # 3
	# -- reading actual data
	curfig.cntr += 1
	curfig.plot += 'data "%s" d%i\n'%(dfn,curfig.cntr)
	# -- -- computing normalization
	curfig.plot += 'N_ = ndata(d%i)\n'%curfig.cntr
	curfig.plot += 'width_ = (xmax_-xmin_)/nbins_\n'
	norm = '1.0'
	if 	 opt_comp['norm'] == 'probability':  norm = '1.0/N_'
	elif opt_comp['norm'] == 'countdensity': norm = '1.0/width_'
	elif opt_comp['norm'] == 'pdf': 		 norm = '1.0/(N_*width_)'
	# -- doing the hist
	curfig.plot += 'let d{0} = hist d{1} from xmin_ to xmax_ bins nbins_\n'.format(curfig.cntr+1,curfig.cntr)
	curfig.cntr += 1
	curfig.plot += 'let d{0} = d{0}*{1}\n'.format(curfig.cntr,norm)
	curfig.plot += 'bar d%i width width_'%curfig.cntr
	# > write style options
	curfig.plot += printdict(opt_style)
	# > flags
	curfig.trsp = curfig.trsp or opt_comp['alpha']
	#
	# no newfig, no rest of line
	return 0,''
# -----------------------------------------------------------------------------
def parse_stem(curfig,line,**xargs):
	return parse_plot(curfig,line,stem=True,**xargs)
# -----------------------------------------------------------------------------
def parse_semilogx(curfig,line,**xargs):
	curfig.axopt += 'xaxis log\n'
	return parse_plot(curfig,line,**xargs)
# -----------------------------------------------------------------------------
def parse_semilogy(curfig,line,**xargs):
	curfig.axopt += 'yaxis log\n'
	return parse_plot(curfig,line,**xargs)
# -----------------------------------------------------------------------------
def parse_loglog(curfig,line,**xargs):
	curfig.axopt += 'xaxis log\nyaxis log\n'
	return parse_plot(curfig,line,**xargs)
# -----------------------------------------------------------------------------
def parse_plot(curfig,line,**xargs):
	# increment plot counter if figure held or if was 0
	curfig.cntr += checkplot(curfig)
	#
	# syntax: plot(x,  ...)
	# 		  plot(x,y,...)
	args = s2gf.get_fargs(line)
	x    = args[0]
	idx  = 1
	if len(args)>1: 
		# plot(x,...)
		if args[1].strip()[0] == "'": 
			# plot(x, '...')
			y,optsraw = '', args[1:]
		else: 
			# plot(x,y,...)
			y,optsraw = args[1], '' if len(args)<3 else args[2:]
	else: 
		# plot(x)
		y,optsraw = '', ''
	#
	# treat options
	# > default dictionaries
	opt_style = {
		'color'	 : 'darkblue',
		'lstyle' : '0',
		'lwidth' : '0',
		'marker' : '',
		'msize'	 : '0.2',
	}
	opt_comp = {
	}
	while optsraw:
		opt = s2gf.getnextarg(optsraw)
		#
		# QUICK SYNTAX (eg '-ro')
		re_lstyle = r'^(?![ml0-9])([-:]?)([-\.]?)([\+o\*\.xs\^]?)([rgbcmykw]?)'
		ma_lstyle = match(re_lstyle,opt)
		if ma_lstyle:
			l_1,l_2,l_3,l_4 = ma_lstyle.group(1,2,3,4)
			# line (continuous, dashed, ...)
			if   match(r':', l_1):
				opt_style['lstyle'] = '2' 	# dotted
			elif match(r'-', l_1) and match(r'\.',l_2):
			 	opt_style['lstyle'] = '6'	# dashed-dotted
			elif match(r'-', l_1) and match(r'-', l_2):
			 	opt_style['lstyle'] = '3'	# dashed
			elif match(r'-', l_1):
				opt_style['lstyle'] = '0'	# standard
			# marker
			if   match(r'\+',l_3): 	
				opt_style['marker'] = 'plus'
			elif match(r'o', l_3):	
				opt_style['marker'] = 'circle'
			elif match(r'\*',l_3): 	
				opt_style['marker'] = 'star'
			elif match(r'x', l_3):	
				opt_style['marker'] = 'cross'
			elif match(r's', l_3):	
				opt_style['marker'] = 'square'
			elif match(r'\^',l_3):	
				opt_style['marker'] = 'triangle'
			# color
			opt_style['color'] = s2gd.md.get(l_4,'darkblue')
		#
		elif opt == 'color':
			opt_style['color'],foo,optsraw = s2gf.get_color(optsraw)
		elif opt in ['linewidth','lwidth']:
			opt = s2gf.getnextarg(optsraw)
			# black magic...
			opt_style['lwidth'] = str(round(((float(opt)/3)**.7)/10,2))
		elif opt in ['markersize','msize']:
			opt = s2gf.getnextarg(optsraw)
			# black magic...
			opt_style['msize'] = str(round(((float(opt)/5)**.5)/5,2))
		elif opt in ['markerfacecolor','mfcol']:
			cm  = opt_style['marker']
			cm2 = 'f' if cm in ['circle','triangle','square'] else ''  
			opt_style['marker'] = cm2+cm
		else:
			raise S2GSyntaxError(line,'<::unknown option in plot::>')			
	#
	# name of data file
	dfn = '%sdatplot%i_%i.dat'%(s2gd.tind,curfig.fignum,curfig.cntr)
	#
	# <ADD TO SCRIPT FILE>
	script = ''
	if y:
		script += addscrvar('x__',x)
		script += addscrvar('y__',y)
	else:
		script += addscrvar('y__',x)
		script += addscrvar('x__',s2gd.csd['span']%s2gd.csd['numel']%'y__')	
	vx,vy   = s2gd.csd['vec']%'x__', s2gd.csd['vec']%'y__'
	script += addscrvar('c__',s2gd.csd['cbind']%(vx,vy))
	script += addscrwrite('c__',dfn)
	# > write script
	xargs['script'].write(script)
	#
	# <ADD TO GLE FILE>
	# -- reading data
	curfig.plot += 'data "%s" d%i\n'%(dfn,curfig.cntr)
	# -- doing the plot
	stem = 'impulses' if xargs.get('stem',False) else ''
	curfig.plot += 'd%i line %s'%(curfig.cntr,stem)
	curfig.plot += printdict(opt_style)
	#
	# no newfig, no rest of line
	return 0,''
