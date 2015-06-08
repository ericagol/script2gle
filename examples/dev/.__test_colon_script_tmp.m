x = linspace(-2,2,100);
y = [normpdf(x,0,1);
	 normpdf(x,-1,1);
	 normpdf(x,1,1)];

x__=x;
y__=y(1,:)*2;
c__=[x__(:),y__(:)];
save('-ascii','.__datplot1_1.dat','c__');
x__=x;
y__=y(2,:)*2;
c__=[x__(:),y__(:)];
save('-ascii','.__datplot1_2.dat','c__');
x__=x;
y__=y(3,:)*2;
c__=[x__(:),y__(:)];
save('-ascii','.__datplot1_3.dat','c__');

exit()
