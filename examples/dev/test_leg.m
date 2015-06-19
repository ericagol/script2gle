x = linspace(-2,2,100);
y = [normpdf(x,0,1);
	 normpdf(x,-1,1);
	 normpdf(x,1,1)];

figure
hold on
plot(x,y(1,:)*2,'color','CornflowerBlue')
xlabel( '$\mathcal N(x;0,1)$')
legend('$\mathcal N(x;0,1)$')