# S2G syntax

## 2D Plots

### Basic Syntax
#### PLOT
**Quick note for Matlab/Octave users**, noticeable differences:
- multi graphs not accepted (e.g., `plot(x1,y1,x2,y2)`),
- x11 colors implemented (e.g., `...,'colors','cornflowerblue'`)

Accepted format
```Matlab
plot(x,...)
plot(x,y,...)
```
where `...` goes for options, accepted options are:
- **line style**: `-` (line), `:` (dotted), `-.` (dashed-dotted), `--` (dashed),
- **marker symbols**: (after line style symbol if any) `+`, `o`, `*`, `x`, `s` (square), `^` (triangle),
- **line style+color**: append a color to one of the line style symbol so for example `-r` will produce a red line, basic colors are `r`, `g`, `b`,`c` (cyan), `m` (magenta), `y`, `k` (black), `w`,
- **color**: using the name `color` followed by either a normalized RGB triplet (eg: `...,'color',[0.1 0.5 0.7],...`) or an X11 name (eg: `...,'color','salmon',...)
- **line width**: using the name `linewidth` followed by a non-negative number (note that a bit of fiddling might be necessary to find the proper number, it does not exactly match Matlab's width),
- **marker size**: using the name `markersize` followed by a non-negative number, same remark applies,
- (!) **marker face color**: the color is ignored, it just acts as a switch and the color will be the same as that of the line

**Examples**:
```Matlab
plot(x,y,'-+r','linewidth',0.5)
plot(x,y,':','color','cornflowerblue')
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
- **number of bins** just an integer or the name `nbins` followed by an integer,
- **normalization** using the name `normalization` followed by one of `probability` (height=count/totcount), `pdf` (h=count/totcount*binwidth), `countdensity` (height=count/width) (default is just the count),
- **face color** using the name `color` or `facecolor` followed by a matlab short (`rgbmc...`) or an X11 name or an RGB triplet or an RGBA (with transparency eg `[0.1 0.5 0.7 0.3]` will have alpha set to 30%). An alternative for transparency is to use an X11 name followed by `alpha` and a number between 0 and 1 e.g.: `...,'facecolor','cornflowerblue','alpha',0.7,...`.
- **edge color** using the name `edgecolor` followed by a matlab short or an X11 name or an RGB triplet

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