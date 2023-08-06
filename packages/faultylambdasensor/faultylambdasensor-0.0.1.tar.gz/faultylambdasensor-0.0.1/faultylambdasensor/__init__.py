from fuelmap import fuel_load, fuel_rpm, afr
from ignitionmap import igni_load, igni_rpm, spark_angle
from scipy.interpolate import interp2d


def airfuelratio(given_load, given_rpm):
    a_f_r = interp2d(fuel_load, fuel_rpm, afr, kind='linear', fill_value='-1')
    airistofuelratio = (float(round(a_f_r(given_load, given_rpm)[0], 4)))/14.7
    return airistofuelratio


def sparkangle(given_load, given_rpm):
    spang = interp2d(igni_load, igni_rpm, spark_angle,
                     kind='linear', fill_value='-1')
    sparkangle = float(round(spang(given_load, given_rpm)[0], 4))
    return sparkangle
