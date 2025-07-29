import cairo
from math import pi,tau

def draw_egg(egg,ctx:cairo.Context):
    match egg:
        case 0:
            ctx.move_to(0.25,0.25)
            ctx.line_to(0.75,0.75)
            ctx.move_to(0.75,0.25)
            ctx.line_to(0.25,0.75)
            ctx.stroke()
        case 1:
            ctx.arc(0.5,0.5,0.35,0,tau)
            ctx.fill()
        case default:
            pass

def draw_eggs(rows,cols,eggs,file_format='png',file_name="output"):
    assert len(eggs)==rows*cols

    # Set up the image surface (width, height)
    cell_width, cell_height = 64, 64
    width=cell_width*cols
    height=cell_height*rows

    if file_format == 'svg':
        # SVG surface for SVG output
        surface = cairo.SVGSurface(file_name+".svg", width, height)
    else:
        # PNG surface for PNG output (default)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    
    ctx = cairo.Context(surface)
    
    ctx.set_source_rgb(0,0,0)  # RGB for black
    ctx.rectangle(0, 0, width, height)  # Full canvas
    ctx.fill()
    
    ctx.set_line_width(0.2)
    ctx.scale(cell_width,cell_height)
    
    ctx.set_source_rgb(1, 1, 1)  # Set color for the circles (black)
    
    for idx,egg in enumerate(eggs):
        row,col=divmod(idx,cols)
        ctx.save()
        ctx.translate(col,row)
        draw_egg(egg,ctx)
        ctx.restore()

    # Save the output based on the chosen file format
    if file_format == 'svg':
        print(f"SVG saved as '{file_name}.svg'")
    else:
        surface.write_to_png(file_name+".png")
        print(f"PNG saved as '{file_name}.png'")

draw_eggs(3,5,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],file_format="svg",file_name="0009_001")
draw_eggs(3,5,[1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],file_format="svg",file_name="0009_002")
draw_eggs(3,5,[1,1,0,1,1,1,1,1,1,1,1,1,0,1,1],file_format="svg",file_name="0009_003")
draw_eggs(3,5,[1,1,1,1,1,0,1,1,1,0,1,1,1,1,1],file_format="svg",file_name="0009_004")
draw_eggs(3,5,[1,1,1,1,1,1,0,1,0,1,1,1,1,1,1],file_format="svg",file_name="0009_005")