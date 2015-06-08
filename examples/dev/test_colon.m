x = linspace(-2,2,100);
y = [normpdf(x,0,1);
	 normpdf(x,-1,1);
	 normpdf(x,1,1)];

figure
hold on
plot(x,y(1,:),'-r')
plot(x,y(2,:),'-b')
plot(x,y(3,:),'-c')