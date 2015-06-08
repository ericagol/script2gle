import glec
import s2gd

class S2GFIG(glec.GLE):
	def __init__(self,fignum,notex=True):
		fn = '%s%s_fig%i'%(s2gd.tind,s2gd.sname,fignum) 
		glec.GLE.__init__(self,fn)
		# in GLE
		self.tex  	  = not notex
		#
		# specific S2GFIG
		self.fignum   = fignum
		self.cntr     = 0 # to increment over datasets
		self.nplots   = 0 # to increment over actual objects
		self.flags    = {'holdon':False}
		self.lstyles  = [] # for legend

class S2GSyntaxError(Exception):
	def __init__(self,line,message=''):
		self.line = line
		self.message = message
	def __str__(self):
		return self.line, self.message