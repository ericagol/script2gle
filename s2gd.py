# SHARED VARIABLES
#
csd = {} # current script dictionary, this is set by S2G
		 # by default, set to matlab (see end of this file)
sname = ''
tind  = '.__' # temporary file indicator

# DICTIONARIES
#
# start of line markers
# > can appear but line won't be considered
ignored = r'|'.join([r'^\s*home',r'^\s*clear',r'^\s*close'])
# > can appear and will trigger something
markers = r'|'.join([ 	
	'figure',
	'plot',
	'fill',
	'fillbetween',			# extra syntax
	'hist','histogram',
	'bar',
	'hold',
	r'[xy]lim',
	r'[xy]label',
	'title',
	r'[xy]?axis',
	'set',
	'legend',
	r'semilog[xy]',
	'loglog',
	'stem',
	r'(#j2g:)'])
#
# definition of script dictionary in different languages
#
script_dict_JL = {
	'append'	: 'include',
	'writevar'	: 'writecsv(\"{0}\",{1})', # with .format not %
	'vec'		: '%s[:]',
	'asmatrix' 	: '%s',
	'minvec'	: 'minimum(%s)',
	'maxvec'	: 'maximum(%s)',
	'lenvec'	: 'length(%s)',
	'nrows'		: 'size(%s,1)',
	'ncols'		: 'size(%s,2)',
	'numel'		: 'prod(size(%s))',
	'tifrow' 	: 'ifelse(size({0},1)>1,{0},{0}\')',
	'autobins'  : '({0}<10)*{0}+(10<={0}<30)*10+(30<={0})*int(round(sqrt({0})))',
	'EOL'		: '',
	'cbind' 	: '[%s %s]',
	'rbind'		: '[%s;%s]',
	'span' 		: '1:%s',
	'exit' 		: 'exit()',
	'comment' 	: '\#',
	'caller'	: 'julia'
}
script_dict_R = {
	'append'	: 'source',
	'writevar'	: 'write.table({1},file=\'{0}\',row.names=F,col.names=F)',
	'vec'		: 'c(%s)',
	'asmatrix' 	: 'as.matrix(%s)',
	'minvec'	: 'min(%s)',
	'maxvec'	: 'max(%s)',
	'lenvec'	: 'length(%s)',
	'nrows'		: 'nrow(%s)',
	'ncols'		: 'ncol(%s)',
	'numel'		: 'length(%s)',
	'tifrow' 	: 'if(nrow{0}>1){{0}}else{t({0})}',
	'autobins'  : '({0}<10)*{0}+(10<={0} && {0}<30)*10+(30<={0})*round(sqrt({0}))',
	'EOL'		: '',
	'cbind' 	: 'cbind(%s,%s)',
	'rbind'		: 'rbind(%s,%s)',
	'span' 		: '1:%s',
	'exit'		: 'q()',
	'comment'	: '\#',
	'caller'	: 'Rscript'
}
script_dict_M = {
	'append'	: 'run',
	'writevar'	: 'save(\'-ascii\',\'{0}\',\'{1}\')',
	'vec'		: '%s(:)',
	'asmatrix' 	: '%s',
	'minvec'	: 'min(%s)',
	'maxvec'	: 'max(%s)',
	'lenvec' 	: 'length(%s)',
	'nrows'		: 'size(%s,1)',
	'ncols' 	: 'size(%s,2)',
	'numel' 	: 'numel(%s)',
	'tifrow' 	: 'reshape({0}, (size({0},1)>1)*size({0},1)+(size({0},1)==1)*size({0},2), (size({0},1)>1)*size({0},2)+(size({0},1)==1)*size({0},1))',
	'autobins'	: '({0}<10)*{0}+(10<={0} && {0}<30)*10+(30<={0})*round(sqrt({0}))',
	'EOL'		: ';',
	'cbind'		: '[%s %s]',
	'rbind'		: '[%s;%s]',
	'span'		: '1:%s',
	'exit'		: 'exit()',
	'comment' 	: '\%',
	'caller'	: 'octave -q'
}
#
# legend position conversion matlab/octave > gle
#
leg_dict = {
	'north'				: 'tc',
	'n'					: 'tc',
	'northoutside'		: 'tc offset 0 -0.1', # need figsize adjustment + removal of scale auto
	'no' 				: 'tc offset 0 -0.1',
	'northwest'			: 'tl',
	'nw' 				: 'tl',
	'northwestoutside'	: 'tl offset -0.1 0', # idem
	'nwo'				: 'tl offset -0.1 0',
	'northeast'			: 'tr',
	'ne'				: 'tr',
	'northeastoutside'	: 'tr offset -0.1 0', # idem
	'neo'				: 'tr offset -0.1 0',
	'south'				: 'bc',
	's'					: 'bc',
	'southoutside'		: 'bc offset 0 -0.1', # idem
	'so'				: 'bc offset 0 -0.1',
	'southwest'			: 'bl',
	'sw'				: 'bl',
	'southwestoutside'	: 'bl offset -0.1 0', # idem
	'swo'				: 'bl offset -0.1 0',
	'southeast' 		: 'br',
	'se'				: 'br',
	'southeastoutside' 	: 'br offset -0.1 0',
	'seo'				: 'br offset -0.1 0',
}
#
# basic matlab/octave color conversion to X11 names
#
mcol_dict = {
	'r'	: 'darkred',
	'g'	: 'darkgreen',
	'b' : 'darkblue',
	'c' : 'darkcyan',
	'm' : 'darkmagenta',
	'y' : 'goldenrod',
	'k' : 'black',
	'w' : 'white',
}
md = mcol_dict # short
#
# X11 names to rgb (useful when considering alpha)
#
svg2rgb_dict = {
	'Pink'				:	(255,192,203),
	'LightPink'			:	(255,182,193),
	'HotPink'			:	(255,105,180),
	'DeepPink'			:	(255,20,147),
	'PaleVioletRed'		:	(219,112,147),
	'MediumVioletRed'	:	(199,21,133),
	'LightSalmon'		:	(255,160,122),
	'Salmon'			:	(250,128,114),
	'DarkSalmon'		:	(233,150,122),
	'LightCoral'		:	(240,128,128),
	'IndianRed'			:	(205,92,92),
	'Crimson'			:	(220,20,60),
	'FireBrick'			:	(178,34,34),
	'DarkRed'			:	(139,0,0),
	'Red'				:	(255,0,0),
	'OrangeRed'			:	(255,69,0),
	'Tomato'			:	(255,99,71),
	'Coral'				:	(255,127,80),
	'DarkOrange'		:	(255,140,0),
	'Orange'			:	(255,165,0),
	'Yellow'			:	(255,255,0),
	'LightYellow'		:	(255,255,224),
	'LemonChiffon'		:	(255,250,205),
	'LightGoldenrodYellow':	(250,250,210),
	'PapayaWhip'		:	(255,239,213),
	'Moccasin'			:	(255,228,181),
	'PeachPuff'			:	(255,218,185),
	'PaleGoldenrod'		:	(238,232,170),
	'Khaki'				:	(240,230,140),
	'DarkKhaki'			:	(189,183,107),
	'Gold'				:	(255,215,0),
	'Cornsilk'			:	(255,248,220),
	'BlanchedAlmond'	:	(255,235,205),
	'Bisque'			:	(255,228,196),
	'NavajoWhite'		:	(255,222,173),
	'Wheat'				:	(245,222,179),
	'BurlyWood'			:	(222,184,135),
	'Tan'				:	(210,180,140),
	'RosyBrown'			:	(188,143,143),
	'SandyBrown'		:	(244,164,96),
	'Goldenrod'			:	(218,165,32),
	'DarkGoldenrod'		:	(184,134,11),
	'Peru'				:	(205,133,63),
	'Chocolate'			:	(210,105,30),
	'SaddleBrown'		:	(139,69,19),
	'Sienna'			:	(160,82,45),
	'Brown'				:	(165,42,42),
	'Maroon'			:	(128,0,0),
	'DarkOliveGreen'	:	( 85,107,47),
	'Olive'				:	(128,128,0),
	'OliveDrab'			:	(107,142,35),
	'YellowGreen'		:	(154,205,50),
	'LimeGreen'			:	( 50,205,50),
	'Lime'				:	(  0,255,0),
	'LawnGreen'			:	(124,252,0),
	'Chartreuse'		:	(127,255,0),
	'GreenYellow'		:	(173,255,47),
	'SpringGreen'		:	(  0,255,127),
	'MediumSpringGreen'	:	(  0,250,154),
	'LightGreen'		:	(144,238,144),
	'PaleGreen'			:	(152,251,152),
	'DarkSeaGreen'		:	(143,188,143),
	'MediumSeaGreen'	:	( 60,179,113),
	'SeaGreen'			:	( 46,139,87),
	'ForestGreen'		:	( 34,139,34),
	'Green'				:	(  0,128,0),
	'DarkGreen'			:	(  0,100,0),
	'MediumAquamarine'	:	(102,205,170),
	'Aqua'				:	(  0,255,255),
	'Cyan'				:	(  0,255,255),
	'LightCyan'			:	(224,255,255),
	'PaleTurquoise'		:	(175,238,238),
	'Aquamarine'		:	(127,255,212),
	'Turquoise'			:	( 64,224,208),
	'MediumTurquoise'	:	( 72,209,204),
	'DarkTurquoise'		:	(  0,206,209),
	'LightSeaGreen'		:	( 32,178,170),
	'CadetBlue'			:	( 95,158,160),
	'DarkCyan'			:	(  0,139,139),
	'Teal'				:	(  0,128,128),
	'LightSteelBlue'	:	(176,196,222),
	'PowderBlue'		:	(176,224,230),
	'LightBlue'			:	(173,216,230),
	'SkyBlue'			:	(135,206,235),
	'LightSkyBlue'		:	(135,206,250),
	'DeepSkyBlue'		:	(  0,191,255),
	'DodgerBlue'		:	( 30,144,255),
	'CornflowerBlue'	:	(100,149,237),
	'SteelBlue'			:	( 70,130,180),
	'RoyalBlue'			:	( 65,105,225),
	'Blue'				:	(  0,0,255),
	'MediumBlue'		:	(  0,0,205),
	'DarkBlue'			:	(  0,0,139),
	'Navy'				:	(  0,0,128),
	'MidnightBlue'		:	( 25,25,112),
	'Lavender'			:	(230,230,250),
	'Thistle'			:	(216,191,216),
	'Plum'				:	(221,160,221),
	'Violet'			:	(238,130,238),
	'Orchid'			:	(218,112,214),
	'Fuchsia'			:	(255,0,255),
	'Magenta'			:	(255,0,255),
	'MediumOrchid'		:	(186,85,211),
	'MediumPurple'		:	(147,112,219),
	'BlueViolet'		:	(138,43,226),
	'DarkViolet'		:	(148,0,211),
	'DarkOrchid'		:	(153,50,204),
	'DarkMagenta'		:	(139,0,139),
	'Purple'			:	(128,0,128),
	'Indigo'			:	( 75,0,130),
	'DarkSlateBlue'		:	( 72,61,139),
	'RebeccaPurple'		:	(102,51,153),
	'SlateBlue'			:	(106,90,205),
	'MediumSlateBlue'	:	(123,104,238),
	'White'				:	(255,255,255),
	'Snow'				:	(255,250,250),
	'Honeydew'			:	(240,255,240),
	'MintCream'			:	(245,255,250),
	'Azure'				:	(240,255,255),
	'AliceBlue'			:	(240,248,255),
	'GhostWhite'		:	(248,248,255),
	'WhiteSmoke'		:	(245,245,245),
	'Seashell'			:	(255,245,238),
	'Beige'				:	(245,245,220),
	'OldLace'			:	(253,245,230),
	'FloralWhite'		:	(255,250,240),
	'Ivory'				:	(255,255,240),
	'AntiqueWhite'		:	(250,235,215),
	'Linen'				:	(250,240,230),
	'LavenderBlush'		:	(255,240,245),
	'MistyRose'			:	(255,228,225),
	'Gainsboro'			:	(220,220,220),
	'LightGrey'			:	(211,211,211),
	'Silver'			:	(192,192,192),
	'DarkGray'			:	(169,169,169),
	'Gray'				:	(128,128,128),
	'DimGray'			:	(105,105,105),
	'LightSlateGray'	:	(119,136,153),
	'SlateGray'			:	(112,128,144),
	'DarkSlateGray'		:	( 47,79,79),
	'Black'				:	(  0,0,0),
}
svg2rgb_dict = {k.lower() : v for k, v in svg2rgb_dict.items()}
srd = svg2rgb_dict

# PARSER SPECIFICS
keyclose = {
	'\''	: '\'',
	'\"'	: '\"',
	'['		: ']',
	'('		: ')',
	'{'		: '}'
}
keyopen = keyclose.keys()

# Intialization of global variable if needed
csd = script_dict_M