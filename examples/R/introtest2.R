draw1 = rnorm(500,mean=1,sd=5)
draw2 = rnorm(500,mean=2,sd=5)
x    = seq(-15,20,len=200)
y 	 = dnorm(x,mean=1,sd=5)
# The Matlab-like syntax below is extracted and treated by S2G
hist(draw1,'normalization','pdf',...
	'facecolor','indianred','alpha',0.5,'edgecolor','indianred')
hold on
hist(draw2,'normalization','pdf',...
	'facecolor','navy','alpha',0.5,'edgecolor','navy')
plot(x,y,'-b','linewidth',0.5)
xlabel('$x$')
ylabel('$y=\mathcal N(x;1,5)$')