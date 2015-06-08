x = linspace(-2,2,100);
y = t_myfun1(x);

x__=x;
y__=y;
c__=[x__(:) y__(:)];
save('-ascii','.__datplot1_1.dat','c__');

exit()
