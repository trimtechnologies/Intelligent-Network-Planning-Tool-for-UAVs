from colour import Color

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def get_color_gradient(steps: int = 250) -> list:
    cores = list(Color("red").range_to(Color("green"), steps))
    cores.pop(0)
    cores.pop(len(cores) - 1)
    return cores


COLORS = get_color_gradient(16)  # 64, 32, 24, 16, 8


def get_color_of_interval(x: float, max_value: float = -30, min_value: float = -100):
    """
    Este método retorna uma cor de acordo com o valor que está entre o intervalo min-max. Em outras palavras,
    este método transforma um número em uma cor dentro de uma faixa informada.
    :param min_value: Valor mínimo do intervalo.
    :param max_value: Valor máximo do intervalo.
    :param x: Valor que está dentro do intervalo e que deseja saber sua cor.
    :return: Retorna uma tupla representando um cor no formato RGB.
    """

    # if PAINT_BLACK_BELOW_SENSITIVITY and x < SENSITIVITY:
    #     return BLACK

    percentage = get_percentage_of_range(min_value, max_value, x)
    color = get_value_in_list(percentage, COLORS)

    return color


def get_percentage_of_range(min_value: float, max_value: float, x: float) -> float:
    """
    Método responsável por retornar a porcentagem de acordo com um respectivo intervalo.
    :param min_value: Valor mínimo do intervalo.
    :param max_value: Valor máximo do intervalo.
    :param x: Valor que está no intervalo de min-max que deseja saber sua respectiva porcentagem.
    :return: Retorna uma porcentagem que está de acordo com o intervalo min-max.
    """

    return ((x - min_value) / (max_value - min_value)) * 100


def get_value_in_list(percent: float, list_numbers: list, to_hex: bool = True):
    """
    Método retorna o valor de uma posição de uma lista. A posição é calculada de acordo a porcentagem.
    :param percent: Valor float representando a porcentagem.
    :param list_numbers: Lista com n números.
    :param to_hex: Boolean to inform the return type
    :return: Retorna a cor da posição calculada.
    """
    position = (percent / 100) * len(list_numbers)
    if position < 1:
        position = 1
    elif position >= len(list_numbers):
        position = len(list_numbers)
    return list_numbers[int(position - 1)] if to_hex else hex_to_rgb(list_numbers[int(position - 1)])


def hex_to_rgb(hex_value: str) -> tuple:
    """
    Método responsável por converter uma cor no formato hexadecial para um RGB.
    :param hex_value: Valor em hexadecimal da cor.
    :return: Tupla representando a cor em formato RGB.
    """
    hex_value = str(hex_value).lstrip('#')
    lv = len(hex_value)
    return tuple(int(hex_value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
