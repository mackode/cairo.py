#!/usr/bin/env python3

import cairo

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200)
context = cairo.Context(surface)

context.set_line_width(12)
context.set_source_rgb(1., .75, 0.)

context.move_to(0, 100)
context.line_to(100, 100)
context.stroke()

surface.flush()
surface.write_to_png("line.png")