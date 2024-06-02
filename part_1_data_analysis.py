from itertools import product

from bokeh.io import show
from bokeh.layouts import gridplot
from bokeh.models import (BasicTicker, ColumnDataSource, DataRange1d,
                          Grid, LassoSelectTool, LinearAxis, PanTool,
                          Plot, ResetTool, Scatter, WheelZoomTool)
from bokeh.sampledata.penguins import data
from bokeh.transform import factor_cmap
from bokeh.io import show
from bokeh.models import CustomJS, MultiChoice
import pandas as pd


def build_splom(prop, old_attrs, attrs):
    plots = []

    for i, (y, x) in enumerate(product(attrs, reversed(attrs))):
        
        N = len(attrs)
        xdrs = [DataRange1d(bounds=None) for _ in range(N)]
        ydrs = [DataRange1d(bounds=None) for _ in range(N)]
        p = Plot(x_range=xdrs[i%N], y_range=ydrs[i//N],
                background_fill_color="#fafafa",
                border_fill_color="white", width=200, height=200, min_border=5)

        if i % N == 0:  # first column
            p.min_border_left = p.min_border + 4
            p.width += 40
            yaxis = LinearAxis(axis_label=y)
            yaxis.major_label_orientation = "vertical"
            p.add_layout(yaxis, "left")
            yticker = yaxis.ticker
        else:
            yticker = BasicTicker()
        p.add_layout(Grid(dimension=1, ticker=yticker))

        if i >= N*(N-1):  # last row
            p.min_border_bottom = p.min_border + 40
            p.height += 40
            xaxis = LinearAxis(axis_label=x)
            p.add_layout(xaxis, "below")
            xticker = xaxis.ticker
        else:
            xticker = BasicTicker()
        p.add_layout(Grid(dimension=0, ticker=xticker))

        scatter = Scatter(x=x, y=y, fill_alpha=0.6, size=5, line_color=None,
                        fill_color=factor_cmap('rg_case', 'Category10_3', RG_CASES))
        r = p.add_glyph(source, scatter)
        p.x_range.renderers.append(r)
        p.y_range.renderers.append(r)

        # suppress the diagonal
        if (i%N) + (i//N) == N-1:
            r.visible = False
            p.grid.grid_line_color = None

        p.add_tools(PanTool(), WheelZoomTool(), ResetTool(), LassoSelectTool())

        plots.append(p)

    show(gridplot(plots, ncols=N))

df = pd.read_csv("./Gambling_data.csv", sep=";")


df['rg_case'] = df['rg_case'].astype('str')
RG_CASES = sorted(df['rg_case'].unique())

source = ColumnDataSource(data=df)



OPTIONS = list(df.columns)
multi_choice = MultiChoice(value=["rg_case", "year_of_birth"], options=OPTIONS)
multi_choice.js_on_change("value", CustomJS(code="""
    console.log('multi_choice: value=' + this.value, this.toString())
"""))
multi_choice.on_change("value", build_splom)

show(multi_choice)

