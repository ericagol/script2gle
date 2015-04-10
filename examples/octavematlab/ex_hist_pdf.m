s = 5;
draw = s*randn(1000,1);
hist(draw,20,'color','cornflowerblue', ...
	'normalization','pdf')
x = linspace(-15,15,500);
y = normpdf(x,0,s);
hold on
plot(x,y,'-r')