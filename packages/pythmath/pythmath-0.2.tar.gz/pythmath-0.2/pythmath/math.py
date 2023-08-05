"""
An advance math library that performs math operations such as sine, cosine, tangent etc. and all the necessary
math functions

Finds area of square, area of rectangle, area of circle and area of triangle etc

Author: Roshaan Mehmood

GitHub: https://github.com/roshaan55/pythmath
"""
pi = 3.141592653589793
e = 2.718281828459045


def absolute(x):
    """
    Gets the absolute value of x, if negative it will be positive.

    :param x: Value of x to get its absolute value in positive.
    :return: Absolute value of x in positive
    """
    if x <= 0:
        return x * -1
    return x * 1


def area_circle(r):
    """
    Calculate the area of circle from given radius.

    :param r: Radius of a circle.
    :return: Area of a circle.
    """
    return float(pi * power(r, 2))


def area_rect(a, b):
    """
    Calculates the area of rectangle from given points or sides.

    :param a: Side 'a' of a rectangle.
    :param b: Side 'b' of a rectangle.
    :return: Area of a rectangle.
    """
    return float(a * b)


def perimeter_rect(a, b):
    """
    Calculates the perimeter of a rectangle from given points or sides.

    :param a: Side 'a' of a rectangle.
    :param b: Side 'b' of a rectangle.
    :return: Area of a rectangle.
    """
    return float(2 * (a + b))


def area_square(side):
    """
    Calculates the area of a square from given side, a square has four equal sides,
    therefore it takes only one side to calculate its area.

    :param side: Side of a square.
    :return: Area of a square
    """
    return float(side * side)


def area_triangle(a, b, c):
    """
    Calculates the area of a triangle from three sides of a triangle.

    :param a: First side of a triangle.
    :param b: Second side of a triangle.
    :param c: Third side of a triangle.
    :return: Area of a triangle.
    """
    s = (a + b + c) / 2
    return square_root((s * (s - a) * (s - b) * (s - c)))


def power(a, b):
    """
    Calculates the power x**y (x to the power of y).

    :param a: Base number
    :param b: Exponent Number or power value
    :return: Return x**y (x to the power of y).
    """
    return float(pow(a, b))


def square_root(a):
    """
    Calculates the square root of a number

    :param a: Number Value
    :return: Square Root of a number to which the square root will be calculated
    """
    return float(a ** (1 / 2))


def cube_root(a):
    """
    Calculates cube root of a number

    :param a: Number value to which the cube root will be calculated
    :return: Cube root of a number
    """
    return float(a ** (1 / 3))


def calc_lcm(a, b):
    """
    Calculate The Least Common Multiple of two numbers.

    :param a: First Number
    :param b: Second Number
    :return: The Least Common Multiple of two numbers
    """
    if a > b:
        greater = a
    else:
        greater = b

    while True:
        if (greater % a == 0) and (greater % b == 0):
            lcm = greater
            break
        greater += 1

    return float(lcm)


def calc_gcd(a, b):
    """
    Calculate the Greatest Common Divisor of two numbers.

    :param a: First Number
    :param b: Second Number
    :return: Greatest Common Divisor
    """
    if a > b:
        smaller = b
    else:
        smaller = a
    for i in range(1, smaller + 1):
        if (a % i == 0) and (b % i == 0):
            gcd = i
    return float(gcd)


def deg_to_rad(deg):
    """
    Convert angle x from degrees to radians.

    :param deg: angle in degrees.
    :return: Degrees to Radians.
    """
    return deg * pi / 180


def rad_to_deg(rad):
    """
    Convert angle x from radians to degrees.

    :param rad: angle in radians.
    :return: Radians to Degrees.
    """
    return rad * 180 / pi


def cos(x):
    """
    Calculates the cosine of x in radians.

    :param x: Value of x to be passed in cos(x) function.
    :return: Cosine of x in radians form.
    """
    return (e ** (x * 1j)).real


def cosd(x):
    """
    Calculates the cosine of x in degrees.

    :param x: Value of x to be passed in cosd(x) function.
    :return: Cosine of x in degrees form.
    """
    return cos(x * pi / 180)


def cot(x):
    """
    Calculates the cotangent of x in radians.

    :param x: Value of x to be passed in cot(x) function.
    :return: Cotangent of x in radians form.
    """
    return cos(x) / sin(x)


def cotd(x):
    """
    Calculates Cotangent of x in degrees.

    :param x: Value of x to be passed in cotd(x) function.
    :return: Cotangent of x in degrees form.
    """
    return cot(x * pi / 180)


