# svgdatashapes

SVGdatashapes.py is a compact set of python functions for creating many types of plots and data displays in SVG for use in web pages. 

Full info:  https://pepprseed.github.io/svgdatashapes/

General purpose, useful in areas such as biomedical, scientific, business, process monitoring, report generation. 
Plenty of control over legends, tooltips, colors, transparency, and many other appearance details. 
It has no package dependencies, and can work nicely in frameworks such as Flask and Bootstrap. 
No javascript, CSS, DOM, or SVG knowledge is required. 

Produce many types of bargraphs, lineplots, curves, bands, scatterplots, pie graphs, heatmaps, boxplots,
histograms, multipanel displays, 
and other data displays like windbarbs and Secchi depth graphs.  Plot from your numeric, categorical, or date/time data.

SVGdatashapes produces attractive results for many typical straightforward graphing / data display needs, as can be seen 
in the examples. The approach is procedural and the code is relatively simple and agile (click on examples to see code). 
It supports some basic 'reactive' things: tooltips, clickthru, hyperlinks, element hide/show with js. It does some basic 
stat / computational things: data ranges, frequency distributions, mean and SD, quartiles for boxplots. 

SVGdatashapes renders its results in SVG. All modern web browsers support viewing and printing of SVG graphics.
SVG is a good format for web-based data displays and line art because it's vector-based and has full support for 
good fonts, text in any direction, transparency, as well as tooltip and hyperlink support. SVG can share CSS styling 
from the host web page and can use the full range of html special characters to get Greek letters, etc. 
(SVGdatashapes also supports <sup> and <sub> for superscripts and subscripts).

You can include a chunk of SVG code directly into your html (referred to as an "inline SVG"). Or, you can put the SVG in 
a separate file and reference it using an <img> tag. (We do it both ways on the above web site.) 




