# Basic Sequence Alignment Algorithm - Revised
# Authors: Ben Streck (6276247283), Shravya Shashidhar (2763825542), Navya Bhat (5673980946)

import sys
import timeit
import psutil
import tracemalloc


# def process_memory():
#     """
#
#     :return:
#     """
#     process = psutil.Process()
#     memory_info = process.memory_info()
#     memory_consumed = int(memory_info.rss/1024)
#     return memory_consumed


def time_wrapper(filename_in: str):
    """
    TODO Function Header
    :param filename_in:
    :return:
    """
    start_time = timeit.default_timer()
    opt_cost, aligned_s1, aligned_s2 = basic_algorithm(filename_in)
    end_time = timeit.default_timer()
    time_taken = (end_time-start_time)*1000
    return str(time_taken), opt_cost, aligned_s1, aligned_s2


def string_parameters(filename: str):
    """
    This function extracts base_s1, base_s2, array_j, and array_k from filename. This file is assumed to follow a
    precise format according to the specifications in the project description and error handling for erroneous file
    formats is not included in the code

    :param filename: the name of the file that includes parameters for the input string generation
    :return: base_s1 (str), array_j (int list), base_s2 (str), array_k (int list)
    """

    data, i = [], 0
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        while i < len(lines):
            base_str = lines[i].strip()  # Read the base string
            data.append(base_str)  # Add to data list
            i += 1
            base_array = []
            while i < len(lines) and lines[i].strip().isdigit():
                base_array.append(int(lines[i].strip()))  # Read the next j or k lines of integers
                i += 1
            data.append(base_array)  # Add the array of integers to the data list

        # print(f"Input File: {filename} -> {data}")
        base_s1, array_j, base_s2, array_k = data[0], data[1], data[2], data[3]
        return base_s1, array_j, base_s2, array_k

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist")
    except Exception as error:
        print(error)


def validate_string_length(s1: str, s2: str, base_s1: str, base_s2: str, array_j: str, array_k: str):
    """
    This function validates that the resulting strings (s1 and s2) have the correct length according to their
    input parameters

    :param s1: string 1
    :param s2: string 2
    :param base_s1: base nucleotides for s1 generation
    :param base_s2: base nucleotides for s2 generation
    :param array_j: integer array for s1 generation
    :param array_k: integer array for s2 generation
    :return: pass/fail status of string generation based on the analysis of string lengths (boolean)
    """

    return ((2 ** len(array_j)) * len(base_s1) == len(s1)) & ((2 ** len(array_k)) * len(base_s2) == len(s2))


def input_string_generator(filename: str):
    """
    This function generates the input strings, s1 and s2, according to the logic outlined in the project description

    :param filename: the name of the file used to generate s1 and s2
    :return: s1 (str), s2 (str)
    """

    try:
        base_s1, array_j, base_s2, array_k = string_parameters(filename)

        temp_s1 = base_s1
        for i in range(len(array_j)):
            index = int(array_j[i])  # Index where the copy should be inserted
            temp_s1 = temp_s1[:index + 1] + temp_s1 + temp_s1[index + 1:]

        temp_s2 = base_s2
        for i in range(len(array_k)):
            index = int(array_k[i])  # Index where the copy should be inserted
            temp_s2 = temp_s2[:index + 1] + temp_s2 + temp_s2[index + 1:]

        s1 = temp_s1
        s2 = temp_s2

        if not validate_string_length(s1, s2, base_s1, base_s2, array_j, array_k):
            raise Exception("Length Error: s1 and/or s2 have an incorrect length based on the given input parameters")
        return s1, s2

    except Exception as error:
        print(error)


gap_penalty = 30
mismatch_penalty = {
        "AA": 0, "AC": 110, "AG": 48, "AT": 94,
        "CA": 110, "CC": 0, "CG": 118, "CT": 48,
        "GA": 48, "GC": 118, "GG": 0, "GT": 110,
        "TA": 94, "TC": 48, "TG": 110, "TT": 0
    }


def basic_algorithm(filename: str):
    [x, y] = input_string_generator(filename)
    m, n = len(x), len(y)
    OPT = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        OPT[i][0] = i * gap_penalty
    for j in range(n + 1):
        OPT[0][j] = j * gap_penalty
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost1=OPT[i - 1][j - 1] + mismatch_penalty[x[i - 1] + y[j - 1]]
            cost2=OPT[i - 1][j] + gap_penalty
            cost3=OPT[i][j - 1] + gap_penalty
            OPT[i][j] = min(cost1,cost2,cost3)
    print(f"OPT Cost = {OPT[m][n]}")
    opt_cost=OPT[m][n]
    aligned_x = ''
    aligned_y = ''
    i, j = m, n
    while i > 0 and j > 0:
        if OPT[i][j] == OPT[i - 1][j - 1] + mismatch_penalty[x[i - 1] + y[j - 1]]:
            aligned_x = x[i - 1] + aligned_x
            aligned_y = y[j - 1] + aligned_y
            i=i-1
            j=j-1
        elif OPT[i][j] == OPT[i - 1][j] + gap_penalty:
            aligned_x = x[i - 1] + aligned_x
            aligned_y = '_' + aligned_y
            i=i-1
        else:
            aligned_x = '_' + aligned_x
            aligned_y = y[j - 1] + aligned_y
            j=j-1
    while i > 0:
        aligned_x = x[i - 1] + aligned_x
        aligned_y = '_' + aligned_y
        i=i-1
    while j > 0:
        aligned_x = '_' + aligned_x
        aligned_y = y[j - 1] + aligned_y
        j=j-1
    return opt_cost, aligned_x, aligned_y


def write_output_file(filename: str, opt_cost: int, aligned_s1: str, aligned_s2: str, time: str, memory: str):
    """
    TODO Function Header

    :param filename:
    :param opt_cost:
    :param aligned_s1:
    :param aligned_s2:
    :param time:
    :param memory:
    :return:
    """
    with open(filename, "w") as f:
        f.write(str(opt_cost) + '\n')
        f.write(aligned_s1 + '\n')
        f.write(aligned_s2 + '\n')
        f.write(time + '\n')
        f.write(memory)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python string_return_basic.py input.txt output.txt")

    else:
        filename_input = sys.argv[1]
        filename_output = sys.argv[2]
        print(f"Input File 1: {filename_input}")
        print(f"Output File 2: {filename_output}")

        tracemalloc.start()
        t, opt_cost, aligned_s1, aligned_s2 = time_wrapper(filename_input)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        m = str(int(peak / 1024))

        print(f"Time: {t} milliseconds")
        print(f"Memory: {m} kilobytes")
        write_output_file(filename_output, opt_cost, aligned_s1, aligned_s2, t, m)
