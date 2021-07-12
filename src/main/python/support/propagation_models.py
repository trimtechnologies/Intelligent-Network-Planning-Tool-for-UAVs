import math
from math import log10
from numba import jit
from scipy.constants import speed_of_light


@jit(nopython=True)
def log_distance_ref_d0(gamma: float = 2, pt: float = -17):
    """
    Modelo logaritmo de perda baseado em resultados experimentais. Independe da frequência do sinal transmitido
    e do ganho das antenas transmissora e receptora.
    Livro Comunicações em Fio - Pricipios e Práticas - Rappaport (páginas 91-92).

    :param pt:      Potência transmitida.
    :param gamma:   Expoente de perda de caminho.
    :return:        Retorna um float representando a perda do sinal entre a distância d0 e d.
    """
    return (10 * gamma * log10(1)) - pt


@jit(nopython=True)
def log_distance_path_loss(d: float, gamma: float = 2, d0: float = 1, pr_d0: float = -60, pt: float = -17):
    """
    Modelo logaritmo de perda baseado em resultados experimentais. Independe da frequência do sinal transmitido
    e do ganho das antenas transmissora e receptora.
    Livro Comunicações em Fio - Pricipios e Práticas - Rappaport (páginas 91-92).

    :param pr_d0:   Potência recebida na distância de referencia d0.
    :param pt:      Potência transmitida.
    :param d0:      Distância do ponto de referência d0.
    :param d:       Distância em metros que desejo calcular a perda do sinal.
    :param gamma:   Expoente de perda de caminho.
    :return:        Retorna um float representando a perda do sinal entre a distância d0 e d.
    """
    return (pr_d0 - 10 * gamma * log10(d / d0)) - pt


@jit(nopython=True)
def log_distance_v2_model(d: float, gamma: float = 3, d0: float = 10, pr_d0: float = -69, pt: float = -20):
    """

    :param d:
    :param gamma:
    :param d0:
    :param pr_d0:
    :param pt:
    :return:
    """
    return (pr_d0 - 10 * gamma * log10(d / d0)) - pt


@jit(nopython=True)
def tree_par_log_model(x: float):
    """

    :param x:
    :return:
    """
    return -17.74321 - 15.11596 * math.log(x + 2.1642)


@jit(nopython=True)
def two_par_logistic_model(pt_dbm: float, x: float):
    """

    :param pt_dbm:
    :param x:
    :return:
    """
    # https://en.wikipedia.org/wiki/Logistic_distribution#Related_distributions
    return pt_dbm - (-15.11596 * math.log10(x * 2.1642))


@jit(nopython=True)
def four_par_log_model(pt_dbm: float, x: float):
    """

    :param pt_dbm:
    :param x:
    :return:
    """
    # https://en.wikipedia.org/wiki/Shifted_log-logistic_distribution
    a = 79.500
    b = -38
    c = -100.000
    d = 0.0
    e = 0.005
    return pt_dbm - (d + (a - d) / (pow((1 + pow((x / c), b)), e)))


@jit(nopython=True)
def five_par_log_model(pt_dbm: float, x: float):
    """

    :param pt_dbm:
    :param x:
    :return:
    """
    # https://en.wikipedia.org/wiki/Shifted_log-logistic_distribution
    a = 84.0
    b = -48
    c = -121.0
    d = -5.0
    e = 0.005
    return pt_dbm - (d + (a - d) / (pow((1 + pow((x / c), b)), e)))


@jit(nopython=True)
def cost231_path_loss(f: float, tx_h: float, rx_h: float, d: float, mode) -> float:
    """
    COST231 extension to HATA model
    https://morse.colorado.edu/~tlen5510/text/classwebch3.html
    :param f:       Carrier Frequency (1500 to 2000MHz)
    :param tx_h:    Base station height 30 to 200m
    :param rx_h:    Mobile station height 1 to 10m
    :param d:       Distance between Tx and Rx, 1-20km
    :param mode:    1 = URBAN, 2 = SUBURBAN, 3 = OPEN
    :return:        Path loss
    """
    c = 3  # 3dB for Urban
    lrx_h = math.log10(11.75 * rx_h)
    c_h = 3.2 * (lrx_h * lrx_h) - 4.97  # Large city(conservative)
    c0 = 69.55
    cf = 26.16
    if f > 1500:
        c0 = 46.3
        cf = 33.9

    if mode == 2:
        c = 0  # Medium city (average)
        lrx_h = math.log10(1.54 * rx_h)
        c_h = 8.29 * (lrx_h * lrx_h) - 1.1

    if mode == 3:
        c = -3  # Small city (Optimistic)
        c_h = (1.1 * math.log10(f) - 0.7) * rx_h - (1.56 * math.log10(f)) + 0.8

    log_f = math.log10(f)

    return (
            c0
            + (cf * log_f)
            - (13.82 * math.log10(tx_h))
            - c_h
            + (44.9 - 6.55 * math.log10(tx_h)) * math.log10(d)
            + c
    )


