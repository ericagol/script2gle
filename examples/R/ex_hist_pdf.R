s = 5
draw = rnorm(100,mean=0,sd=s);
hist(draw,20,'color','cornflowerblue', ...
	'normalization','pdf')
x = seq(-15,15,len=500);
y = dnorm(x,mean=0,sd=s);
hold on
plot(x,y,'-r')