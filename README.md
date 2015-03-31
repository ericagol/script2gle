# tex2jem

## Warning

This project is still under (rather heavy but infrequent) development.

## What this is about

The rough idea is to use `Matlab/Octave` style syntax for plots whilst generating GLE ([Graphics Layout Engine](http://glx.sourceforge.net/index.html)) code in the background to output paper-quality graphs. The advantage of using GLE it supports the use of LaTeX very easily (cf. example).

Roughly, the workflow is as follows:

1. "Parse" the script (.jl or .m),
2. Remove the lines where plotting is done following `Matlab/Octave` syntax and write it in corresponding `.gle` code, replace these lines by `write` lines (`.dat` output),
3. Run the script, `.dat` files are generated,
4. Run GLE, `.pdf` or `.png` files are generated.

## Requirements

- A working version of `Python 2.x` (tested with `2.7.6`),
- A working version of GLE ([Link](http://glx.sourceforge.net/index.html)),
- A working version of `pdflatex` (tested with `pi-2.6-x`)
- A working version of Julia,Octave or Matlab (depending on what you want),

I'm assuming that your `$PATH` variable has been updated accordingly so that you can call each of those with `gle`, `julia`, `octave` and `matlab`.

## Example

With `Julia` go to the `examples` directory and run

```
../s2g ex_basic.jl
```

It takes a few seconds to compile the figure since it must run `pdflatex`, there is also an option to have a quick look at figures and not compile the LaTeX: running `s2g` with option `-notex` or (equivalently) `-draft` will escape the TeX and just quickly compile the figure:

```
../s2g ex_basic.jl -notex
```

If you want a png output, use the option `-png` eg:

```
../s2g ex_basic.jl -notex -png
```