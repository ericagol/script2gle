from re import search, sub, match
from math import floor
#
import s2gc
import s2gf
import s2gd
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
# >> return syntax is: return NEWFIG, NEWLINE, SCRIPT STACK
# where
#	 > NEWFIG is a new S2GFIG if needed, 0 otherwise,
#	 > NEWLINE is the rest of line, '' if ignored,
#	 > SCRIPTSTACK is the new rest of stack (cf append), '' def.
# -----------------------------------------------------------------------------
def parse_append(curfig,line,**xargs):
	scriptname = s2gf.strip_d(s2gf.getarg1(line),'\"')
	print 'Appending script <', scriptname, '>...'
	with open(scriptname,'r') as script:
		# prepend the script to stack of lines
		script_stack = script.readlines()+xargs['scriptstack']
	#print xargs['scriptstack']
	#
	# no new fig, no rest of line, no new stack
	return 0,'',script_stack
# -----------------------------------------------------------------------------
def parse_hold(curfig,line,**xargs):
	regex = r'hold\s*(off|on)?\s*?;?'
	#
 	srch  = search(regex,line)
 	#
	curfig.flags['holdon'] = not(srch.group(1)=='off')
	#
	# no new fig, rest of line
	return 0,sub(regex,'',line),''
# -----------------------------------------------------------------------------
def parse_label(curfig,line,**xargs):
	#
	args = s2gf.get_fargs(line)
	al   = args.pop(0).strip('\'')
	m0   = xargs['_labmarker']
	if xargs['no_tex']:
		curfig.axopt += '%stitle "%s"\n'%(m0,sub(r'\\','/',al))
	else:
		curfig.axopt += '%stitle "\\tex{%s}"\n'%(m0,sub('%','\%',al))
	while args:
		arg = s2gf.getnextarg(args)
		if match(r'fontsize$',arg):
			fsize = s2gf.safe_pop(args,arg)
	#
	# no new fig, no rest of line, no new stack
	return 0,'',''
# -----------------------------------------------------------------------------
def parse_xlabel(curfig,line,**xargs):
	return parse_label(curfig,line,_labmarker='x',**xargs)
# -----------------------------------------------------------------------------
def parse_ylabel(curfig,line,**xargs):
	return parse_label(curfig,line,_labmarker='y',**xargs)
# -----------------------------------------------------------------------------
def parse_title(curfig,line,**xargs):
	return parse_label(curfig,line,_labmarker='',**xargs)
# -----------------------------------------------------------------------------
def parse_lim(curfig,line,**xargs):
	#!<DEV:EXPR>
	al = s2gf.array_x(s2gf.getarg1(line))
	m0 = xargs['_axmarker']
	curfig.axopt += '%saxis min %s max %s\n'%(m0,al[0],al[1])
	#
	# no new fig, no rest of line, no new stack
	return 0,'',''
# -----------------------------------------------------------------------------
def parse_xlim(curfig,line,**xargs):
	return parse_lim(curfig,line,_axmarker='x',**xargs)
# -----------------------------------------------------------------------------
def parse_ylim(curfig,line,**xargs):
	return parse_lim(curfig,line,_axmarker='y',**xargs)
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
	# return a new S2G figure + rest of line, no new stack
	return s2gc.S2GFIG(fn,xargs['no_tex']),sub(regex,'',line),''
# -----------------------------------------------------------------------------
def parse_legend(curfig,line,**xargs):
	# legend as stack
	leg_stack = s2gf.get_fargs(line)
	leg_c 	  = 0
	while leg_stack:
		leg_i_str   = s2gf.getnextargNL(leg_stack)
		leg_i_str_l = leg_i_str.lower()
		if   leg_i_str_l == 'location':
			leg_loc       = s2gf.getnextarg(leg_stack)
			curfig.legpos = 'pos %s'%s2gd.leg_dict.get(leg_loc,'tr')
		elif leg_i_str_l == 'boxoff':
			curfig.legopt+= ' nobox'
		elif leg_i_str_l == 'offset':
			leg_off       = s2gf.array_x(leg_stack.pop(0))
			curfig.legoff = ' offset '+' '.join(leg_off)
		else:
			if xargs['no_tex']: leg_i_str = sub(r'\\','/',leg_i_str)
			#
			try:
				curfig.legend += 'text "%s" %s\n'%(leg_i_str,curfig.lstyles[leg_c])
				leg_c         += 1
			except IndexError, e:
				s2gc.S2GSyntaxError(line,'<::found too many legends, did you forget a HOLD?::>')
	return 0,'',''
