
### GitHub Copilot Python Exploration

# Graph Exploration

This was a somewhat interesting day experiment. 
There was a bunch of very nearby construction noise to ignore while I was working on it, and Copilot was not tremendously helpful. 

I did not find a way to easily update the graph graphics with a single method call, 
and fully re-generating the graph results in an blank and flicker that has multiple
stages of layout adjustment.

There are surely better ways to handle the graph re-generation in Python, and 
other programming languages likely have better coordination between the graphics 
code and user interface configuration.

It did seem that the multi-y-axis feature was built into matplotlib. 
This example was the source for most of developing that capability: 
https://matplotlib.org/stable/gallery/spines/multiple_yaxis_with_spines.html .

The 'TkAgg' seems like a non-standard way to implement a graph plot, 
there is no copyright type date information on the pythonprogramming.net 
tutorial website to reference with Python versions.

The documentation for Python was a bit terse and unfamiliar,
the Visual Studio Code pop-up intellisense was a bit lacking. 
It was a rough day of coding.

Run 'python multi-y-axis-graph-window.py' to see where the exploration went.