# S2G syntax

## General remarks

### Do's and Don't
* Don't write multiple expressions on the same line, (some of it might work but don't assume it will) so this:
```Matlab
plot(x1,y1); hold on; plot(x2,y2);
```
should be written in three lines

* Writing things on multiple lines with `...` continuation is fine:
```Matlab
plot(x1,y1, ...
		'color','IndianRed',...
		'linewidth',2.0)
```


### Expression within s2g lines
Expressions to be evaluated within S2G display lines will be evaluated with the context-script and hence have to be valid within that script. For example in R this would be valid (the `ceiling(sqrt(N))` will be computed in R)
```R
N = 500
draw = rnorm(N)
hist(draw,'nbins',ceiling(sqrt(N)))
```

### Color options
Colors implemented include the usual Matlab short ones, RGB triplets, RGBA (with transparency) and X11/SVG names, syntax:
* short Matlab `...,'r',...` with one of `rgbcmyk`
* rgb triplet `...,'color',[0.8 0.7 0.5],...` (note: normalized RGB as in Matlab)
* rgba triplet `...,'color',[0.8 0.7 0.5 0.4],...` will use 40% transparency
* X11/SVG name `...,'color','cornflowerblue',...`
* X11/SVG name+transparency `...,'color','salmon','alpha',0.7,...`

this will be referred to in the sequel as "colorspec"

## 2D Plots

### Basic Syntax
#### PLOT
**Quick note for Matlab/Octave users**, noticeable differences:
- multi graphs not (yet) accepted (e.g., `plot(x1,y1,x2,y2)`),
- x11 colors implemented (e.g., `...,'colors','cornflowerblue'`)

Accepted format
```Matlab
plot(x,...)
plot(x,y,...)
```
where `...` goes for options, accepted options at the moment are:
- **line style**: `-` (line), `:` (dotted), `-.` (dashed-dotted), `--` (dashed),
- **marker symbols**: (after line style symbol if any) `+`, `o`, `*`, `x`, `s` (square), `^` (triangle),
- **line style+color**: append a color to one of the line style symbol so for example `-r` will produce a red line, basic colors are `r`, `g`, `b`,`c` (cyan), `m` (magenta), `y`, `k` (black), `w`,
- **color**: using the name `color` followed by a colorspec
- **line width**: using the name `linewidth` followed by a non-negative number (note that a bit of fiddling might be necessary to find the proper number, it does not exactly match Matlab's width),
- **marker size**: using the name `markersize` followed by a non-negative number, same remark applies,
- (!) **marker face color**: the color is ignored, it just acts as a switch and the color will be the same as that of the line

**Examples**:
```Matlab
plot(x,y,'-+r','linewidth',0.5)
plot(x,y,':','color','cornflowerblue')
```

### TITLE/[XY]LABELS
Valid format (identical for `[xy]label`):
```
title('some (tex) string',...)
```
where `...` goes for options, accepted option at the moment is:
- **font size**: using the name `fontsize` followed by an integer (points unit i.e., the standard one).

**Example**:
```Matlab
xlabel('time - [s]','fontsize',14)
```

#### LEGEND
Accepted format
```Matlab
legend('str1','str2',...)
```
where `...` goes for options, accepted options are:
- **location** using the name `location` followed by combined words like `southeast`, `northwest` etc. Shorts are accepted eg: `nw`.
- **box off** using the name `boxoff` will remove the legend bounding box.
- **offset** using the name `offset` followed by an array `[a b]` will offset the legend from the graph box by the specified offset.

#### HIST
Accepted format
```Matlab
hist(x,...)
```
where `...` goes for options, accepted options are:
- **number of bins** just an integer or the name `nbins` followed by an expression (e.g. in R `...,'nbins',ceiling(sqrt(N))+3,...`),
- **normalization** using the name `normalization` followed by one of `probability` (height=count/totcount), `pdf` (h=count/totcount*binwidth), `countdensity` (height=count/width) (default is just the count),
- **x range** using the name `from` followed by an expression and/or the name `to` followed by an expression, it overwrites the default range of bins (from `min(draw)` to `max(draw)`) this can be useful when comparing two histograms where one wants the bins to overlap.
- **face color** using the name `color` or `facecolor` followed by a colorspec
- **edge color** using the name `edgecolor` followed by a colorspec

#### BAR
- **bar width** using name `width` followed by number (interpreted in units of `xaxis`)
- **distance between x-ticks** using name `xdticks` followed by number
- **add first and last tick** using name `flticks`, adds ticks on both end of `xaxis`,
- **face color** using name `color` or `facecolor` followed by colorspec
- **edge color** using name `edgecolor` followed by colorspec

#### STEM

#### LOGLOG

#### SEMILOGX/Y

#### FILL

### Extra syntax
#### FILLBETWEEN

### Unstable / not available yet

- Plot::markerfacecolor
- Legend::offset (outside positions need fig resize)
- Hist::cumulative normalization not dealt with (eg: `...,'normalization','cdf'`)

## 3D Plots

### Not available yet

Everything, 3D plots have not yet been considered. Contours should come pretty quickly.
