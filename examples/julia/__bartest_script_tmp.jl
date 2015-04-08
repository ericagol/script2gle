using Distributions

N    = 500
dist = Erlang(7,0.5)
#dist = Normal(0,1)
draw = rand(dist,N)

x__  = draw
c__ = x__[:]
writecsv("__dathist1_1.dat",c__)

# # histogram
# nbins = int(round(sqrt(N)))
# isort = sortperm(draw)
# dsort = draw[isort]
# minval= dsort[1]
# maxval= dsort[end]
# delta = (maxval-minval)/nbins/2
# x     = linspace(minval+delta,maxval-delta,nbins)
# cutoff= x+delta
# chist = 0*x
# chist[1] = sum(dsort.<cutoff[1])
# s = chist[1]
# for i=2:nbins
# 	chist[i] = sum(dsort.<cutoff[i])-s
# 	s+=chist[i]
# end
# xmids = x-(x[1]-minval)/2
# c__ = [xmids[:] chist]
# writecsv("bartestDAT.dat",c__)
exit()