# -----------------------------------------------------------------------------
def parse_set(curfig,line,**xargs):
	#
	# syntax: 	set(gca, ...)
	#	 		set(gcf, ...)
	args = s2gf.get_fargs(line)
	obj  = s2gf.getnextarg(args)
	# AXIS
	if obj == 'gca':
		while args:
			arg = s2gf.getnextarg(args)
			if match(r'[xy]tick$',arg):
				ticks = s2gf.safe_pop(args,arg)
				#!<DEV:EXPR>
				nc = ticks.count(':')
				if nc==1: # format a:b
					f,l = match(r'\[?\s*(.+)\s*:\s*(.+)\s*\]?',ticks).group(1,2)
					num = int(floor(float(l)-float(f))+1)
					curfig.axopt+='%saxis ftick %s dticks 1 nticks %i\n'%(arg[0],f,num)
				elif nc==2: # format a:b:c
					f,d,l = match(r'\[?\s*(.+?)\s*:\s*(.+?)\s*:\s*(.+?)\s*\]?',ticks).group(1,2,3)
					num   = int(floor((float(l)-float(f))/float(d)+1))
					curfig.axopt+='%saxis ftick %s dticks %s nticks %i\n'%(arg[0],f,d,num)
				else: # a or [a b c]
					ticks = s2gf.strip_d(ticks,r'\[|\]')
					ticks = sub(',',' ',ticks)
					curfig.axopt+='%splaces %s\n'%(arg[0],ticks)
			elif match(r'[xy]ticklabel$',arg):
				raw    = s2gf.safe_pop(args,arg)
				labels = s2gf.strip_d(raw,r'\[|\]')
				labels = sub(r'\'','"',labels)
				labels = sub(',',' ',labels)
				if xargs['no_tex']:
					curfig.axopt+='%snames %s\n'%(arg[0],sub(r'\\','/',labels))
				else:
					curfig.axopt+='%snames %s\n'%(arg[0],sub('%','\%',labels))
			elif match(r'[xy]scale$',arg):
				scale = s2gf.safe_pop(args,arg)
				curfig.axopt+='%saxis log\n'%arg[0]
			elif match(r'[xy]lim$',arg):
				al  = s2gf.safe_pop(args,arg)
 				curfig.axopt+='%saxis min %s max %s\n'%(arg[0],al_[0],al_[1])
 			elif match(r'fontsize$',arg):
 				fs  = s2gf.safe_pop(args,arg)
 				curfig.figoptfs = 'set hei %f'%(float(fs)/28.35/2.) # psp to cm
 	# FIGURE
	elif obj == 'gcf':
		while args:
			#!<DEV>
			pass
	else:
		s2gc.S2GSyntaxError(line,'<::unknown object handle in SET::>')
	#
	# no new fig, no rest of line, no new stack
	return 0, '',''
# -----------------------------------------------------------------------------
def parse_axis(curfig,line,**xargs):
	args = s2gf.get_fargs(line)
	if args:
		#!<DEV:EXPR>
		al = s2gf.array_x(s2gf.getnextarg(args))
		block = 'xaxis min %s max %s\n'%(tuple(al[:2]))
		block+= 'yaxis min %s max %s\n'%(tuple(al[2:]))
		curfig.axopt+=block
	else:
		#!<DEV check if axis ij, ...>
		pass
	#
	# no new fig, no rest of line, no new stack
	return 0, '',''
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
		#
		if opt == 'color':
			opt_style['color'],foo,optsraw = s2gf.get_color(optsraw)
		elif opt in ['linewidth','lwidth']:
			#!<DEV:EXPR>
			opt = s2gf.getnextarg(optsraw)
			# black magic...
			opt_style['lwidth'] = str(round(((float(opt)/3)**.7)/10,2))
		elif opt in ['markersize','msize']:
			#!<DEV:EXPR>
			opt = s2gf.getnextarg(optsraw)
			# black magic...
			opt_style['msize'] = str(round(((float(opt)/5)**.5)/5,2))
		elif opt in ['markerfacecolor','mfcol']:
			opt = s2gf.getnextarg(optsraw) # will not be considered
			cm  = opt_style['marker']
			cm2 = 'f' if cm in ['circle','triangle','square'] else ''
			opt_style['marker'] = cm2+cm
		# keep this quick option last since match matches almost anything
		elif ma_lstyle:
			opt_style['lstyle'] = '' # in case only marker
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
		else:
			s2gc.S2GSyntaxError(line,'<::unknown option in plot::>')
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
	script += addscrvar('c__',s2gd.csd['cbind']([vx,vy]))
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
	# store lstyles for legend
	lb,mb  = bool(opt_style['lstyle']),bool(opt_style['marker'])
	lbool  = lb or not mb
	lsty   = opt_style['lstyle']+'0'*(not lb)
	line   = ('lstyle '+lsty+' lwidth '+opt_style['lwidth'])*lbool
	#fill   = 'f'*(opt_style['marker'] in ['circle','square','triangle'])*flags['mface']
	marker = 'marker '*mb+opt_style['marker']
	color  = 'color '+opt_style['color']
	lstyle = ' '+line+' '+marker+' '+color+' '
	curfig.lstyles.append(lstyle)
	#
	# no newfig, no rest of line, no new stack
	return 0,'',''
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
			s2gc.S2GSyntaxError(line,'<::unknown option in hist::>')
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
	script += addscrvar('c2__',s2gd.csd['rbind'](
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
	# no newfig, no rest of line, no new stack
	return 0,'',''
# -----------------------------------------------------------------------------
def parse_bar(curfig,line,**xargs):
	# increment plot counter if figure held or if 0
	curfig.cntr += checkplot(curfig)
	#
	# syntax: 	bar(x,...)
	#			bar(x,y,...)
	args = s2gf.get_fargs(line)
	#
	# DEV DEV DEV DEV
	# DEV DEV DEV DEV
	#
	# no newfig, no rest of line, no new stack
	return 0,'',''
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
			s2gc.S2GSyntaxError(line,'<::unknown option in fill::>')
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
	script += addscrvar('c__', s2gd.csd['cbind']([vx, vy1, vy2]))
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
	# no newfig, no rest of line, no new stack
	return 0,'',''
# -----------------------------------------------------------------------------
