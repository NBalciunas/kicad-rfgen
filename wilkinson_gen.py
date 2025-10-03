import pcbnew

def points_to_sexpr(points, layer):
    pts = []
    mode = None
    buf = []
    for point in points:
        if isinstance(point, str) and point.lower() == "arc_start":
            mode = "arc"
            buf = []
            continue
        if mode == "arc":
            buf.append(point)
            if len(buf) == 3:
                start, mid, end = buf
                pts.append(
                    f"(arc (start {start.x/1e6:.6f} {start.y/1e6:.6f}) (mid {mid.x/1e6:.6f} {mid.y/1e6:.6f}) (end {end.x/1e6:.6f} {end.y/1e6:.6f}))"
                )
                mode = None
            continue
        pts.append(f"(xy {point.x/1e6:.6f} {point.y/1e6:.6f})")
    return f"(fp_poly (pts {' '.join(pts)}) (layer {layer}) (width 0) (fill solid))\n"

def generate_wilkinson(name="WILKINSON", input_length=4, input_width=5, output_length=8, output_width=4, arc_radius=5, arc_width=4, ground_check=True, mask_check=True):
    points_input = [
        pcbnew.VECTOR2I(pcbnew.FromMM(-arc_radius-arc_width-input_length), pcbnew.FromMM(-input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(-arc_radius-arc_width-input_length), pcbnew.FromMM(input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(-arc_radius), pcbnew.FromMM(input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(-arc_radius), pcbnew.FromMM(-input_width/2))
    ]

    points_arc_left = [
        "arc_start",
        pcbnew.VECTOR2I(pcbnew.FromMM(-arc_radius), pcbnew.FromMM(-input_width/2)),  # start
        pcbnew.VECTOR2I(pcbnew.FromMM(0), pcbnew.FromMM(-input_width/2-arc_radius)),  # mid
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius), pcbnew.FromMM(-input_width/2)),  # end
        "arc_start",
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width), pcbnew.FromMM(-input_width/2)),  # start
        pcbnew.VECTOR2I(pcbnew.FromMM(0), pcbnew.FromMM(-input_width/2-arc_radius-arc_width)),  # mid
        pcbnew.VECTOR2I(pcbnew.FromMM(-arc_radius-arc_width), pcbnew.FromMM(-input_width/2))  # end
    ]

    points_arc_right = [
        "arc_start",
        pcbnew.VECTOR2I(pcbnew.FromMM(-arc_radius), pcbnew.FromMM(input_width/2)),  # start
        pcbnew.VECTOR2I(pcbnew.FromMM(0), pcbnew.FromMM(input_width/2+arc_radius)),  # mid
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius), pcbnew.FromMM(input_width/2)),  # end
        "arc_start",
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width), pcbnew.FromMM(input_width/2)),  # start
        pcbnew.VECTOR2I(pcbnew.FromMM(0), pcbnew.FromMM(+input_width/2+arc_radius+arc_width)),  # mid
        pcbnew.VECTOR2I(pcbnew.FromMM(-arc_radius-arc_width), pcbnew.FromMM(input_width/2))  # end
    ]

    points_output_left = [
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius), pcbnew.FromMM(-input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width+output_length), pcbnew.FromMM(-input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width+output_length), pcbnew.FromMM(-input_width/2-output_width)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius), pcbnew.FromMM(-input_width/2-output_width))
    ]

    points_output_right = [
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius), pcbnew.FromMM(input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width+output_length), pcbnew.FromMM(input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width+output_length), pcbnew.FromMM(input_width/2+output_width)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius), pcbnew.FromMM(input_width/2+output_width)),
    ]

    points_ground = [
        pcbnew.VECTOR2I(pcbnew.FromMM(-arc_radius-arc_width-input_length), pcbnew.FromMM(-input_width/2-arc_radius-arc_width)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width+output_length), pcbnew.FromMM(-input_width/2-arc_radius-arc_width)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width+output_length), pcbnew.FromMM(input_width/2+arc_radius+arc_width)),
        pcbnew.VECTOR2I(pcbnew.FromMM(-arc_radius-arc_width-input_length), pcbnew.FromMM(input_width/2+arc_radius+arc_width)),
    ]

    points_mask_left = [
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius), pcbnew.FromMM(-input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width), pcbnew.FromMM(-input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width), pcbnew.FromMM(-input_width/2-output_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius), pcbnew.FromMM(-input_width/2-output_width/2))
    ]

    points_mask_right = [
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius), pcbnew.FromMM(input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width), pcbnew.FromMM(input_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius+arc_width), pcbnew.FromMM(input_width/2+output_width/2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(arc_radius), pcbnew.FromMM(input_width/2+output_width/2)),
    ]

    winput = points_to_sexpr(points_input, "F.Cu")
    arc_left = points_to_sexpr(points_arc_left, "F.Cu")
    arc_right = points_to_sexpr(points_arc_right, "F.Cu")
    w_output_left = points_to_sexpr(points_output_left, "F.Cu")
    w_output_right = points_to_sexpr(points_output_right, "F.Cu")
    poly_f = winput + arc_left + arc_right + w_output_left + w_output_right

    poly_b = points_to_sexpr(points_ground, "B.Cu")
    poly_copper = poly_f + poly_b if ground_check else poly_f

    poly_mask_left = points_to_sexpr(points_mask_left, "F.Mask")
    poly_mask_right = points_to_sexpr(points_mask_right, "F.Mask")
    poly_mask = poly_mask_left + poly_mask_right

    poly = poly_copper + poly_mask if mask_check else poly_copper

    input_pad = f"(pad 1 smd rect (at {-arc_radius-arc_width-input_length/2} 0) (size {input_length} {input_width}) (layers F.Cu))\n"
    output_pad_left = f"(pad 2 smd rect (at {arc_radius+arc_width+output_length/2} {-input_width/2-output_width/2}) (size {output_length} {output_width}) (layers F.Cu))\n"
    output_pad_right = f"(pad 3 smd rect (at {arc_radius+arc_width+output_length/2} {input_width/2+output_width/2}) (size {output_length} {output_width}) (layers F.Cu))\n"
    pads = input_pad + output_pad_left + output_pad_right

    template = f"""
                (module {name} (layer F.Cu)
                (fp_text reference REF** (at 0 0) (layer F.SilkS))
                (fp_text value {name} (at 0 -2) (layer F.Fab))
                {poly}
                {pads}
                )
                """

    return template
