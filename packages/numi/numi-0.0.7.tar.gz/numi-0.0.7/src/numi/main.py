from curses import ALL_MOUSE_EVENTS
from unicodedata import category
from numi.utils import base 
from numi.utils import declensions as dec
import logging

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)

AT_AF = "at_af"


def _get_from_base(n, f):
    """
    Returns all possible variations for the written numbers in the base as a list of strings
    for numbers between 1-19 as well as all numbers that are divisable by 10,100,1000 etc.
    """
    num = base[n, f]
    if "/" in num:
        return num.split("/")
    else:
        return [num]

def _nums_20_99(n, f):
    """
    Returns all possible variations for the written numbers from 20 to 99 as a list of strings.
    """
    n1 = int(str(n)[0] + "0")
    n2 = int(str(n)[1])
    last_number = _get_from_base(n2, f)
    if len(last_number) == 2:
        return [f"{base[n1,AT_AF]} og {n2}" for n2 in last_number]
    else:
        return [f"{base[n1,AT_AF]} og {base[n2,f]}"]

def _nums_100_999(n, f):
    """
    Returns all possible variations for the written numbers from 100 to 999 as a list of strings.
    """

    def _hundreds(n):
        n_1 = int(str(n)[0])
        if n_1 == 1:
            num = f"{base[n_1, 'et_hk_nf']} hundrað"
        elif n_1 in [2, 3, 4]:
            num = f"{base[n_1,'ft_hk_nf']} hundruð"
        else:
            num = f"{base[n_1,'at_af']} hundruð"
        
        return num

    n1 = int(str(n)[0] + "00")
    num1 = _hundreds(n1)
    n2 = n - n1
    num2 = []

    if n in [100, 200, 300, 400, 500, 600, 700, 800, 900]:
        num = [_hundreds(n)]

    elif n2 in [x for x in range(1, 20)] or n2 in [x for x in range(20, 101, 10)]:
        for line in _get_from_base(n2, f):
            num2.append(f"og {line}")
        num2 = num2
    else:
        num2 = _nums_20_99(n2, f)
    
    if num2:
        num = [f"{num1} {n2}" for n2 in num2]
    
    for line in num:
        if "eitt hundrað" in line:
            num.append(line.replace("eitt hundrað", "hundrað"))

    return num

def divert(n, f):
    """
    Handles user input and returns a list of string with all 
    possible variations of if input number
    """
    if (
        n in [x for x in range(1, 20)]
        or n in [x for x in range(20, 91, 10)]
        or n in [1000, 1000000]
    ):
        return _get_from_base(n, f)
    elif n in [x for x in range(20, 100)]:
        return _nums_20_99(n, f)
    elif n in [x for x in range(100, 1000)]:
        return _nums_100_999(n, f)


def parse_input_string(f):
    """
    This functions takes in the input string and does a few things to make the
    package more robust and user friendly. 

    Firstly, it orders the input values separeted by "_" in the correct way. This
    means that the package is agnostic to the order the user sends in. 

    Second, if the user does not specify on or more or all of the three input values
    (number, gender, case) we handle that as if the user want all of the possible 
    numbers, gender or cases for that input number (number here refers the lingustic number
    i.e. singular or plural but also the input number from the user.)

    Thridly, the function throws an error if the input string has e.g. two or more values
    for one of the three possible (number, gender, case).
    """

    # Create a sorted list of all legal combination found in the base. It's sorted
    # for the sake of testing a set is inherently unsorted
    all_combinations = sorted(list(set([x[1] for x in base]))) 
    correct_order = ['number',"gender", "case"]
    # If the input string is none we return all possible combinations of
    # the input string as a list of strings
    if f == None:
        return all_combinations


    # If the input string is one of the input numbers that don't follow declention rules
    # number we don't need look further. 
    if f == AT_AF:
        return [f]

    len_f = len(f.split('_'))
    # If len_f is longer than three means the user has inputed a invalid string
    if len_f > 3:
        raise Exception(f"Sorry, the input string is ambigous")

    # Check wheter the user input e.g. the number twice
    input_value_types = []
    for v in f.split('_'):
        if v not in dec:
            raise Exception(f"Sorry, the input string is ambigous for the part {v} of the input string {f}")

        if dec[v] in input_value_types:
            raise Exception(f"Duplicate value in the input string")
        else:
            input_value_types.append(dec[v])

    # if the length of len_f is three return the input in the correct order
    new_f = []
    if len_f == 3:
        new_f.append(f)

    # if the user only adds one or two values we need to find the category that is missing
    # and populate the string with those categories. 
    categories_present = [dec[x] for x in f.split('_')]
    missing_categories = [x for x in correct_order if x not in categories_present]
    
    if len_f == 2:
        for x in [k for k,v in dec.items() if v== missing_categories[0]]:
            new_f.append(f"{f}_{x}")

    if len_f == 1:
        for m_one in [k for k,v in dec.items() if v== missing_categories[0]]:
            for m_two in [k for k,v in dec.items() if v== missing_categories[1]]:
                new_f.append(f"{f}_{m_one}_{m_two}")


    # Now lest sort all the enties in new_f
    for i in range(len(new_f)):
        new_f[i] = {dec[v]:v for v in new_f[i].split('_')}
        new_f[i] = "{}_{}_{}".format(new_f[i][correct_order[0]],
                                 new_f[i][correct_order[1]],
                                 new_f[i][correct_order[2]])
    logger.debug(f"Sorted input string is {new_f[i]}")
    return new_f


def find_valid_combinations(n,f):
    """
    Given that the last number in the input number controls the declentions 
    we check in the base wheter a combination is valid. We return all valid 
    combinations. If there are no valid combinations an exception is raised. 
    """
    new_f = []


    # if f is only one string at this point, that means the user added a
    # three value string. Let's check if is a valid input.
    # if len(f) == 1:
    #     if (n,f[0]) in base:
    #         logging.debug(f"0: Adding {n,f[0]}")
    #         new_f.append(f[0])

    if len(str(n)) > 1:
        for v in f:
            # if the whole number along with the input stris in the 
            # base, add the combination. 
            if (n,v) in base:
                logging.debug(f"1: Adding {n,v}")

                new_f.append(v)
            # if the last two digit form a number with the input str
            # that is the base we add that to the combination.
            elif (int(str(n)[-2:]), v) in base:
                logging.debug(f"2: Adding {n,v} based on {int(str(n)[-2])}") 

                new_f.append(v)
            # if the last number is in the base with the input str
            # that is the base we add that to the combination.
            elif (int(str(n)[-1]), v) in base:
                logging.debug(f"3: Adding {n,v} based on {int(str(n)[-1])}")
                new_f.append(v)
    else:
        if (n,f) in base:
            logging.debug(f"4: Adding {n,f}")
            new_f.append(f)

    if new_f:
        return new_f
    else:
        raise Exception(f"Sorry, can't find a valid combination with that input")


def spell_out(n, f=None):
    """
    Validates user input and sends the input to diverter.
    The output is printed to the console. 
    """
    logger.debug(f'User input: {n,f}')    
    f = parse_input_string(f)
    logger.debug(f'The the len of f after parse input is {len(f)} and of type {type(f)}')

    f = find_valid_combinations(n,f)

    if len(f) > 1:
        return [[n, v, divert(n,v)] for v in f]
    else:
        return divert(n,f[0])
