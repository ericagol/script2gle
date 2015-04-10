# script2gle

## Warning

This project is still under (rather heavy but infrequent) development.

## What this is about

The rough idea is to use `Matlab` style syntax for figures whilst generating GLE ([Graphics Layout Engine](http://glx.sourceforge.net/index.html)) code in the background to output top-quality graphs with TeX support. The advantage of using GLE it supports the use of LaTeX very easily (cf. example).

Roughly, the workflow is as follows:

1. "Parse" the script (`.jl`, `.m` or `.R` so far),
2. Separate code for displaying, translate it and generate corresponding `.gle` code, add lines to output data needed by plots as temporary `.dat` files,
3. Run the temporary script: `.dat` files are generated,
4. Run GLE: `.pdf` or `.png` files are generated,
5. Remove temporary files (unless option `-dev` is chosen)

**Rem**: if `-dev` option is chosen, one can have a look at the temporary files that have been created (useful for debugging), the temporary files are hidden by default with names starting with `.__`, if you can't see them use `ls -a` in the appropriate directory.

## Requirements

- A working version of `Python 2.x` (tested with `2.7.6`),
- A working version of GLE ([Link](http://glx.sourceforge.net/index.html)),
- A working version of `pdflatex` (tested with `pi-2.6-x`)
- A working version of Julia,Octave or Matlab (depending on what you want to use),

I'm assuming that your `$PATH` variable has been updated accordingly so that you can call each of those with `gle`, `julia`, `octave` and `matlab`.

If you intend to use transparency (`fill` command), then GLE needs to be able to run with a `cairo` option, nothing to be done on Linux (tested on Fedora) or OSX (tested on Yosemite) but I haven't tested it on Windows. Also a warning may be issued if you're using this in the draft mode (without the `-tex` option), and the font might be changed to agree with cairo. Compile with `-tex` option to get rid of that warning.

## Quick example of how to run S2G

With (say) `Julia` go to the `examples/julia` directory and run

```Bash
../../s2g ex_basic.jl -tex
```

It takes a few seconds to compile the figure since it must run `pdflatex` to generate the labels etc. Note that by default (without option), TeX is disabled so that one can have a quick look at figures (or if your figure has no need for TeX):

```Bash
../../s2g ex_basic.jl
```

If you want a png output, use the option `-png` eg:

```Bash
../../s2g ex_basic.jl -tex -png
```

## Understanding the workflow with an example

Running the above command with the `-dev` option generates the following files:

1. `.__ex_basic_script_tmp.jl` whose core is
```Julia
x = linspace(-5,5,500)
y = exp(-(x).^2/2)
x__ = x
y__ = y
c__ = [x__[:] y__[:]]
writecsv(".__datplot1_1.dat",c__)
```
so you can see that the script that ends up being run only aims at producing `.dat` files on which the plots will be based. 
2. `.__ex_basic_plot1_g.gle` whose core is
```
begin graph
	scale auto
	data ".__datplot1_1.dat" d1=c1,c2
	d1 lstyle 0  color darkblue  lwidth 0.06  msize 0.2 
	xsubticks off 
	ysubticks off
	x2axis off
	y2axis off
	title "The std normal distribution"
	xtitle "$x$"
	ytitle "$/mathcal N(x;0,1)$"
end graph
```
this is the GLE syntax which will generate one plot based on the given `.dat` file.
3. `.__datplot1_1.dat` which contains lines like
```
-3.6773547094188377,.0011575277138466272
-3.657314629258517,.001245802786172585
-3.637274549098196,.0013402715011302559
-3.6172344689378755,.0014413247808285163
-3.5971943887775546,.0015493748758152082
```
that were generated after running the temporary script file.

Compiling the GLE file above will then generate the desired `.pdf` file.

## An example in Octave/Matlab

Here is a very simple example with Octave/Matlab, in a file `smalltest.m` (already in `examples/octavematlab/`) write:

```Matlab
x = linspace(-5,5,500);
plot(x,exp(-x.^2/2),'-b')
hold on
plot(x,exp(-abs(x)),'-','color','cornflowerblue')
set(gca,'ytick',[0 0.5 1],'yticklabel',['0', '1/2', '1'])
set(gca,'xtick',[-5 -2.5 0 2.5 5])
xlabel('$x$')
ylabel('$p(x)$')
legend('$\propto\mathcal N(0,1)$','$\propto$ Laplace','Location','southeast')
```

**Remark**: due to the similarity between Octave/Matlab and Julia syntax, the above example can be also be run with Julia, just name it `smalltest.jl` and let `s2g` do the rest. 

in your terminal, in the same directory with `$PATHS2G` the path to the executable `s2g`,

```Bash
$PATHS2G/s2g smalltest.m -tex -png
```

which should generate the figure below:

![smalltest.m](/examples/octavematlab/smalltest_plot1_g.png)

another similar example with the `fillbetween` command

```Matlab
x = linspace(-5,5,500);
plot(x,exp(-x.^2/2),'-r')
hold on
plot(x,exp(-abs(x)),'-','color','cornflowerblue')
set(gca,'ytick',[0 0.5 1],'yticklabel',['0', '1/2', '1'])
set(gca,'xtick',[-5 -2.5 0 2.5 5])
xlabel('$x$')
ylabel('$p(x)$')
legend('$\propto\mathcal N(0,1)$','$\propto$ Laplace','location','southeast')
set(gca,'fontsize',12)
fillbetween(x,exp(-x.^2/2),exp(-abs(x)),'color','palegreen','alpha',0.7)
```

which should generate the figure below:

![smalltest2.m](/examples/octavematlab/smalltest2_plot1_g.png);

**Remark**: as you may have realized, `fillbetween` is not part of Matlab syntax, it's just a useful extension here, and the idea is to have a `Matlab-like` syntax but without restriction for a bit of syntactic sugar (remember, this does not have the ambition to be an award winning software (...) but rather to be a useful hack).

## Additional comments
### Use of transparency
- needs `-cairo` working (ok on Linux, Mac, ?Windows)
- the `alpha` needs to be directly the color option so `(...,'color','cornflowerblue','alpha',0.8)` is the valid syntax
- another way to use it is the RGBA syntax: `(...,[0.2,0.3,0.9,0.5])` will take `r=0.2` etc and `alpha=0.5`.
