from math import cos, sin, radians


angle = 180
incr = 5
radius = 325



move_code = """{$x, $y, $z, $w},\n"""
code = ""

def process_point(x, y, z, w):
    x = round(x)
    y = round(y)
    z = round(z)
    w = round(w)
    return move_code.replace("$x", str(x)).replace("$y", str(y)).replace("$z", str(z)).replace("$w", str(w))

rem_char = 2

for theta in range(0, angle + incr, incr):
    x = radius
    y = radius * cos(radians(theta))
    z = 50 + radius * sin(radians(theta))
    w = theta
    c = process_point(x, y,z,  w)
    code += c
code = code[:-2]
print(code)