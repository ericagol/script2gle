# script2gle

## Warning

This project is still under (rather heavy but infrequent) development.

## What this is about

The rough idea is to use `Matlab/Octave` style syntax for plots whilst generating GLE ([Graphics Layout Engine](http://glx.sourceforge.net/index.html)) code in the background to output paper-quality graphs. The advantage of using GLE it supports the use of LaTeX very easily (cf. example).

Roughly, the workflow is as follows:

1. "Parse" the script (.jl or .m),
2. Remove the lines where plotting is done following `Matlab/Octave` syntax and write it in corresponding `.gle` code, replace these lines by `write` lines (for `.dat` output) in a temporary script file,
3. Run the temporary script: `.dat` files are generated
4. Run GLE: `.pdf` or `.png` files are generated
5. Remove temporary files (unless option `-dev` is chosen)

**Rem**: if `-dev` option is chosen, one can have a look at the temporary files that have been created (useful for debugging), the temporary files are hidden by default with names starting with `.__`, if you can't see them use `ls -a` in the appropriate directory.

## Requirements

- A working version of `Python 2.x` (tested with `2.7.6`),
- A working version of GLE ([Link](http://glx.sourceforge.net/index.html)),
- A working version of `pdflatex` (tested with `pi-2.6-x`)
- A working version of Julia,Octave or Matlab (depending on what you want to use),

I'm assuming that your `$PATH` variable has been updated accordingly so that you can call each of those with `gle`, `julia`, `octave` and `matlab`.

If you intend to use transparency (`fill` command), then GLE needs to be able to run with a `cairo` option, nothing to be done on Linux (tested on Fedora) or OSX (tested on Yosemite) but I haven't tested it on Windows.

## Quick example

With `Julia` go to the `examples/julia` directory and run

```Bash
../../s2g ex_basic.jl -tex
```

With `Octave/Matlab` go to the `examples/octavematlab`

```Bash
../../s2g ex_axis.m -tex
```

It takes a few seconds to compile the figure since it must run `pdflatex` to generate the labels etc. Note that by default (without option), TeX is disabled so that one can have a quick look at figures (or if your figure has no need for TeX):

```Bash
../../s2g ex_basic.jl
```

If you want a png output, use the option `-png` eg:

```Bash
../../s2g ex_basic.jl -tex -png
```

## Example in Octave/Matlab

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