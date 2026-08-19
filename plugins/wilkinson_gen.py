import pcbnew
from .sexpr import points_to_sexpr, pad_to_sexpr, corner_anchor


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

    input_pad = pad_to_sexpr(1, [points_input, points_arc_left, points_arc_right], (-arc_radius-arc_width-input_length/2, 0), (input_length, input_width), "F.Cu")
    output_pad_left = pad_to_sexpr(2, [points_output_left], (arc_radius+arc_width+output_length/2, -input_width/2-output_width/2), (output_length, output_width), "F.Cu")
    output_pad_right = pad_to_sexpr(3, [points_output_right], (arc_radius+arc_width+output_length/2, input_width/2+output_width/2), (output_length, output_width), "F.Cu")
    ground_pad = pad_to_sexpr(4, [points_ground], *corner_anchor(points_ground), "B.Cu")
    pads = input_pad + output_pad_left + output_pad_right + (ground_pad if ground_check else "")

    poly_mask_left = points_to_sexpr(points_mask_left, "F.Mask")
    poly_mask_right = points_to_sexpr(points_mask_right, "F.Mask")
    poly = poly_mask_left + poly_mask_right if mask_check else ""

    template = f"""
                (module {name} (layer F.Cu)
                (net_tie_pad_groups "1,2,3")
                (fp_text reference REF** (at 0 0) (layer F.SilkS))
                (fp_text value {name} (at 0 -2) (layer F.Fab))
                {poly}
                {pads}
                )
                """

    return template
