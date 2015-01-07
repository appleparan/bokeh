""" This is the utils module that collects convenience functions and code that are
useful for charts ecosystem.
"""
#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2014, Continuum Analytics, Inc. All rights reserved.
#
# Powered by the Bokeh Development Team.
#
# The full license is in the file LICENCE.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from math import cos, sin
from ..document import Document
from ..session import Session
from ..embed import file_html
from ..resources import INLINE
from ..browserlib import view
from ..utils import publish_display_data
from ..models import Layout, List, Instance, Widget
from ..models import HBox as _HBox
from ..models import VBox as _VBox

#-----------------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------------


def polar_to_cartesian(r, start_angles, end_angles):
    """Translate polar coordinates to cartesian.

    Args:
    r (float): radial coordinate
    start_angles (list(float)): list of start angles
    end_angles (list(float)): list of end_angles angles

    Returns:
        x, y points
    """
    cartesian = lambda r, alpha: (r*cos(alpha), r*sin(alpha))
    points = []

    for start, end in zip(start_angles, end_angles):
        points.append(cartesian(r, (end + start)/2))

    return zip(*points)

class OverlayBox(object):
    def __init__(self, *charts, **kwargs):
        self.filename = kwargs.pop('filename', None)
        self.server = kwargs.pop('server', None)
        self.notebook = kwargs.pop('notebook', None)
        self.title = kwargs.pop('title', '')

        self.charts = charts

    def show(self):
        """Main show function.

        It shows the plot in file, server and notebook outputs.
        """
        # self.doc = Document()
        # self.doc.hold(True)
        # self.plot = None
        # xdr, ydr = None, None
        # _chart = None
        # for i, chart in enumerate(self.charts):
        #     chart.doc = self.doc
        #     if i>0:
        #         chart.xdr = xdr
        #         chart.ydr = ydr
        #
        #         chart.chart = _chart
        #         # self.create_chart()
        #         # we start the plot (adds axis, grids and tools)
        #         # self.start_plot()
        #         # we prepare values
        #         chart.prepare_values()
        #         # we get the data from the incoming input
        #         chart.get_data()
        #         # we filled the source and ranges with the calculated data
        #         chart.get_source()
        #         # we dynamically inject the source and ranges into the plot
        #         # self.add_data_plot()
        #         chart._palette = None
        #         # we add the glyphs into the plot
        #         chart.draw()
        #         # we pass info to build the legend
        #         # self.end_plot()
        #     else:
        #         xdr, ydr = chart.xdr, chart.ydr
        #
        #         chart._setup_show()
        #         chart._prepare_show()
        #         chart._show_teardown()
        #
        #         _chart = chart.chart
        #
        #     # self.doc.._current_plot = fig
        #     # curdoc().add(fig)
        #
        #     if not self.title:
        #         self.title = chart.chart.title
        #
        # print self.doc.context.children
        # print self.doc._current_plot.renderers

        self.doc = Document()
        self.doc.hold(True)
        self.plot = None
        xdr, ydr = None, None
        for i, chart in enumerate(self.charts):
            chart.doc = self.doc
            if i>0:
                chart.xdr = xdr
                chart.ydr = ydr
            else:
                xdr, ydr = chart.xdr, chart.ydr

            chart._setup_show()
            chart._prepare_show()
            chart._show_teardown()

            # self.doc.._current_plot = fig
            # curdoc().add(fig)

            if not self.title:
                self.title = chart.chart.title


        if self.filename:
            if self.filename is True:
                filename = "untitled"
            else:
                filename = self.filename
            with open(filename, "w") as f:
                f.write(file_html(self.doc, INLINE, self.title))
            print("Wrote %s" % filename)
            view(filename)
        elif self.filename is False and self.server is False and self.notebook is False:
            print("You have to provide a filename (filename='foo.html' or"
                  " .filename('foo.html')) to save your plot.")

        if self.server:
            self.session.store_document(self.doc)
            link = self.session.object_link(self.doc.context)
            view(link)

        if self.notebook:
            from bokeh.embed import notebook_div
            for plot in self._plots:
                publish_display_data({'text/html': notebook_div(plot)})


def VBox(*charts):
        #
        # self._filename = kwargs.pop('filename', None)
        # self._server = kwargs.pop('server', None)
        # self._notebook = kwargs.pop('notebook', None)

    # self.doc = Document()
    # self.doc.hold(True)
    plots = []
    xdr, ydr = None, None
    for i, chart in enumerate(charts):
        chart._setup_show()
        chart._prepare_show()
        chart._show_teardown()

        plots.append(chart.chart.plot)


    return _VBox(*plots)

def HBox(*charts):
        #
        # self._filename = kwargs.pop('filename', None)
        # self._server = kwargs.pop('server', None)
        # self._notebook = kwargs.pop('notebook', None)

    # self.doc = Document()
    # self.doc.hold(True)
    plots = []
    xdr, ydr = None, None
    for i, chart in enumerate(charts):
        chart._setup_show()
        chart._prepare_show()
        chart._show_teardown()

        plots.append(chart.chart.plot)


    return _HBox(*plots)

def show(obj=None, title='test', filename=False, server=False, notebook=False):
    """ 'shows' a plot object or the current plot, by auto-raising the window or tab
    displaying the current plot (for file/server output modes) or displaying
    it in an output cell (IPython notebook).

    Args:
        obj (Widget/Plot object, optional): it accepts a plot object and just shows it.

        browser (str, optional) : browser to show with (default: None)
            For systems that support it, the **browser** argument allows specifying
            which browser to display in, e.g. "safari", "firefox", "opera",
            "windows-default".  (See the webbrowser module documentation in the
            standard lib for more details.)

        new (str, optional) : new file output mode (default: "tab")
            For file-based output, opens or raises the browser window
            showing the current output file.  If **new** is 'tab', then
            opens a new tab. If **new** is 'window', then opens a new window.
    """
    if filename:
        if filename is True:
            filename = "untitled"
        else:
            filename = filename
        with open(filename, "w") as f:
            f.write(file_html(obj, INLINE, title))
        print("Wrote %s" % filename)
        view(filename)

    elif filename is False and server is False and notebook is False:
        print("You have to provide a filename (filename='foo.html' or"
              " .filename('foo.html')) to save your plot.")

    if server:
        obj.session.store_document(obj.doc)
        link = obj.session.object_link(obj.doc.context)
        view(link)

    if notebook:
        from bokeh.embed import notebook_div
        for plot in obj._plots:
            publish_display_data({'text/html': notebook_div(plot)})