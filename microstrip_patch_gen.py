import pcbnew


def points_to_sexpr(points, layer):
    pts = " ".join([f"(xy {p.x / 1e6:.6f} {p.y / 1e6:.6f})" for p in points])
    return f"(fp_poly (pts {pts}) (layer {layer}) (width 0) (fill solid))\n"


def generate_microstrip_patch(name="PATCH_ANTENNA", patch_length=15, patch_width=20, feed_length=5, feed_width=3,
                              inset_gap=1, inset_distance_input=5, ground_check=True, mask_check=True):
    points_f = [
        pcbnew.VECTOR2I(-pcbnew.FromMM(patch_width / 2), -pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(patch_width / 2), -pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(patch_width / 2), pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_width / 2 + inset_gap), pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_width / 2 + inset_gap),
                        pcbnew.FromMM(patch_length / 2 - inset_distance_input)),
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_width / 2), pcbnew.FromMM(patch_length / 2 - inset_distance_input)),
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_width / 2), pcbnew.FromMM(patch_length / 2 + feed_length)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(feed_width / 2), pcbnew.FromMM(patch_length / 2 + feed_length)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(feed_width / 2), pcbnew.FromMM(patch_length / 2 - inset_distance_input)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(feed_width / 2 + inset_gap),
                        pcbnew.FromMM(patch_length / 2 - inset_distance_input)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(feed_width / 2 + inset_gap), pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(patch_width / 2), pcbnew.FromMM(patch_length / 2))
    ]

    points_b = [
        pcbnew.VECTOR2I(-pcbnew.FromMM(patch_width / 2), -pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(patch_width / 2), -pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(patch_width / 2), pcbnew.FromMM(patch_length / 2 + feed_length)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(patch_width / 2), pcbnew.FromMM(patch_length / 2 + feed_length))
    ]

    poly_f = points_to_sexpr(points_f, "F.Cu")
    poly_b = points_to_sexpr(points_b, "B.Cu")
    poly_fm = points_to_sexpr(points_f, "F.Mask")
    poly_bm = points_to_sexpr(points_b, "B.Mask")
    poly_copper = poly_f + poly_b if ground_check else poly_f
    poly_mask = poly_fm + poly_bm if ground_check else poly_fm
    poly = poly_copper + poly_mask if mask_check else poly_copper

    pad = f"(pad 1 smd rect (at 0 {patch_length/2+feed_length-feed_width/2}) (size {feed_width} {feed_width}) (layers F.Cu))\n"

    template = f"""
                (module {name} (layer F.Cu)
                (fp_text reference REF** (at 0 0) (layer F.SilkS))
                (fp_text value {name} (at 0 -2) (layer F.Fab))
                {poly}
                {pad}
                )
                """

    return template
