# tex2jem

## Warning

This project is still under (rather heavy but infrequent) development.

## What this is about

The rough idea is to use `Matlab/Octave` style syntax for plots whilst generating GLE ([Graphics Layout Engine](http://glx.sourceforge.net/index.html)) code in the background to output paper-quality graphs. The advantage of using GLE it supports the use of LaTeX very easily (cf. example).

Roughly, the workflow is as follows:

1. "Parse" the script (.jl or .m),
2. Remove the lines where plotting is done following `Matlab/Octave` syntax and write it in corresponding `.gle` code, replace these lines by `write` lines (`.dat` output) (*in tmp folder*)
3. Run the script, `.dat` files are generated (*in tmp folder*), 
4. Run GLE, `.pdf` or `.png` files are generated (*in tmp folder*),
5. Copy relevant files to the original directory.

## Requirements

- A working version of `Python 2.x` (tested with `2.7.6`),
- A working version of GLE ([Link](http://glx.sourceforge.net/index.html)),
- A working version of `pdflatex` (tested with `pi-2.6-x`)
- A working version of Julia,Octave or Matlab (depending on what you want to use),

I'm assuming that your `$PATH` variable has been updated accordingly so that you can call each of those with `gle`, `julia`, `octave` and `matlab`.

## Quick example

With `Julia` go to the `examples/julia` directory and run

```
../../s2g ex_basic.jl
```

With `Octave/Matlab` go to the `examples/octavematlab`

```
../../s2g ex_axis.m
```

It takes a few seconds to compile the figure since it must run `pdflatex` to generate the labels etc. Note that there is also an option without TeX to have a quick look at figures (or if your figure has no need for TeX): running `s2g` with option `-notex` or (equivalently) `-draft` will escape the TeX and just quickly compile the figure:

```
../../s2g ex_basic.jl -notex
```

If you want a png output, use the option `-png` eg:

```
../../s2g ex_basic.jl -notex -png
```

## Example in Julia

Here is a very simple example with Octave, in a file `smalltest.m` (already in `examples/octavematlab/`) write:

```
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

then in your terminal, in the same directory with `$PATHS2G` the path to the executable `s2g`,

```
$PATHS2G/s2g smalltest.m -png
```

which should generate the figure below:

![smalltest.m](/examples/octavematlab/smalltest_plot1_g.png)