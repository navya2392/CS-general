# Test Class - Revised
# Authors: Ben Streck (6276247283), Shravya Shashidhar (2763825542), Navya Bhat (5673980946)

import unittest
from unittest import TestCase
import string_return_basic as basic
import string_return_efficient as efficient


def read_file(filename: str):
    """
    Read the contents of filename (test case's expected output) and returns the optimal solution as well as the
    two aligned strings
    :param filename: the name of the file that contains the test case's expected output
    :return: solution (int), s1 (str), s2 (str)
    """

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        solution = int(lines[0].strip())
        s1 = lines[1].strip()
        s2 = lines[2].strip()
        return solution, s1, s2

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist")
    except Exception as error:
        print(error)


class BasicTest(TestCase):
    """
    Tests for basic_3.py
    """

    def test_basic_1_1(self):
        """
        testing basic_algorithm() with sample test case 1
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input1.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output1.txt")
        self.assertEqual(opt_cost, sol)

    def test_basic_1_2(self):
        """
        testing basic_algorithm() with sample test case 1
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input1.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output1.txt")
        self.assertEqual(aligned_s1, s1)

    def test_basic_1_3(self):
        """
        testing basic_algorithm() with sample test case 1
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input1.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output1.txt")
        self.assertEqual(aligned_s2, s2)

    def test_basic_2_1(self):
        """
        testing basic_algorithm() with sample test case 2
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input2.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output2.txt")
        self.assertEqual(opt_cost, sol)

    def test_basic_2_2(self):
        """
        testing basic_algorithm() with sample test case 2
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input2.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output2.txt")
        self.assertEqual(aligned_s1, s1)

    def test_basic_2_3(self):
        """
        testing basic_algorithm() with sample test case 2
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input2.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output2.txt")
        self.assertEqual(aligned_s2, s2)

    def test_basic_3_1(self):
        """
        testing basic_algorithm() with sample test case 3
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input3.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output3.txt")
        self.assertEqual(opt_cost, sol)

    def test_basic_3_2(self):
        """
        testing basic_algorithm() with sample test case 3
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input3.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output3.txt")
        self.assertEqual(aligned_s1, s1)

    def test_basic_3_3(self):
        """
        testing basic_algorithm() with sample test case 3
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input3.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output3.txt")
        self.assertEqual(aligned_s2, s2)

    def test_basic_4_1(self):
        """
        testing basic_algorithm() with sample test case 4
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input4.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output4.txt")
        self.assertEqual(opt_cost, sol)

    def test_basic_4_2(self):
        """
        testing basic_algorithm() with sample test case 4
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input4.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output4.txt")
        self.assertEqual(aligned_s1, s1)

    def test_basic_4_3(self):
        """
        testing basic_algorithm() with sample test case 4
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input4.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output4.txt")
        self.assertEqual(aligned_s2, s2)

    def test_basic_5_1(self):
        """
        testing basic_algorithm() with sample test case 5
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input5.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output5.txt")
        self.assertEqual(opt_cost, sol)

    def test_basic_5_2(self):
        """
        testing basic_algorithm() with sample test case 5
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input5.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output5.txt")
        self.assertEqual(aligned_s1, s1)

    def test_basic_5_3(self):
        """
        testing basic_algorithm() with sample test case 5
        """
        opt_cost, aligned_s1, aligned_s2 = basic.basic_algorithm("SampleTestCases\\input5.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output5.txt")
        self.assertEqual(aligned_s2, s2)


class EfficientTest(TestCase):
    """
    Tests for efficient_3.py
    """

    def test_efficient_1_1(self):
        """
        testing efficient_algorithm() with sample test case 1
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input1.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output1.txt")
        self.assertEqual(opt_cost, sol)

    def test_efficient_1_2(self):
        """
        testing efficient_algorithm() with sample test case 1
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input1.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output1.txt")
        self.assertEqual(aligned_s1, s1)

    def test_efficient_1_3(self):
        """
        testing efficient_algorithm() with sample test case 1
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input1.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output1.txt")
        self.assertEqual(aligned_s2, s2)

    def test_efficient_2_1(self):
        """
        testing efficient_algorithm() with sample test case 2
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input2.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output2.txt")
        self.assertEqual(opt_cost, sol)

    def test_efficient_2_2(self):
        """
        testing efficient_algorithm() with sample test case 2
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input2.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output2.txt")
        self.assertEqual(aligned_s1, s1)

    def test_efficient_2_3(self):
        """
        testing efficient_algorithm() with sample test case 2
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input2.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output2.txt")
        self.assertEqual(aligned_s2, s2)

    def test_efficient_3_1(self):
        """
        testing efficient_algorithm() with sample test case 3
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input3.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output3.txt")
        self.assertEqual(opt_cost, sol)

    def test_efficient_3_2(self):
        """
        testing efficient_algorithm() with sample test case 3
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input3.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output3.txt")
        self.assertEqual(aligned_s1, s1)

    def test_efficient_3_3(self):
        """
        testing efficient_algorithm() with sample test case 3
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input3.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output3.txt")
        self.assertEqual(aligned_s2, s2)

    def test_efficient_4_1(self):
        """
        testing efficient_algorithm() with sample test case 4
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input4.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output4.txt")
        self.assertEqual(opt_cost, sol)

    def test_efficient_4_2(self):
        """
        testing efficient_algorithm() with sample test case 4
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input4.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output4.txt")
        self.assertEqual(aligned_s1, s1)

    def test_efficient_4_3(self):
        """
        testing efficient_algorithm() with sample test case 4
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input4.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output4.txt")
        self.assertEqual(aligned_s2, s2)

    def test_efficient_5_1(self):
        """
        testing efficient_algorithm() with sample test case 5
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input5.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output5.txt")
        self.assertEqual(opt_cost, sol)

    def test_efficient_5_2(self):
        """
        testing efficient_algorithm() with sample test case 5
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input5.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output5.txt")
        self.assertEqual(aligned_s1, s1)

    def test_efficient_5_3(self):
        """
        testing efficient_algorithm() with sample test case 5
        """
        opt_cost, aligned_s1, aligned_s2 = efficient.efficient_algorithm("SampleTestCases\\input5.txt")
        sol, s1, s2 = read_file("SampleTestCases\\output5.txt")
        self.assertEqual(aligned_s2, s2)


if __name__ == '__main__':
    unittest.main()
