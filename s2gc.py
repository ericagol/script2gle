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
		self.plotcntr = 0
		self.flags    = {'holdon':False}
		self.lstyles  = [] # for legend
