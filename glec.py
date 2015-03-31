from subprocess	import check_call
from re import sub

class GLE:
	def __init__(self,fname=''):
		# ----------------------------------------
		# <GLE> Public variables -- initialization
		# ----------------------------------------
		self.fname		= fname
		self.figsize 	= 'size 6 4'				# figure size
		self.figopt  	= 'set hei .25 font psh'	# fontsize, if latex true, font ignored
		self.tex  	  	= True 						# enable LaTeX engine
		self.texfont 	= 'palatino' 				# > Latex font
		self.texmfont 	= 'mathpazo' 				# > Latex math font
		self.scale   	= 'scale auto'				# fig centered + tight box
		self.plot    	= ''						# typical = what+linespec
		self.axopt   	= '''	xsubticks off 		
								ysubticks off
								x2axis off
								y2axis off\n''' 	# axis options (log, xplaces..)
		self.extra  	= ''						# add. stuff (draw arrow,..)
		self.legend  	= ''						# legend
		self.legopt  	= 'compact pos tr'		    # legend position, style

		# -----------------------
		# <GLE> Private variables
		# -----------------------
		self.fext   = '_g.gle'

	# ----------------------
	# <GLE> Public functions
	# ----------------------
	def no_prompt(self):
		self.prompt = False

	def compile(self,png_resol=''):	
		self.__write()
		try:
			print 'GLE::compiling fig... < %s >'%self.fname
			if png_resol:
				check_call('gle -device png -r %s -vb 0 %s%s'%
					(png_resol,self.fname,self.fext),shell=True)
			else:
				check_call('gle -device pdf -vb 0 %s%s'%
					(self.fname,self.fext),shell=True)
		except Exception, e:
			 print e

	def writefile(self): # if just want the glefile
		self.__write()

	# -----------------------
	# <GLE> Private functions
	# -----------------------
	def __glepath(self):
		return self.fname+self.fext

	def __write(self):
		axopt = self.axopt.replace('\t','')
		axopt = axopt.replace('\n','\n\t')
		axopt = sub(r'^\s*','\t',axopt)
		plot  = self.plot.replace('\t','')
		plot  = plot.replace('\n','\n\t')
		# symbols to simplify notations
		n,t = '\n','\t'
		nt  = n+t
		# graph framework
		graph =	'begin graph'	+nt+\
					self.scale 	+nt+\
					plot 		+n +\
					axopt 		+n +\
				'end graph'
		# key (legend) framework
		key   = 'begin key' 	+nt+\
					self.legopt +nt+\
					self.legend +n +\
				'end key'
		# write everything to .GLE file
		with open(self.__glepath(),'w+') as gle_out__:
			gle_out__.write('''!This GLE document was generated\n'''+
							'''!AUTOMATICALLY and should only be modified\n'''+
							'''!through the generating source.'''+n*2)
			# Fig basics
			gle_out__.write( self.figsize+n+
							 self.figopt +n*2 )
			# Tex setup
			if self.tex:
				gle_out__.write('begin texpreamble'					+nt+
								'\usepackage{'+self.texfont+'}'		+nt+
								'\usepackage{'+self.texmfont+'}'	+n +
								'end texpreamble' 					+n +
								'set texlabels 1 texscale scale' 	+n*2)
			# Main write
			gle_out__.write( graph 	    +n*2+
						 	 self.extra +n*2+
							 key )
# Complementary functions
def gle(name):
 		return GLE(fname=name)
