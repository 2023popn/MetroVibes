import math
import pygame

def make_fillet(prev_point, corner, next_point, radius):
    """
    Make a rounded arc at `corner`, tangent to the segments prev->corner and corner->next.
    Returns (p1, p2): the tangent points where the straight segments should stop,
    so the caller can trim its straight lines instead of drawing all the way to `corner`.
    """
    cx, cy = corner
    px, py = prev_point
    nx, ny = next_point

    # direction vectors from corner toward each neighbor, normalized
    d1x, d1y = px - cx, py - cy
    d2x, d2y = nx - cx, ny - cy
    len1 = math.hypot(d1x, d1y)
    len2 = math.hypot(d2x, d2y)
    if len1 == 0 or len2 == 0:
        return corner, corner

    d1x, d1y = d1x / len1, d1y / len1
    d2x, d2y = d2x / len2, d2y / len2

    # interior angle at the corner
    dot = max(-1.0, min(1.0, d1x * d2x + d1y * d2y))
    alpha = math.acos(dot)

    if alpha > math.radians(179):  # nearly straight, no real corner to round
        return corner, corner

    # how far back along each segment the fillet starts (tangent length)
    tangent_len = radius / math.tan(alpha / 2)
    tangent_len = min(tangent_len, len1 * 0.5, len2 * 0.5)  # don't eat past segment midpoints
    actual_radius = tangent_len * math.tan(alpha / 2)

    p1 = (cx + d1x * tangent_len, cy + d1y * tangent_len)
    p2 = (cx + d2x * tangent_len, cy + d2y * tangent_len)

    # circle center lies along the angle bisector
    bx, by = d1x + d2x, d1y + d2y
    blen = math.hypot(bx, by)
    if blen == 0:
        return p1, p2
    bx, by = bx / blen, by / blen
    center_dist = actual_radius / math.sin(alpha / 2)
    center = (cx + bx * center_dist, cy + by * center_dist)

    # sweep the short way around from p1 to p2
    a1 = math.atan2(p1[1] - center[1], p1[0] - center[0])
    a2 = math.atan2(p2[1] - center[1], p2[0] - center[0])
    diff = (a2 - a1) % (2 * math.pi)
    if diff > math.pi:
        a1, a2 = a2, a1
        diff = 2 * math.pi - diff

    steps = max(4, int(diff / math.radians(8)))  # ~8° per segment, smooth enough at any radius
    arc_points = [
        (center[0] + actual_radius * math.cos(a1 + diff * i / steps),
         center[1] + actual_radius * math.sin(a1 + diff * i / steps))
        for i in range(steps + 1)
    ]

    # ensure the arc starts at p1 (tangent point on the incoming segment)
    # rather than trusting raw angle comparisons, which don't generalize
    # across corners in different screen quadrants
    dist_start_to_p1 = math.hypot(arc_points[0][0] - p1[0], arc_points[0][1] - p1[1])
    dist_start_to_p2 = math.hypot(arc_points[0][0] - p2[0], arc_points[0][1] - p2[1])
    if dist_start_to_p2 < dist_start_to_p1:
        arc_points.reverse()

    # pygame.draw.lines(screen, color, False, arc_points, thickness)
    return arc_points