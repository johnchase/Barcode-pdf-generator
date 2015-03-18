#!/usr/bin/env python
# File created on 14 Jun 2013
from __future__ import division

from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import os
from sys import exit
from os.path import exists
import pandas as pd
import numpy as np


def get_ids(input_fh):

    id_df = pd.read_csv(input_fh)
    id_list = id_df.ix[:, 0]

    return list(id_list)


def get_x_y_coordinates(columns, rows, x_start, y_start):

    x_coords = np.arange(x_start, (columns*2.2), 2.2)
    y_coords = np.arange(y_start, (y_start - (rows*1.21)), -1.21)

    xy_coords = []
    for x_coord in x_coords:
        for y_coord in y_coords:
            xy_coords.append((x_coord*inch, y_coord*inch))

    return xy_coords


def get_barcodes(input_fh,
                 output_fp,
                 columns=4,
                 rows=9,
                 x_start = 0,
                 y_start = 10):

    barcode_ids = get_ids(input_fh)

    barcode_canvas = canvas.Canvas(output_fp, pagesize=letter)

    xy_coords = get_x_y_coordinates(columns, rows, x_start, y_start)

    c = 0
    for barcode_id in barcode_ids:
        new_record = barcode_id[:]
        sample_id = new_record[0]
        x = xy_coords[c][0]
        y = xy_coords[c][1]
        # Create the barcodes and sample_id text and draw them on the canvas
        barcode = code128.Code128(sample_id, barWidth=0.009*inch,
                                  barHeight=0.4*inch)
        barcode.drawOn(barcode_canvas, x, y)
        # the offset for the text will change automatically as x and y
        # coordinates are
        # changed therefore the the following values do not need to be changed.
        barcode_canvas.drawString((x + .47 * inch), (y - .15 * inch),
                                  sample_id)
        if c < ((rows*columns) - 1):
            c += 1
        else:
            c = 0
            barcode_canvas.showPage()
    barcode_canvas.save()