@jit(nopython=True)
def ecc33_path_loss():
    """
    Todo
    :return:
    """
    # https://pdfs.semanticscholar.org/766b/6c7317a191cb8d910adbd520e3615a6afc31.pdf
    pass


@jit(nopython=True)
def egli_path_loss():
    """
    Todo
    :return:
    """
    # https://en.wikipedia.org/wiki/Egli_model
    # https://www.commscope.com/calculators/qegli.aspx
    pass


@jit(nopython=True)
def ericsson_path_loss():
    """
    Todo
    :return:
    """
    # https://thescipub.com/pdf/10.3844/ajeassp.2015.94.99
    pass


@jit(nopython=True)
def fspl_path_loss(d: float, fc: float) -> float:
    """
    Recommendation ITU-R P.525-4 - Calculation of free-space attenuation

    Calculate the free space path loss
    :type d: float
    :type fc: float
    :param d: Distance in meters
    :param fc: Frequency
    :return: Free-space basic transmission loss (dB)
    """
    # https://github.com/Cloud-RF/Signal-Server/blob/master/models/fspl.cc
    # https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.525-4-201908-I!!PDF-E.pdf

    lamb = speed_of_light / fc
    return 20 * log10((4 * math.pi * d) / lamb)


@jit(nopython=True)
def hata_path_loss(f: float, h_B: float, h_M: float, d: float, mode: int = None) -> float:
    """
    HATA URBAN model for cellular planning. The Hata model is a radio propagation model for predicting the path loss of
    cellular transmissions in exterior environments, valid for microwave frequencies from 150 to 1500 MHz

    :param f:   Frequency (MHz) 150 to 1500MHz
    :param h_B: Base station height 30-200m
    :param h_M: Mobile station height 1-10m
    :param d:   Distance 1-20km
    :param mode: mode 1 = URBAN; mode 2 = SUBURBAN; mode 3 = OPEN
    :return: Path loss of cellular transmissions
    """
    # https://en.wikipedia.org/wiki/Hata_model
    # https://github.com/Cloud-RF/Signal-Server/blob/master/models/hata.cc
    logf = log10(f)

    if f < 200:
        lh_M = log10(1.54 * h_M)
        C_H = 8.29 * (lh_M * lh_M) - 1.1
    else:
        lh_M = log10(11.75 * h_M)
        C_H = 3.2 * (lh_M * lh_M) - 4.97

    L_u = 69.55 + 26.16 * logf - 13.82 * log10(h_B) - C_H + (44.9 - 6.55 * log10(h_B)) * log10(d)

    if mode is None or mode == 1:
        return L_u  # URBAN

    if mode == 2:  # SUBURBAN
        logf_28 = log10(f / 28)
        return L_u - 2 * logf_28 * logf_28 - 5.4

    if mode == 3:  # OPEN
        return L_u - 4.78 * logf * logf + 18.33 * logf - 40.94

    return 0.0


@jit(nopython=True)
def sui_path_loss(f: float, d: float, terdicpr: float) -> float:
    """
    Todo
    :return:
    """
    # https://core.ac.uk/download/pdf/84396454.pdf
    pass


@jit(nopython=True)
def two_rays_ground_reflection_path_loss(d: float, g_t: float, g_r: float, h_t: float, h_r: float) -> float:
    """
    Todo
    :return:
    """
    return 40 * log10(d) - (10 * log10(g_t) - 10 * log10(g_r) + 20 * log10(h_t) + 20 * log10(h_r))
