def fraction(n, d):
    """
    Takes numerator and denominator as input and returns proper fraction or improper fraction or a
    simplified fraction.

    Proper Fraction: A fraction where the numerator is less than the denominator, then it is known as a
    proper fraction.

    Improper Fraction: A fraction where the numerator is greater than the denominator, then it is known as an
    improper fraction.

    :param n: Value of numerator
    :param d: Value of denominator
    :return: Fraction value from numerator and denominator
    """
    i = 2
    while i < min(n, d) + 1:
        if n % i == 0 and d % i == 0:
            n = n // i
            d = d // i
        else:
            i += 1
    if d == 1:
        return n
    else:
        return "{}/{}".format(n, d)


def frac_to_float(frac_str):
    """
    Converts the proper fraction, improper fraction and mixed fraction to exact floating number.

    Proper Fraction: A fraction where the numerator is less than the denominator, then it is known as a
    proper fraction.

    Improper Fraction: A fraction where the numerator is greater than the denominator, then it is known as an
    improper fraction.

    Mixed Fraction: A mixed fraction is the combination of a natural number and fraction. It is basically an
    improper fraction.

    :param frac_str: Fraction string ex: "1 1/2" or "3/5"
    :return: Fraction or mixed(whole) fraction to exact floating number.
    """
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


def float_to_frac(flt):
    """
    Converts an exact floating number to proper fraction or improper fraction.

    Proper Fraction: A fraction where the numerator is less than the denominator, then it is known as a
    proper fraction.

    Improper Fraction: A fraction where the numerator is greater than the denominator, then it is known as an
    improper fraction.

    :param flt: Floating Number
    :return: Fraction from a floating number
    """
    flt_str = str(flt)
    flt_split = flt_str.split('.')
    numerator = int(''.join(flt_split))
    denominator = 10 ** len(flt_split[1])
    if flt == 0.0:
        return 0
    else:
        return fraction(numerator, denominator)
