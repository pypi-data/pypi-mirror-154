import math
## @package constants
#  This module provides physical constants in uniform format.

## [C], electron charge.
q_e: float = 1.60217662e-19

## [J * s], Planks constant.
h: float = 6.62e-34

## [m / s], speed of light.
c: float = 299792458

## [kg], electron mass.
m_e: float = 9.10938356e-31

## [m], electron radius
r_o: float = 2.8179403267e-15

## [K], room temperature
t_room: float = 273 + 23

## [J / K], Boltzmann constant
k_b = 1.38064852e-23

## [F / m] = [A2 * s4 / (kg * m3)], permittivity of free space
eps_0: float = 8.85418781e-12


## Converts pressure from [Torr] to [Pa]
def torr_to_pa(torr: float) -> float:
    return torr * 133.322368421


## Converts temperature from [deg C] to [deg K]
def cels_to_kelv(cels: float) -> float:
    return cels + 273.15


## floating point infinity
inf: float = float('inf')


## linear interpolation
def interpolate(x_prev: float, x_tgt: float, x_next: float, y_prev: float, y_next: float) -> float:
    return y_prev + (y_next - y_prev) * (x_tgt - x_prev) / (x_next - x_prev)


## linear interpolation in array
def interpolate_arr(x_arr: list[float], y_arr: list[float], x_tgt: float) -> float:
    if len(x_arr) != len(y_arr):
        print('Input array have different length: %d vs %d. Throwing error' % (len(x_arr), len(y_arr)))
        fuckOff
    is_ascending = True
    if x_arr[0] > x_arr[-1]:
        is_ascending = False

    if is_ascending:
        if x_tgt <= x_arr[0] or x_tgt >= x_arr[-1]:
            print('Warning! x out of bounds!')
            return inf
    else:
        if x_tgt >= x_arr[0] or x_tgt <= x_arr[-1]:
            print('Warning! x out of bounds!')
            return inf
    for ind in range(len(x_arr) - 1):
        if is_ascending:
            if x_arr[ind] <= x_tgt < x_arr[ind + 1]:
                return interpolate(x_prev=x_arr[ind], x_tgt=x_tgt, x_next=x_arr[ind + 1], y_prev=y_arr[ind],
                                   y_next=y_arr[ind + 1])
        else:
            if x_arr[ind] >= x_tgt > x_arr[ind + 1]:
                return interpolate(x_prev=x_arr[ind], x_tgt=x_tgt, x_next=x_arr[ind + 1], y_prev=y_arr[ind], y_next=y_arr[ind + 1])
    print(x_arr[0], x_tgt, x_arr[-1])
    print('WTF?')
    return fuckOff


## radians to degrees converter
def rad_to_deg(rad: float) -> float:
    return rad * 180 / math.pi


## degrees to radians converter
def deg_to_rad(deg: float) -> float:
    return deg * math.pi / 180


## angle between two vectors. Result from 0 to 2Pi.
def vector_angle(first_x: float, first_y: float, second_x: float, second_y: float) -> float:
    angle: float = math.atan2(second_y - first_y, second_x - first_x)
    if angle < 0:
        angle += math.tau
    return angle
