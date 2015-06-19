
from s2gf import *

check_lambdas  		= False
check_getfargs 		= True
check_arrayx   		= False
check_getcolor 		= False
check_closeellipsis = False

# LAMBDA FUNCTIONS
if check_lambdas:
	print '\n -- L::MATCH START -- '
	s = "  plota(..."
	print 'PASS' if match_start('plota',s) and not match_start('plot',s) else 'FAIL'
	s = "   T0(..."
	print 'PASS' if match_start('T0',s) and not match_start('T',s) else 'FAIL'

# -- GET FARGS (basic parsing)
if check_getfargs:
	print '\n -- GETFARGS CHECK --'
	s = "plot(x,y,'linewidth',1.5,'color', [0.1,0.1,0.9])"
	test = (get_fargs(s) == ['x', 'y', "'linewidth'", '1.5', "'color'", '[0.1,0.1,0.9]'])
	print 'PASS' if test else 'FAIL',1
	s = "plot(x,y','linewidth',1.5)"
	test = (get_fargs(s) == ['x', "y'", "'linewidth'",'1.5'])
	print 'PASS' if test else 'FAIL',2
	s = "marker('a string, ( ]', 'another!', y'*a')"
	test = (get_fargs(s) == ["'a string, ( ]'", "'another!'", "y'*a'"])
	print 'PASS' if test else 'FAIL',3
	s = "marker( [y',x',z], ' blah  ')"
	test = (get_fargs(s) == ["[y',x',z]","' blah  '"])
	print 'PASS' if test else 'FAIL',4
	s = "function(x',y(1,:)','linewidth',2)"
	test = (get_fargs(s) == ["x'","y(1,:)'","'linewidth'",'2'])
	print 'PASS' if test else 'FAIL',5

# -- ARRAY X (extract array) [SHOULD BE OBSOLETED, the array should be INTERPRETED by the script]
if check_arrayx:
	print '\n -- ARRAY X --'
	s = '[2.0 -2.3]'
	test = (array_x(s) == ['2.0','-2.3'])
	print 'PASS' if test else 'FAIL'
	s = '1:5'
	test = (array_x(s) == ['1.0','2.0','3.0','4.0','5.0'])
	print 'PASS' if test else 'FAIL'
	s = '[1:5]'
	test = (array_x(s) == ['1.0','2.0','3.0','4.0','5.0'])
	print 'PASS' if test else 'FAIL'
	s = '1:.5:3'
	test = (array_x(s) == ['1.0','1.5','2.0','2.5','3.0'])
	print 'PASS' if test else 'FAIL'

# -- GET COLOR 
if check_getcolor:
	print '\n -- GET COLOR --'
	s = ['[0.1,0.3, 0.4]']
	a,b,c = get_color(s)
	print 'PASS' if a=='rgba(0.1,0.3,0.4,1)' else 'FAIL'
	s = ['salmon','alpha','0.8']
	a,b,c = get_color(s)
	print 'PASS' if a=='rgba255(250,128,114,80.0)' else 'FAIL'
	s = ['salmon']
	a,b,c = get_color(s)
	print 'PASS' if a=='salmon' else 'FAIL'
	s = ['m']
	a,b,c = get_color(s)
	print 'PASS' if a=='darkmagenta' else 'FAIL'

# -- CLOSE ELLIPSIS
if check_closeellipsis:
	print '\n -- CLOSE ELLIPSIS --'
	stack = ["plot(x,y,...\n",
		 	 "'color','IndianRed' ,...",
			 "'linewidth', 2.0)"]
	a,b = close_ellipsis(stack.pop(0),stack)
	test = (a == "plot(x,y,'color','IndianRed' ,'linewidth', 2.0)") and not b
	print 'PASS' if test else 'FAIL'