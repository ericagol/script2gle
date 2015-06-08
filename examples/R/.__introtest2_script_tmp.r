draw1 = rnorm(500,mean=1,sd=5)
draw2 = rnorm(500,mean=2,sd=5)
x    = seq(-15,20,len=200)
y 	 = dnorm(x,mean=1,sd=5)
x__=draw1
xv__=c(x__)
write.table(xv__,file='.__dathist1_1.dat',row.names=F,col.names=F)
xmin__=min(xv__)
xmax__=max(xv__)
nbins__=(length(xv__)<10)*length(xv__)+(10<=length(xv__) && length(xv__)<30)*10+(30<=length(xv__))*round(sqrt(length(xv__)))
c2__=rbind(xmin__,xmax__,nbins__)
write.table(c2__,file='.__dathist_sup1_1.dat',row.names=F,col.names=F)
x__=draw2
xv__=c(x__)
write.table(xv__,file='.__dathist1_4.dat',row.names=F,col.names=F)
xmin__=min(xv__)
xmax__=max(xv__)
nbins__=(length(xv__)<10)*length(xv__)+(10<=length(xv__) && length(xv__)<30)*10+(30<=length(xv__))*round(sqrt(length(xv__)))
c2__=rbind(xmin__,xmax__,nbins__)
write.table(c2__,file='.__dathist_sup1_4.dat',row.names=F,col.names=F)
x__=x
y__=y
c__=cbind(c(x__),c(y__))
write.table(c__,file='.__datplot1_7.dat',row.names=F,col.names=F)