def cosh(x):
    """
    Calculates the hyperbolic cosine of x in radians format.

    :param x: Value of x to be passed in cosh(x) function.
    :return: Hyperbolic cosine of x in radians format.
    """
    return (power(e, x) + power(e, -x)) / 2


def sin(x):
    """
    Calculates the sine of x in radians format.

    :param x: Value of x to be passed in sin(x) function.
    :return: Sine of x in radians.
    """
    return (e ** (x * 1j)).imag


def sind(x):
    """
    Calculates the sine of x in degrees format.

    :param x: Value of x to be passed in sind(x) function.
    :return: Sine of x in degrees.
    """
    return sin(x * pi / 180)


def sec(x):
    """
    Calculates the secant of x in radians format.

    :param x: Value of x to be passed in sec(x) function.
    :return: Secant of x in radians.
    """
    return 1 / cos(x)


def secd(x):
    """
    Calculates the secant of x in degrees format.

    :param x: Value of x to be passed in secd(x) function.
    :return: Secant of x in degrees.
    """
    return sec(x * pi / 180)


def cosec(x):
    """
    Calculates the cosecant of x in radians format.

    :param x: Value of x to be passed in cosec(x) function.
    :return: Cosecant of x in radians format.
    """
    return 1 / sin(x)


def cosecd(x):
    """
    Calculates the cosecant of x in degrees format.

    :param x: Value of x to be passed in cosecd(x) function.
    :return: Cosecant of x in degrees format.
    """
    return cosec(x * pi / 180)


def sinh(x):
    """
    Calculates the hyperbolic sine of x in radians format.

    :param x: Value of x to be passed in sinh(x) function.
    :return: Hyperbolic sine of x in radians.
    """
    return (power(e, x) - power(e, -x)) / 2


def tan(x):
    """
    Calculates the tangent of x in radians format.

    :param x: Value of x to be passed in tan(x) function.
    :return: Tangent of x in radians.
    """
    return sin(x) / cos(x)


def tand(x):
    """
    Calculates the tangent of x in degrees format.

    :param x: Value of x to be passed in tand(x) function.
    :return: Tangent of x in degrees.
    """
    return tan(x * pi / 180)


def tanh(x):
    """
    Calculates the hyperbolic tangent of x in radians format.

    :param x: Value of x to be passed in tanh(x) function.
    :return: Hyperbolic tangent of x in radians.
    """
    return sinh(x) / cosh(x)


def fact(num):
    """
    Find factorial of x.

    Raise a ValueError if x is negative or non-integral.

    :param num: Number of which you want to find it's factorial
    :return: Factorial of a number 'x'.
    """
    fact = 1
    if num < 0:
        raise ValueError("Sorry, factorial does not exist for negative numbers")
    if not isinstance(num, int):
        raise ValueError("Number is non integral")
    else:
        for i in range(1, num + 1):
            fact = fact * i
        return float(fact)


def isinteger(x):
    """
    Check whether the number is integral or non-integral.

    :param x: Number to check integral or non-integral.
    :return: True if number is integral otherwise False.
    """
    return isinstance(x, int)


def iseven(x):
    """
    Check whether the number is an even number.

    :param x: Number to check even or not.
    :return: True if number is even otherwise False.
    """
    if (x % 2) == 0:
        return True
    else:
        return False


def isodd(x):
    """
    Check whether the number is an odd number.

    :param x: Number to check odd or not.
    :return: True if number is odd otherwise False.
    """
    if (x % 2) != 0:
        return True
    else:
        return False


def isprime(x):
    """
    Check whether the number is a prime number.

    :param x: Number to check prime or not.
    :return: True if number is prime otherwise False.
    """
    if x > 1:
        for n in range(2, x):
            if (x % n) == 0:
                return False
        return True
    else:
        return False


def intsqrt(x):
    """
    Gets the integer part of square root from input.

    :param x: Number to calculate its square root.
    :return: Integer part of square root.
    """
    return floor(square_root(x))


def intcbrt(x):
    """
    Gets the integer part of cube root from input.

    :param x: Number to calculate its cube root.
    :return: Integer part of cube root.
    """
    return floor(cube_root(x))


def ispositive(x):
    """
    Checks whether the number is positive or not.

    :param x: Number to check positive or not.
    :return: True if number is positive otherwise False.
    """
    if x > 0:
        return True
    else:
        return False


def isnegative(x):
    """
    Checks whether the number is negative or not.

    :param x: Number to check negative or not.
    :return: True if number is negative otherwise False.
    """
    if x < 0:
        return True
    else:
        return False


