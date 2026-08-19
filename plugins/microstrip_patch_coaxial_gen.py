import pcbnew
import math
from .sexpr import points_to_sexpr, pad_to_sexpr, corner_anchor


def generate_microstrip_coaxial_patch(name="PATCH_ANTENNA", patch_length=28.348, patch_width=28.348, ground_length=37.948, ground_width=37.948, feed_offset_x=0, feed_offset_y=7.286, pad_radius=2.143, hole_radius=0.635, clearance_radius=3.5, ground_check=True, mask_check=True):

    points_f = [
        pcbnew.VECTOR2I(-pcbnew.FromMM(patch_width / 2), -pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(patch_width / 2), -pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(patch_width / 2), pcbnew.FromMM(patch_length / 2)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(patch_width / 2), pcbnew.FromMM(patch_length / 2))
    ]

    circle = [
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_offset_x + clearance_radius * math.sin(2 * math.pi * i / 36)),
                        pcbnew.FromMM(feed_offset_y + clearance_radius * math.cos(2 * math.pi * i / 36)))
        for i in range(37)
    ]

    points_b = [
        pcbnew.VECTOR2I(-pcbnew.FromMM(ground_width / 2), -pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(ground_width / 2), -pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(ground_width / 2), pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_offset_x), pcbnew.FromMM(ground_length / 2)),
        *circle,
        pcbnew.VECTOR2I(pcbnew.FromMM(feed_offset_x), pcbnew.FromMM(ground_length / 2)),
        pcbnew.VECTOR2I(-pcbnew.FromMM(ground_width / 2), pcbnew.FromMM(ground_length / 2))
    ]

    pad_probe = f"(pad 1 thru_hole circle (at {feed_offset_x} {feed_offset_y}) (size {pad_radius * 2} {pad_radius * 2}) (drill {hole_radius * 2}) (layers *.Cu *.Mask))\n"
    pad_f = pad_to_sexpr(1, [points_f], (feed_offset_x, feed_offset_y), (pad_radius * 2, pad_radius * 2), "F.Cu", anchor="circle")
    pad_b = pad_to_sexpr(2, [points_b], *corner_anchor(points_b), "B.Cu")
    pad = pad_probe + pad_f + (pad_b if ground_check else "")

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
