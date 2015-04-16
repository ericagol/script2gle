
from s2gf import *

check_getfargs = True


# LAMBDA FUNCTIONS

# NORMAL FUNCTIONS

# -- GET FARGS (basic parsing)
if check_getfargs:
	s  = "plot(x,y,'linewidth',1.5,'color', [0.1,0.1,0.9])"
	print s
	print '::> ', 'PASS' if (get_fargs(s) == ['x', 'y', "'linewidth'", '1.5', "'color'", '[0.1,0.1,0.9]']) else get_fargs(s)
	s = "plot(x,y','linewidth',1.5)"
	print s
	print '::> ', 'PASS' if (get_fargs(s) == ['x', "y'", "'linewidth'",'1.5']) else get_fargs(s)
	s = "marker('a string, ( ]', 'another!', y'*a')"
	print s
	print '::> ', 'PASS' if (get_fargs(s) == ["'a string, ( ]'", "'another!'", "y'*a'"]) else get_fargs(s)
	s = "marker( [y',x',z], ' blah  ')"
	print s
	print '::> ', 'PASS' if (get_fargs(s) == ["[y',x',z]","' blah  '"]) else get_fargs(s)

