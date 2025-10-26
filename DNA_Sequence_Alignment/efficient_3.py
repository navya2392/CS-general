# Efficient Sequence Alignment Algorithm
# Authors: Ben Streck (6276247283), Shravya Shashidhar (2763825542), Navya Bhat (5673980946)

import sys
import timeit
# import psutil
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
    opt_cost, aligned_s1, aligned_s2 = efficient_algorithm(filename_in)
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
            temp_s1 = temp_s1[:index+1] + temp_s1 + temp_s1[index+1:]

        temp_s2 = base_s2
        for i in range(len(array_k)):
            index = int(array_k[i])  # Index where the copy should be inserted
            temp_s2 = temp_s2[:index+1] + temp_s2 + temp_s2[index+1:]

        s1 = temp_s1
        s2 = temp_s2

        if not validate_string_length(s1, s2, base_s1, base_s2, array_j, array_k):
            raise Exception("Length Error: s1 and/or s2 have an incorrect length based on the given input parameters")
        return s1, s2

    except Exception as error:
        print(error)


def string_alignment(s1: str, s2: str, pairing_builder: list):
    """
    This function builds two aligned strings based on the two original input strings and the results of the efficient
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


def efficient_cost(s1, s2, reverse = False):
    """
    Compute the last row of the DP table for aligning s1 with s2,
    using only two rows (space-efficient).
    Returns a list of costs for aligning s1 with all prefixes of s2.
    Use O(n) space instead of O(mn) by using temporary rows curr and prev.
    """

    m = len(s1)
    n = len(s2)
    gap_penalty = 30

    mismatch_penalty = {
        "AA": 0, "AC": 110, "AG": 48, "AT": 94,
        "CA": 110, "CC": 0, "CG": 118, "CT": 48,
        "GA": 48, "GC": 118, "GG": 0, "GT": 110,
        "TA": 94, "TC": 48, "TG": 110, "TT": 0
    }
    #This creates the first row of the opt table.
    prev = [j * gap_penalty for j in range(n + 1)]  # Initial row (gap penalties against empty s1)

    #Temporary row that we will fill in during each iteration.
    #This will hold the costs for aligning current row of s1 with all prefixes of s2.
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i * gap_penalty
        for j in range(1, n + 1):
            if reverse:
                a = s1[m - i]
                b = s2[n - j]
            else:
                a = s1[i - 1]
                b = s2[j - 1]
            cost_match = mismatch_penalty[a + b]
            curr[j] = min(
                prev[j - 1] + cost_match,
                prev[j] + gap_penalty,
                curr[j - 1] + gap_penalty
            )
        prev, curr = curr, prev

    return prev


def efficient_algorithm(filename: str):
    """
    This function uses the input_string_generator() utility to create two text strings consisting of the characters
    'A,' 'C,' 'T,' and 'G.' It then uses the memory-efficient string matching algorithm (Hirschberg’s Algorithm)
    to calculate the optimal alignment of the two input strings using only O(n) space at any time.

    :param filename: the name of the file used to generate s1 and s2
    :return: opt_cost (int), aligned_s1 (str), aligned_s2 (str)
    """

    [s1, s2] = input_string_generator(filename)

    mismatch_penalty = {"AA": 0, "AC": 110, "AG": 48, "AT": 94,
                        "CA": 110, "CC": 0, "CG": 118, "CT": 48,
                        "GA": 48, "GC": 118, "GG": 0, "GT": 110,
                        "TA": 94, "TC": 48, "TG": 110, "TT": 0}
    gap_penalty = 30

    def recursive_align(x, y, x_offset, y_offset):
        """
        Recursive alignment function.
        This function aligns substrings x (From s1) and y (from s2).
        x_offset and y_offset keep track of where x and y start in the original full strings so that the
        final pairing list can map the local indices of x and y to the global indices of the full strings.
        """
        pairing_list = []

        #Handle base case when x is empty. If x is empty, we align all characters in y with gaps in x (-1)
        #Global index (in s2) of each character in y is y_offset + j.
        if len(x) == 0:
            for j in range(len(y)):
                pairing_list.append((-1, y_offset + j))
            return pairing_list

        #Handle base when y is empty. If y is empty, align all characters in x with gaps in y (-1)
        #Global index (in s1) of each character in x is x_offset + i.
        if len(y) == 0:
            for i in range(len(x)):
                pairing_list.append((x_offset + i, -1))
            return pairing_list

        #When either string is very short (1 character), we solve it using the full DP approach
        #It is fast, space efficient O(m) and avoids further recursion.
        if len(x) == 1 or len(y) == 1:
            return base_case_pairing(x, y, x_offset, y_offset)

        # Divide step: split x and compute costs for split points in y
        mid = len(x) // 2
        left_cost = efficient_cost(x[:mid], y) #Forward alignment costs: cost of aligning left half of x with full y.
        right_cost = efficient_cost(x[mid:], y, reverse=True) #Backward alignment cost: cost of aligning right half of x with full y (both reversed).
        #Note: efficient_cost returns only the last row thus saving space.
        #for each possible split point i in y, compute total cost of aligning: x[:mid] with y[:i], x[mid:] with y[i:]
        total_cost = [left_cost[i] + right_cost[len(y) - i] for i in range(len(y) + 1)]
        split_index = total_cost.index(min(total_cost)) #Find best split point in y based on minimum total cost.

        # Recurse on both halves.
        #Every time we split the strings recursively, we pass down the correct offsets so we can map local indices (0, 1, 2...) back to the global indices of the full strings.
        #This way, all base cases and tracebacks know exactly where they are in the full strings.
        #The left half of x still starts at the same index in s1 → so x_offset stays the same.
        #Same for y: since we are aligning the begining of s2, y_offset remains same.
        left_pairings = recursive_align(x[:mid], y[:split_index], x_offset, y_offset)

        #For right, we have moved some characters forward in s1 & s2.
        #x_offset + mid: skips the first half of x
        #y_offset + split_index: skips the first half of y
        right_pairings = recursive_align(x[mid:], y[split_index:], x_offset + mid, y_offset + split_index)

        # Combine the results from the left and right halves into a complete pairing_list.
        pairing_list.extend(left_pairings)
        pairing_list.extend(right_pairings)

        return pairing_list

    #Start the full alignment with both strings and offset 0
    pairing_list = recursive_align(s1, s2, 0, 0)

    # Generate aligned strings from pairings. uses string_alignment (same function from basic.py)
    aligned_s1, aligned_s2 = string_alignment(s1, s2, pairing_list)

    # Compute cost based on aligned strings
    opt_cost = 0
    for i in range(len(aligned_s1)):
        a, b = aligned_s1[i], aligned_s2[i]
        if a == '_' or b == '_':
            opt_cost += gap_penalty
        else:
            opt_cost += mismatch_penalty[a + b]

    print(f"OPT Cost = {opt_cost}")
    return opt_cost, aligned_s1, aligned_s2


def base_case_pairing(s1: str, s2: str, offset1: int, offset2: int):
    """
    Handles base cases using full DP for very short strings where length == 1.
    Returns the list of pairings (i, j) with proper global offsets.
    Matches the structure and format used in basic_algorithm.
    s1, s2: sliced versions of the full input strings.
    offset1: starting index of this substring s1 in the original full string.
    offset2: starting index of s2 in the original full string
    """
    mismatch_penalty = {"AA": 0, "AC": 110, "AG": 48, "AT": 94,
                        "CA": 110, "CC": 0, "CG": 118, "CT": 48,
                        "GA": 48, "GC": 118, "GG": 0, "GT": 110,
                        "TA": 94, "TC": 48, "TG": 110, "TT": 0}
    gap_penalty = 30

    m, n = len(s1), len(s2)
    opt = [[0 for _ in range(n + 1)] for _ in range(m + 1)]  # DP matrix

    # Initialize first column
    for i in range(m + 1):
        opt[i][0] = i * gap_penalty

    # Initialize first row
    for j in range(n + 1):
        opt[0][j] = j * gap_penalty

    # Fill the rest of the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_mismatch = mismatch_penalty[s1[i - 1] + s2[j - 1]] + opt[i - 1][j - 1]  # Diagonal move
            cost_gap_s1 = gap_penalty + opt[i - 1][j]  # Up move (gap in s2)
            cost_gap_s2 = gap_penalty + opt[i][j - 1]  # Left move (gap in s1)
            opt[i][j] = min(cost_mismatch, cost_gap_s1, cost_gap_s2)

    # Traceback to construct pairing list
    pairing_list = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and opt[i][j] == opt[i - 1][j - 1] + mismatch_penalty[s1[i - 1] + s2[j - 1]]:
            pairing_list.append((offset1 + i - 1, offset2 + j - 1))  # Map local index to global.
            #Note: we are matching s1[i-1] and s2[j-1]. These are local indices (0-based).
            #To find the actual position in original full string, we add offset1 + (i - 1) for s1 and offset2 + (j-1) in s2.
            i -= 1
            j -= 1
        elif j > 0 and opt[i][j] == opt[i][j - 1] + gap_penalty:
            pairing_list.append((-1, offset2 + j - 1))  # Gap in s1. Global index of s2 if offset2 + j - 1
            j -= 1
        elif i > 0 and opt[i][j] == opt[i - 1][j] + gap_penalty:
            pairing_list.append((offset1 + i - 1, -1))  # Gap in s2. Global index of s1 is offset1 + i - 1.
            i -= 1

    pairing_list.reverse()
    return pairing_list


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
        print("Usage: python efficient_3.py input.txt output.txt")

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
