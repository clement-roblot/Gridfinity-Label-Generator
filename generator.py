#!/usr/bin/env python3
import cairo
import cairosvg

labelWidth = 370
labelHeight = 120



def addBorder(context, strokeSize = 0.01, margin = 0.05):
    # Add border to the label
    context.set_source_rgba(0, 0, 0, 1)
    context.set_line_width(strokeSize)
    context.move_to(margin, margin)
    context.line_to(1 - margin, margin)
    context.line_to(1 - margin, 1 - margin)
    context.line_to(margin, 1 - margin)
    context.line_to(margin, margin)
    context.stroke()


def generateLabel():


    # label dimentions: 37mm by 12mm
    with cairo.SVGSurface("label.svg", labelWidth, labelHeight) as surface:
        context = cairo.Context(surface)
        context.scale(labelWidth, labelHeight)

        addBorder(context)

        # context.set_source_rgba(0, 0, 0, 1)
        # context.set_line_width(0.05)
        # context.move_to(0, 0)
        # context.line_to(0.9, 0.9)
        # context.stroke()
    
    # cairosvg.svg2png(url="label.svg", write_to="label.png", output_width=labelWidth)


if __name__ == '__main__':

    generateLabel()
    print("Done")
