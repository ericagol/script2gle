draw1 = rnorm(500,mean=1,sd=5)
draw2 = rnorm(500,mean=2,sd=5)
x    = seq(-15,20,len=200)
y 	 = dnorm(x,mean=1,sd=5)
# The Matlab-like syntax below is extracted and treated by S2G
hist(draw1,'normalization','pdf',...
	'facecolor','indianred','alpha',0.5,'edgecolor','indianred')
hold on
# using to/from specification so that bins overlap exactly
# (if removed then bins will be adjusted from min to max)
hist(draw2,'normalization','pdf',...
	'facecolor','navy','alpha',0.5,'edgecolor','navy',...
	'from',min(draw1),'to',max(draw1))
plot(x,y,'-b','linewidth',0.5)
xlabel('$x$')
ylabel('$y=\mathcal N(x;1,5)$')

legend('leg1','leg2','leg3')