# 🧬 DNA Sequence Alignment

This project implements **two algorithms** for global sequence alignment:

* **Basic Dynamic Programming Algorithm**
* **Memory-Efficient (Hirschberg-style) Algorithm**

Both compute the **optimal alignment cost** and aligned sequences for DNA strings, comparing performance in **time** and **memory efficiency**.

---

## 🗁️ Folder Structure

```
DNA_Sequence_Alignment/
│
├── basic_3.py                       # Standard DP-based alignment
├── efficient_3.py                   # Memory-efficient divide & conquer version
├── string_return_basic.py           # Wrapper for running basic algorithm
├── string_return_efficient.py       # Wrapper for efficient algorithm
├── string_return_datapoints_plot.py # For plotting time/memory comparisons
├── string_return_test_cases.py      # Unit tests for both algorithms
├── datapoints_plot_3.py             # Plot generation script
├── basic_only_plots.pdf             # Basic algorithm time/memory plot
├── efficient_only_plots.pdf         # Efficient algorithm time/memory plot
├── combined_plots.pdf               # Combined comparison plot
└── SampleTestCases/
    ├── input1.txt … input5.txt
    └── output1.txt … output5.txt
```

---

## ⚙️ How to Run

* **Run Basic Algorithm**

  ```bash
  python string_return_basic.py <input_file> <output_file>
  ```

* **Run Efficient Algorithm**

  ```bash
  python string_return_efficient.py <input_file> <output_file>
  ```

* **Run Tests**

  ```bash
  python -m unittest string_return_test_cases.py
  ```

---

## 🔍 Process Overview

* Inputs define two base DNA strings and integer duplication arrays to generate the final sequences.
* Both algorithms construct these sequences, compute alignment via a defined scoring matrix, and output:

  * Alignment cost
  * Aligned sequences
  * Runtime
  * Memory usage

**Algorithm Comparison**

* *Basic DP:* Fills an entire m×n table (O(mn) time and space).
* *Efficient DP:* Uses divide-and-conquer recursion with O(mn) time and O(m+n) space.

---

## 📊 Performance Analysis

Performance was measured using increasing problem sizes (M+N).
Plots generated using `datapoints_plot_3.py` show:

| Metric              | Basic Algorithm                                          | Efficient Algorithm              |
| ------------------- | -------------------------------------------------------- | -------------------------------- |
| **Time Complexity** | Grows linearly with input size, but high constant factor | Comparable runtime across scales |
| **Memory Usage**    | Increases quadratically                                  | Reduces memory by ~80–90%        |
| **Accuracy**        | Identical alignment results                              | Identical alignment results      |

📈 **From the plots:**

* The **basic version** shows a near-quadratic growth in both memory and time.
* The **efficient version** dramatically reduces memory consumption with minimal time tradeoff.
* The **combined plot** confirms similar runtimes but vastly different memory footprints.

---

## 🧠 Tech Stack

* **Language:** Python 3
* **Libraries:** `unittest`, `psutil`, `timeit`, `matplotlib`, `tracemalloc`
* **Environment:** Command line / Jupyter Notebook

---

## 👩‍💻 Authors

* **Ben Streck 
* **Shravya Shashidhar 
* **Navya Bhat

---

## 📚 References

* Hirschberg, D.S. (1975). “A Linear Space Algorithm for Computing Maximal Common Subsequences.” *Communications of the ACM.*
* CSCI 570 – *Analysis of Algorithms*, University of Southern California.

---

## 🏁 Summary

The **efficient algorithm** preserves alignment accuracy while drastically reducing space complexity, demonstrating the benefits of optimizing dynamic programming for large-scale DNA datasets. These findings align with theoretical expectations and highlight practical tradeoffs between memory and execution time.
