y = [75 91 105 123.5 131 150 179 203 226 249 281.5];
x__  = y;
y__ = x__;
y__ = reshape(y__, (size(y__,1)>1)*size(y__,1)+(size(y__,1)==1)*size(y__,2), (size(y__,1)>1)*size(y__,2)+(size(y__,1)==1)*size(y__,1));
lsp = 1:size(y__,1);
c__ = [lsp(:) y__];
ncols__ = size(y__,2);
save('-ascii','.__datbar1_1.dat','c__');
c2__ = ncols__;
save('-ascii','.__datbar1_1_side.dat','c2__');