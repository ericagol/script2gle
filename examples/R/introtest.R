draw = rnorm(500,mean=1,sd=5)
x    = seq(-15,20,len=200)
y 	 = dnorm(x,mean=1,sd=5)
# The Matlab-like syntax below is extracted and treated by S2G
hist(draw,'normalization','pdf',...
	'facecolor','indianred',...
	'edgecolor','dodgerblue')
hold on
plot(x,y,'-b','linewidth',0.5)
xlabel('$x$')
ylabel('$y=\mathcal N(x;1,5)$')