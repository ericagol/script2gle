x = linspace(-2,2,100);
y = [normpdf(x,0,1);
	 normpdf(x,-1,1);
	 normpdf(x,1,1)];

figure
hold on
plot(x,y(1,:)*2,'color','CornflowerBlue')
plot(x,y(2,:)*2,'color','DeepPink')
plot(x,y(3,:)*2,'-r','linewidth',1.5)
legend('$\mathcal N(x;0,1)$','$\mathcal N(x;-1,1)$','$\mathcal N(x;1,1)$')