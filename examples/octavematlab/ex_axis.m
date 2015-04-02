x = linspace(-3,6,200);
y = sin(x).*exp(-x.*cos(x));
plot(x,y,'-r','linewidth',2)

% AXIS TICKS
% > axis ticks
set(gca,'xtick',[0,4],'ytick',-15:5:5)
set(gca,'xticklabel',['origin', 'down'])
% > axis limits
set(gca,'xlim',[-3.5,7])
ylim([-15,5])

% LABELS
% tex is accepted
xlabel('The x label $x=\sin(\theta^2)$')
title('Hello this is the title')