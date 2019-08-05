class ObjectMap():
    def __init__(self, viewpoint, direction, x_area, y_area, screen_distance):
        self.view = viewpoint
        self.direction = direction
        self.x_area = x_area
        self.y_area = y_area
        self.dist = screen_distance
        self.objects = []

class PixelRaster():
    def __init__(self, x_area, y_area, max_view=999999999.0):
        self.raster = []
        for num in range(y_area):
            line = []
            for num in range(x_area):
                line.append(((0,0,0), max_view))
            self.raster.append(line)
        
    def z_buffer_polygon(*args):
        pass


def pixel_path(point_a, point_b):
    point_a = list(point_a)
    point_b = list(point_b)
    print(point_a, point_b)
    if point_a == point_b:
        return point_a
    x_delta = point_a[0] - point_b[0]
    y_delta = point_a[1] - point_b[1]
    total_steps = abs(x_delta) + abs(y_delta)
    if abs(x_delta) < abs(y_delta):
        lesser = 'x'
        l_val = x_delta
        g_val = y_delta
    else:
        lesser = 'y'
        l_val = y_delta
        g_val = x_delta
    if l_val == 0:
        base = int(g_val)
        extra = 0
        m_steps = abs(g_val) + 1
    else:
        base = int(abs(g_val))//int(abs(l_val))
        extra = abs(g_val)%abs(l_val)
        if extra > 0:
            m_steps = abs(l_val)//extra
        else:
            m_steps = abs(g_val) + 1
    target_pixel = point_b
    steps_to_go = total_steps
    if l_val != 0:
        x_c = x_delta/abs(x_delta)
        y_c = y_delta/abs(y_delta)
    elif lesser != 'x':
        x_c = x_delta/abs(x_delta)
        y_c = 1
    else:
        y_c = y_delta/abs(y_delta)
        x_c = 1
    x_c = int(x_c)
    y_c = int(y_c)
    pixels = []
    r_c = (point_a[2] - point_b[2])/total_steps
    y_steps = 0
    x_steps = 0
    while steps_to_go > 0:
        if lesser == 'y':
            for num in range(base):
                target_pixel[0] += x_c
                target_pixel[2] += r_c
                x_steps += 1
                pixels.append(tuple(target_pixel))
                steps_to_go -= 1
            if y_steps%m_steps == 0 and extra > 0:
                extra -= 1
                target_pixel[0] += x_c
                target_pixel[2] += r_c
                x_steps += 1
                pixels.append(tuple(target_pixel))
                steps_to_go -= 1
            target_pixel[1] += y_c
            target_pixel[2] += r_c
            pixels.append(tuple(target_pixel))
            steps_to_go -= 1
        else:
            for num in range(base):
                target_pixel[1] += y_c
                target_pixel[2] += r_c
                y_steps += 1
                pixels.append(tuple(target_pixel))
                steps_to_go -= 1
            if y_steps%m_steps == 0 and extra > 0:
                extra -= 1
                target_pixel[1] += y_c
                target_pixel[2] += r_c
                y_steps += 1
                pixels.append(tuple(target_pixel))
                steps_to_go -= 1
            target_pixel[0] += x_c
            target_pixel[2] += r_c
            pixels.append(tuple(target_pixel))
            steps_to_go -= 1
    return pixels

def pixel_triangle(point_a, point_b, point_c):
    borderline = pixel_path(point_a, point_b)
    triangle = []
    print(borderline)
    for value in borderline:
        print(value)
        triangle.extend(pixel_path(value, point_c))
    depth_dictionary = {}
    for value in triangle:
        depth_dictionary[(value[0], value[1])] = value[2]
    return depth_dictionary
