def _pts(points, offset_x=0.0, offset_y=0.0):
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
                    f"(arc (start {start.x/1e6 - offset_x:.6f} {start.y/1e6 - offset_y:.6f})"
                    f" (mid {mid.x/1e6 - offset_x:.6f} {mid.y/1e6 - offset_y:.6f})"
                    f" (end {end.x/1e6 - offset_x:.6f} {end.y/1e6 - offset_y:.6f}))"
                )
                mode = None
            continue
        pts.append(f"(xy {point.x/1e6 - offset_x:.6f} {point.y/1e6 - offset_y:.6f})")
    return " ".join(pts)


def points_to_sexpr(points, layer):
    return f"(fp_poly (pts {_pts(points)}) (layer {layer}) (width 0) (fill solid))\n"


def pad_to_sexpr(number, polys, at, size, layers, anchor="rect"):
    x, y = at
    primitives = "".join(f"(gr_poly (pts {_pts(poly, x, y)}) (width 0) (fill yes))" for poly in polys)
    return (f"(pad {number} smd custom (at {x:.6f} {y:.6f}) (size {size[0]:.6f} {size[1]:.6f}) (layers {layers})"
            f"(options (clearance outline) (anchor {anchor}))"
            f"(primitives {primitives}))\n")


def corner_anchor(points, size=0.5):
    x = min(p.x for p in points) / 1e6 + size / 2
    y = min(p.y for p in points) / 1e6 + size / 2
    return (x, y), (size, size)