def iszero(x):
    """
    Checks whether the number is zero or not.

    :param x: Number to check zero or not.
    :return: True if number is zero otherwise False.
    """
    if x == 0:
        return True
    else:
        return False


def is_sorted(lst):
    """
    Check whether the list is sorted or not.

    :param lst: List values to check is sorted or not
    :return: True if the list values are sorted otherwise False.
    """
    i = 1
    flag = 0
    while i < len(lst):
        if lst[i] < lst[i - 1]:
            flag = 1
        i += 1
    if not flag:
        return True
    else:
        return False


def hypotenuse(x, y):
    """
    Calculates the hypotenuse of x and y

    :param x: Value of x
    :param y: Value of y
    :return: Hypotenuse of x and y
    """
    return square_root(x ** 2 + y ** 2)


def floor(n):
    """
    Floors the number.

    :param n: Number you want to be floored.
    :return: Floor of the number
    """
    return int(n // 1)


def floatsum(numbers):
    """
    Calculates the accurate floating sum of values in a sequence or in list

    :param numbers: Numbers to calculate the floating sum
    :return: Accurate Floating Sum of numbers in a list
    """
    a = 0
    for num in numbers:
        a += num
    return float(a)


def floatabs(x):
    """
    Gets the absolute floating value of x.

    :param x: Number to get absolute floating value.
    :return: Absolute floating value of x.
    """
    return (x ** 2) ** 0.5


def ceil(n):
    """
    Find the ceiling of a number

    :param n: Number you want to be ceiled.
    :return: Ceiling of the number
    """
    return int(-1 * n // 1 * -1)


def remainder(num, divisor):
    """
    Find the remainder of two numbers.

    :param num: Number or Dividend
    :param divisor: Value of divisor
    :return: Remainder of two numbers.
    """
    return float(num - divisor * (num // divisor))


def euc_dist(x, y):
    """
    Finds the Euclidean Distance between two points x and y.

    :param x: First Point
    :param y: Second Point
    :return: Euclidean Distance between two points x and y.
    """
    return square_root(sum((px - py) ** 2 for px, py in zip(x, y)))


def exponential(x):
    """
    Finds the exponential of a specific number (e raised to the power of x).

    :param x: Number raise to the power of e
    :return: Exponential of a specific number (e raised to the power of x).
    """
    return power(e, x)


def mean(nums):
    """
    Calculates the exact arithmatic mean(average) of numbers in a list.

    :param nums: Numbers in a list to calculate their arithmatic mean(average).
    :return: Arithmatic mean(average) of numbers in a list.
    """
    return sum(nums) / len(nums)


def float_mean(nums):
    """
    Calculates the floating exact arithmatic mean(average) of numbers in a list.

    :param nums: Numbers in a list to calculate their arithmatic mean(average).
    :return: Floating arithmatic mean(average) of numbers in a list.
    """
    return float(sum(nums) / len(nums))


def median(nums):
    """
    Calculates the median of numbers in a list.

    :param nums: Numbers in a list to calculate their median.
    :return: Median of numbers in a list.
    """
    n = len(nums)
    if n % 2 == 0:
        return nums[n // 2] + nums[n // 2 - 1] / 2
    else:
        return nums[n // 2]


def mode(nums):
    """
    Gets the mode of numbers in a list.

    :param nums: Numbers to get the mode of numbers in a list.
    :return: Mode of numbers in list.
    """
    unique_nums = list(set(nums))
    dictionary = {}
    for i in unique_nums:
        get_count = nums.count(i)
        dictionary[i] = get_count
    max_repeat = 0
    for i in unique_nums:
        get_value = dictionary[i]
        if get_value > max_repeat:
            max_repeat = get_value
    result = ''
    for i in unique_nums:
        if dictionary[i] == max_repeat:
            result = result + str(i) + " "
    return result


def percentage(val, total_val):
    """
    Calculates the percentage.

    :param val: Value
    :param total_val: Total Value
    :return: Percentage.
    """
    return val / total_val * 100


def perc_error(measured_val, true_val):
    """
    Calculates the percentage error from measured value and true or real value.

    :param measured_val: Measured Value
    :param true_val: True or real value
    :return: Percentage error from measured value and true or real value.
    """
    return absolute((measured_val - true_val)) / true_val * 100


def abs_error(measured_val, true_val):
    """
    Calculates the absolute error from measured value and true or real value.

    :param measured_val: Measured value.
    :param true_val: True or real value
    :return: Absolute error from measured values and true or real value.
    """
    return absolute(measured_val - true_val)


def rel_error(measured_val, true_val):
    """
    Calculates the relative error from measured value and true or real value.

    :param measured_val: Measured Value
    :param true_val: True or real value
    :return: Relative error from measured value and true or real value.
    """
    return abs_error(measured_val, true_val) / true_val


def stdev(data):
    """
    Calculates the standard deviation from given dataset.

    Standard Deviation: In statistics, the standard deviation is a measure of the amount of variation or dispersion
    of a set of values. A low standard deviation indicates that the values tend to be close to the mean of the set,
    while a high standard deviation indicates that the values are spread out over a wider range.

    :param data: Values of given dataset
    :return: The standard deviation from given dataset.
    """
    get_mean = mean(data)
    s = 0
    for i in data:
        s += (i - get_mean) ** 2
    return square_root(s / (len(data) - 1))


def pstdev(data):
    """
    Calculates the standard deviation of population from given dataset.

    :param data: Values of given dataset
    :return: Standard deviation of population from given dataset
    """
    m = sum(data) / len(data)
    s = 0
    for i in data:
        s += (i - m) ** 2
    return square_root(s / (len(data)))


def mad(data):
    """
    Calculates the mean absolute deviation from given dataset.

    Mean Absolute Deviation: The mean absolute deviation (MAD) is a measure of variability that indicates the
    average distance between observations and their mean. MAD uses the original units of the data, which simplifies
    interpretation. Larger values signify that the data points spread out further from the average. Conversely,
    lower values correspond to data points bunching closer to it. The mean absolute deviation is also known as the
    mean deviation and average absolute deviation.

    :param data: Values of given dataset
    :return: Mean Absolute Deviation from given dataset
    """
    m = sum(data) / len(data)
    s = 0
    for i in range(len(data)):
        dev = abs(data[i] - m)
        s = s + round(dev, 2)
    return s / len(data)


def zscore(x, mean_val, st_dev):
    """
    Calculates the z score value from x, mean value and from value of standard deviation.

    Z Score: In statistics, the standard score is the number of standard deviations by which the value of a raw score
    is above or below the mean value of what is being observed or measured. Raw scores above the mean have positive
    standard scores, while those below the mean have negative standard scores.

    :param x: Standardized random variable
    :param mean_val: Mean Value
    :param st_dev: Value of standard deviation
    :return: z score value from x, mean value and from value of standard deviation.
    """
    return (x - mean_val) / st_dev


def stderr(data):
    """
    Calculates the standard error from given dataset.

    Standard Error: The standard error of a statistic is the standard deviation of its sampling distribution or an
    estimate of that standard deviation. If the statistic is the sample mean, it is called the standard error of the
    mean.

    :param data: Values of given dataset
    :return: Standard error from given dataset
    """
    return stdev(data) / square_root(len(data))


def samp_err(n, pst_dev, conf=1.96):
    """
    Calculates the sampling error.

    Sampling Error: In statistics, sampling errors are incurred when the statistical characteristics of a population
    are estimated from a subset, or sample, of that population.

    :param n: Size of sampling
    :param pst_dev: Value of standard deviation of population
    :param conf: Confidence level approx: 1.96
    :return: Sampling Error
    """
    return pst_dev / square_root(n) * conf


def sort(lst):
    """
    Sorts the elements in a list in ascending order.

    :param lst: List to be sorted.
    :return: Sorted List
    """
    if is_sorted(lst):
        # string = "The list is sorted already!"
        return "The list is sorted already!"
    else:
        a = []
        for i in range(len(lst)):
            a.append(min(lst))
            lst.remove(min(lst))
        return a


def count(lst):
    """
    Counts how many numbers in a list.

    :param lst: List to count the elements in it.
    :return: Count of numbers in a list.
    """
    c = 0
    for _ in lst:
        c += 1
    return c


def variance(data, v_mode="std"):
    """
    Calculates the variance from given datasets or list.

    Variance: In probability theory and statistics, variance is the expectation of the squared deviation of a random
    variable from its population mean or sample mean. Variance is a measure of dispersion, meaning it is a measure of
    how far a set of numbers is spread out from their average value.

    :param data: Values of given dataset or a list
    :param v_mode: Mode of variance either standard(std) or population(popul).
    :return: Variance from given datasets or list.
    """
    m = mean(data)
    if v_mode == "std":
        return sum([(xi - m) ** 2 for xi in data]) / (len(data) - 1)
    elif v_mode == "pop":
        return sum([(xi - m) ** 2 for xi in data]) / (len(data))


def arr_sum(arr):
    """
    Calculates the sum of 1d array.

    :param arr: Array values of one dimension.
    :return: Sum of 1d array.
    """
    s = 0
    for i in arr:
        s = s + i
    return s


def arr_2d_sum(arr):
    """
    Calculates the sum of 2d array.

    :param arr: Values of 2d array.
    :return: Sum of 2d array.
    """
    my_sum = 0
    for row in arr:
        my_sum += sum(row)
    return my_sum


def nCr(n, r):
    """
    Calculates the combination nCr from n and r.

    :param n: Value of n
    :param r: Value of r
    :return: Result of nCr
    """
    return fact(n) // (fact(r) * fact(n - r))


def nPr(n, r):
    """
    Calculates the permutation nPr from n and r.

    :param n: Value of n
    :param r: Value of r
    :return: Result of nPr
    """
    return fact(n) / fact(n - r)


def minimum(lst):
    """
    Finds the minimum value in a list.

    :param lst: Values of list to find minimum value
    :return: Minimum value from a list.
    """
    return min(lst)


def maximum(lst):
    """
    Finds the maximum value in a list.

    :param lst: Values of list to find maximum value
    :return: Maximum value from a list.
    """
    return max(lst)


def stats_range(data):
    """
    Calculates the statistical range from given dataset or set of integer values.

    Statistical Range: In statistics, the range of a set of data is the difference between the largest and smallest
    values. Difference here is specific, the range of a set of data is the result of subtracting the sample maximum
    and minimum. However, in descriptive statistics, this concept of range has a more complex meaning.

    :param data: Values of given dataset or set of integer values
    :return: Range from given dataset or set of integer values
    """
    return maximum(data) - minimum(data)


def midrange(data):
    """
    Calculates the midpoint range from given dataset or set of integer values.

    Midpoint Range: In statistics, the mid-range or mid-extreme is a measure of central tendency of a sample defined
    as the arithmetic mean of the maximum and minimum values of the data set.

    :param data: Values of given dataset or set of integer values
    :return: Midpoint range from given dataset or set of integer values
    """
    return (maximum(data) + minimum(data)) / 2


def fibonacci(first, second, n_terms=None):
    """
    Prints the fibonacci series in an empty list of n_terms

    Fibonacci Series: In mathematics, the Fibonacci numbers, commonly denoted Fₙ, form a sequence, the Fibonacci
    sequence, in which each number is the sum of the two preceding ones. The sequence commonly starts from 0 and 1,
    although some authors omit the initial terms and start the sequence from 1 and 1 or from 1 and 2.

    :param first: First Number
    :param second: Second Number
    :param n_terms: Number of terms to print fibonacci series, by default its value is 5
    :return: Returns the fibonacci series of n_terms
    """
    i = 2
    lst = [first, second]
    if n_terms is None:
        n_terms = 5
        while i < n_terms:
            fibo = first + second
            lst.append(fibo)
            first = second
            second = fibo
            i += 1
    else:
        while i < n_terms:
            fibo = first + second
            lst.append(fibo)
            first = second
            second = fibo
            i += 1
    return lst


def mult_two_lst(lst1, lst2):
    """
    Multiplies numbers of two list

    :param lst1: Numbers of list 1
    :param lst2: Numbers of list 2
    :return: Product list of numbers of list 1 and list 2
    """
    prod_lst = []
    for num1, num2 in zip(lst1, lst2):
        prod_lst.append(num1 * num2)
    return prod_lst


def square_lst(lst):
    """
    Squares the numbers of a list

    :param lst: Numbers in a list
    :return: Squared list of numbers in a list
    """
    sq_lst = [number ** 2 for number in lst]
    return sq_lst


def pow_lst(lst, pow_val=2):
    """
    Calculates the power of each numbers in a list according to the user defined parameter power and appends
    the powered numbers in a new list.

    :param lst: Numbers in a list
    :param pow_val: Value of power to get the power of each number in a list, by default its value is 2
    :return: Powered list of each numbers of previous list.
    """
    sq_lst = [number ** pow_val for number in lst]
    return sq_lst


def isfloat(num):
    """
    Checks whether the number is float or not.

    :param num: Number to check float or not
    :return: True if the number is float otherwise False.
    """
    if isinstance(num, float):
        return True
    else:
        return False


def pos_neg(num):
    """ returns the positive number if the inputted number is negative and returns negative number if the inputted
    number is positive. """
    if ispositive(num):
        if isfloat(num):
            return float(num * - 1)
        else:
            return num * - 1
    elif isnegative(num):
        if isfloat(num):
            return float(num * - 1)
        else:
            return num * - 1
