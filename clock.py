#!/usr/bin/env python3

import math
import time
import cairo

def draw_hand(hand_angle, hand_length):
    x1 = hand_width / 2 * -math.cos(hand_angle)
    y1 = hand_width / 2 * -math.sin(hand_angle)
    x2 = x1 + hand_length * math.sin(hand_angle)
    y2 = y1 - hand_length * math.cos(hand_angle)
    xc = hand_length * math.sin(hand_angle)
    yc = hand_length * -math.cos(hand_angle)

    context.move_to(x1, y1)
    context.line_to(x2, y2)
    context.arc(xc, yc, hand_width / 2, hand_angle - math.pi, hand_angle)
    context.line_to(-x1, -y1)
    context.close_path()
    context.fill()

IMAGE_WIDTH = 300
IMAGE_HEIGHT = 300

MARK_WIDTH = 1
MAJOR_MARK_WIDTH = 3

NUMERAL_STRINGS = ('12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11')

clock_diameter = min(IMAGE_WIDTH, IMAGE_HEIGHT)
clock_radius = clock_diameter / 2

surface = cairo.ImageSurface(cairo.Format.ARGB32, IMAGE_WIDTH, IMAGE_HEIGHT)
context = cairo.Context(surface)

context.translate((IMAGE_WIDTH - clock_diameter) / 2, (IMAGE_HEIGHT - clock_diameter) / 2)

context.set_source_rgb(1, 1, 1)
context.arc(clock_radius, clock_radius, clock_radius, 0, 2 * math.pi)
context.fill()

bezel_width = clock_diameter / 12
bezel_radius = clock_radius - bezel_width / 2

context.set_source_rgb(0, 0, 0)
context.set_line_width(bezel_width)
context.arc(clock_radius, clock_radius, bezel_radius, 0, 2 * math.pi)
context.stroke()

bezel_to_marks_gap = clock_radius / 15
mark_length = clock_radius / 10
mark_start_distance = clock_radius - bezel_width - bezel_to_marks_gap
mark_end_distance = mark_start_distance - mark_length

context.translate(clock_radius, clock_radius)

context.set_line_width(MARK_WIDTH)
context.arc(0, 0, mark_start_distance, 0, 2 * math.pi)
context.stroke()

context.arc(0, 0, mark_end_distance, 0, 2 * math.pi)
context.stroke()

for i in range(60):
    angle = 2 * math.pi * i / 60
    if i % 5 == 0:
        context.set_line_width(MAJOR_MARK_WIDTH)
    else:
        context.set_line_width(MARK_WIDTH)

    context.move_to(mark_start_distance * math.sin(angle), -mark_start_distance * math.cos(angle))
    context.line_to(mark_end_distance * math.sin(angle), -mark_end_distance * math.cos(angle))
    context.stroke()

marks_to_numerals_gap = clock_radius / 15
numeral_size = clock_radius / 5
numeral_distance = mark_end_distance - marks_to_numerals_gap

context.select_font_face("serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
context.set_font_size(numeral_size)

for i in range(12):
    angle = 2 * math.pi * i / 12
    x_multiplier = math.sin(angle)
    y_multiplier = -math.cos(angle)

    extents = context.text_extents(NUMERAL_STRINGS[i])

    text_x = numeral_distance * x_multiplier + extents.x_bearing * x_multiplier - extents.width / 2 * x_multiplier - extents.width / 2
    text_y = numeral_distance * y_multiplier + extents.y_bearing * y_multiplier + extents.height / 2 * y_multiplier + extents.height / 2

    context.move_to(text_x, text_y)
    context.show_text(NUMERAL_STRINGS[i])
    context.fill()

hand_width = clock_radius / 20

hour_hand_length = clock_radius / 3
minute_hand_length = clock_radius / 2
second_hand_length = clock_radius * 5 / 8

current_time = time.localtime()

second_hand_angle = 2 * math.pi * current_time.tm_sec / 60
minute_hand_angle = 2 * math.pi * (current_time.tm_min + current_time.tm_sec / 60) / 60
hour_hand_angle = 2 * math.pi * ((current_time.tm_hour % 12) + current_time.tm_min / 60) / 12

draw_hand(hour_hand_angle, hour_hand_length)
draw_hand(minute_hand_angle, minute_hand_length)
draw_hand(second_hand_angle, second_hand_length)

context.arc(0, 0, hand_width / 2, 0, 2 * math.pi)
context.fill()

surface.flush()
surface.write_to_png("clock.png")