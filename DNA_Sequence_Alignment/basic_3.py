# Basic Sequence Alignment Algorithm
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


def string_alignment(s1: str, s2: str, pairing_builder: list):
    """
    This function builds two aligned strings based on the two original input strings and the results of the basic
    pairing algorithm

    :param s1: string 1
    :param s2: string 2
    :param pairing_builder: a list of pairings using zero-based indices of s1 and s2
    :return: aligned_s1 (str), aligned_s2 (str)
    """

    aligned_s1 = ""
    aligned_s2 = ""
    for s1_index, s2_index in pairing_builder:
        # Check if s1 character is aligned or a gap is needed
        if s1_index != -1:  # If i is a valid index in s1
            aligned_s1 += s1[s1_index]  # Append the corresponding character
        else:
            aligned_s1 += "_"  # Insert gap in s1

        # Check if s2 character is aligned or a gap is needed
        if s2_index != -1:  # If j is a valid index in s2
            aligned_s2 += s2[s2_index]  # Append the corresponding character
        else:
            aligned_s2 += "_"  # Insert gap in s2

    # Logging
    # print(f"Original String 1: {s1}")
    # print(f"Original String 2: {s2}")
    # print(f"Pairings (i, j): {pairing_builder}")
    print(f"Aligned String 1: {aligned_s1}")
    print(f"Aligned String 2: {aligned_s2}")

    return aligned_s1, aligned_s2


def basic_algorithm(filename: str):
    """
    This function uses the input_string_generator() utility to create two text strings consisting of the characters
    'A,' 'C,' 'T,' and 'G.' It then uses the basic string matching algorithm to calculate the optimal alignment of
    the two input strings.

    :param filename: the name of the file used to generate s1 and s2
    :return: opt_cost (int), aligned_s1 (str), aligned_s2 (str)
    """

    # Input String Generator
    [s1, s2] = input_string_generator(filename)

    # Initialize Variables
    m, n = len(s1), len(s2)
    mismatch_penalty = {"AA": 0,   "AC": 110, "AG": 48,  "AT": 94,
                        "CA": 110, "CC": 0,   "CG": 118, "CT": 48,
                        "GA": 48,  "GC": 118, "GG": 0,   "GT": 110,
                        "TA": 94,  "TC": 48,  "TG": 110, "TT": 0}
    gap_penalty = 30

    # Bottom Up Pass (Build Solution Matrix)
    opt = [[0 for _ in range(n+1)] for _ in range(m+1)]  # solution_matrix (m+1 by n+1)
    for i in range(m + 1):
        opt[i][0] = i * gap_penalty  # initialize first col to zeros (base cases: matching s1 substrings with empty s2)
    for j in range(n + 1):
        opt[0][j] = j * gap_penalty  # initialize first row to zeros (base cases: matching s2 substrings with empty s1)
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost_mismatch = mismatch_penalty[s1[i-1]+s2[j-1]] + opt[i-1][j-1]  # mismatch pairing
            cost_gap_s1 = gap_penalty + opt[i-1][j]  # leave a gap in s1
            cost_gap_s2 = gap_penalty + opt[i][j-1]  # leave a gap in s2
            opt[i][j] = min(cost_mismatch, cost_gap_s1, cost_gap_s2)

    # Logging
    # print(f"Cost Matrix ({m+1}x{n+1}):")
    # for i in range(m+1):
    #     print(opt[i])
    print(f"OPT Cost = {opt[m][n]}")

    # Top Down Pass (Find Optimal String Alignment)
    opt_cost, pairing_list = 0, []
    i, j = m, n
    while i >= 1 or j >= 1:
        cost_mismatch = mismatch_penalty[s1[i-1] + s2[j-1]] + opt[i-1][j-1]  # cost of mismatch pairing
        cost_gap_s1 = gap_penalty + opt[i-1][j]  # cost of leaving a gap in s1
        cost_gap_s2 = gap_penalty + opt[i][j-1]  # cost of leaving a gap in s2
        if opt[i][j] == cost_mismatch:
            pairing_list.append((i-1, j-1))
            # print(f"The ith index of s1 and the jth index of s2 are a pair, and we decrement both -> "
            #       f"(i = {i-1}, j = {j-1})")
            opt_cost = opt_cost + opt[i][j] - opt[i-1][j-1]
            i, j = i-1, j-1
        elif opt[i][j] == cost_gap_s2:
            pairing_list.append((-1, j-1))
            # print(f"There is a gap after the ith index of s1, and we decrement j -> (i = {i-1})")
            opt_cost = opt_cost + opt[i][j] - opt[i][j-1]
            j = j-1
        elif opt[i][j] == cost_gap_s1:
            pairing_list.append((i-1, -1))
            # print(f"There is a gap after the jth index of s2, and we decrement i -> (j = {j-1})")
            opt_cost = opt_cost + opt[i][j] - opt[i-1][j]
            i = i-1
    print(f"Verify OPT Cost = {opt_cost}")

    # Flip pairing_list for string_alignment() function
    pairing_list.reverse()
    # Align s1 and s2 according to pairing_list
    aligned_s1, aligned_s2 = string_alignment(s1, s2, pairing_list)

    return opt_cost, aligned_s1, aligned_s2


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
        print("Usage: python basic_3.py input.txt output.txt")

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
