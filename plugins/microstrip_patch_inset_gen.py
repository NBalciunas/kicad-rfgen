import pcbnew
from .sexpr import points_to_sexpr, pad_to_sexpr, corner_anchor


def generate_microstrip_inset_patch(name="PATCH_ANTENNA", patch_length=15, patch_width=20, ground_length=24.6, ground_width=29.6, feed_width=3, inset_gap=1, inset_distance=5, ground_check=True, mask_check=True):

    points_f = [
        pcbnew.VECTOR2I(-pcbnew.FromMM(patch_width / 2), -pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(patch_width / 2), -pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(patch_width / 2), pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_width / 2 + inset_gap), pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_width / 2 + inset_gap), pcbnew.FromMM(patch_length / 2 - inset_distance)),
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_width / 2), pcbnew.FromMM(patch_length / 2 - inset_distance)),
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_width / 2), pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(feed_width / 2), pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(feed_width / 2), pcbnew.FromMM(patch_length / 2 - inset_distance)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(feed_width / 2 + inset_gap), pcbnew.FromMM(patch_length / 2 - inset_distance)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(feed_width / 2 + inset_gap), pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(patch_width / 2), pcbnew.FromMM(patch_length / 2))
    ]

    points_b = [
        pcbnew.VECTOR2I(-pcbnew.FromMM(ground_width / 2), -pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(ground_width / 2), -pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(ground_width / 2), pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(ground_width / 2), pcbnew.FromMM(ground_length / 2))
    ]

    pad_f = pad_to_sexpr(1, [points_f], (0, ground_length / 2 - feed_width / 2), (feed_width, feed_width), "F.Cu")
    pad_b = pad_to_sexpr(2, [points_b], *corner_anchor(points_b), "B.Cu")
    pad = pad_f + pad_b if ground_check else pad_f

    poly_fm = points_to_sexpr(points_f, "F.Mask")
    poly_bm = points_to_sexpr(points_b, "B.Mask")
    poly_mask = poly_fm + poly_bm if ground_check else poly_fm
    poly = poly_mask if mask_check else ""

    template = f"""
                (module {name} (layer F.Cu)
                (fp_text reference REF** (at 0 0) (layer F.SilkS))
                (fp_text value {name} (at 0 -2) (layer F.Fab))
                {poly}
                {pad}
                )
                """

    return template
