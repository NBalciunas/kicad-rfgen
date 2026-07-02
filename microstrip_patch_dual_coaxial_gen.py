import pcbnew
import math


def points_to_sexpr(points, layer):
    pts = " ".join([f"(xy {p.x / 1e6:.6f} {p.y / 1e6:.6f})" for p in points])
    return f"(fp_poly (pts {pts}) (layer {layer}) (width 0) (fill solid))\n"


def generate_microstrip_dual_coaxial_patch(name="PATCH_ANTENNA", patch_length=15, patch_width=20, ground_length=24.6, ground_width=29.6, feed_offset_x_a=0, feed_offset_y_a=2.9, feed_offset_x_b=2.9, feed_offset_y_b=0, pad_radius=1.4, hole_radius=0.65, clearance_radius=2.5, ground_check=True, mask_check=True):

    points_f = [
        pcbnew.VECTOR2I(-pcbnew.FromMM(patch_width / 2), -pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(patch_width / 2), -pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(patch_width / 2), pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(patch_width / 2), pcbnew.FromMM(patch_length / 2))
    ]

    def slit_circle(fx, fy):
        circle = [
            pcbnew.VECTOR2I(pcbnew.FromMM(fx + clearance_radius * math.sin(2 * math.pi * i / 36)),
                            pcbnew.FromMM(fy + clearance_radius * math.cos(2 * math.pi * i / 36)))
            for i in range(37)
        ]
        return [
            pcbnew.VECTOR2I(pcbnew.FromMM(fx), pcbnew.FromMM(ground_length / 2)),
            *circle,
            pcbnew.VECTOR2I(pcbnew.FromMM(fx), pcbnew.FromMM(ground_length / 2))
        ]

    feed_a, feed_b = sorted([(feed_offset_x_a, feed_offset_y_a), (feed_offset_x_b, feed_offset_y_b)], key=lambda f: -f[0])

    points_b = [
        pcbnew.VECTOR2I(-pcbnew.FromMM(ground_width / 2), -pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(ground_width / 2), -pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(ground_width / 2), pcbnew.FromMM(ground_length / 2)),
        *slit_circle(*feed_a),
        *slit_circle(*feed_b),
        pcbnew.VECTOR2I(-pcbnew.FromMM(ground_width / 2), pcbnew.FromMM(ground_length / 2))
    ]

    poly_f = points_to_sexpr(points_f, "F.Cu")
    poly_b = points_to_sexpr(points_b, "B.Cu")
    poly_fm = points_to_sexpr(points_f, "F.Mask")
    poly_bm = points_to_sexpr(points_b, "B.Mask")
    poly_copper = poly_f + poly_b if ground_check else poly_f
    poly_mask = poly_fm + poly_bm if ground_check else poly_fm
    poly = poly_copper + poly_mask if mask_check else poly_copper

    pads = (f"(pad 1 thru_hole circle (at {feed_offset_x_a} {feed_offset_y_a}) (size {pad_radius * 2} {pad_radius * 2}) (drill {hole_radius * 2}) (layers *.Cu *.Mask))\n"
            f"(pad 2 thru_hole circle (at {feed_offset_x_b} {feed_offset_y_b}) (size {pad_radius * 2} {pad_radius * 2}) (drill {hole_radius * 2}) (layers *.Cu *.Mask))\n")

    template = f"""
                (module {name} (layer F.Cu)
                (fp_text reference REF** (at 0 0) (layer F.SilkS))
                (fp_text value {name} (at 0 -2) (layer F.Fab))
                {poly}
                {pads}
                )
                """

    return template
