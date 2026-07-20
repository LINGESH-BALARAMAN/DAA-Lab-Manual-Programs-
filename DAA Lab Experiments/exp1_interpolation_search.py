import time
import random
import sys
import matplotlib
matplotlib.use('Agg')  # non-interactive backend: avoids hanging on plt.show()
import matplotlib.pyplot as plt

def interpolation_search(arr, target):
    """
    Interpolation Search Algorithm
    Time Complexity: O(log log n) average, O(n) worst case
    Space Complexity: O(1)
    """
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        # Interpolation formula
        pos = low + int(((target - arr[low]) * (high - low))
                        / (arr[high] - arr[low]))

        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons

def binary_search(arr, target):
    """Binary Search for comparison"""
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons

def performance_analysis():
    sizes = [1000, 5000, 10000, 50000, 100000]
    print(f"{'Size':>10} {'IS Time(ms)':>14} {'BS Time(ms)':>14} "
          f"{'IS Comparisons':>16} {'BS Comparisons':>16}")
    print('-' * 75)

    # Lists to store results for plotting
    is_times, bs_times = [], []
    is_comps, bs_comps = [], []

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        # Interpolation Search timing
        start = time.perf_counter()
        for _ in range(100):
            idx_is, comp_is = interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 100 * 1000

        # Binary Search timing
        start = time.perf_counter()
        for _ in range(100):
            idx_bs, comp_bs = binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 100 * 1000

        print(f"{size:>10} {is_time:>14.4f} {bs_time:>14.4f} "
              f"{comp_is:>16} {comp_bs:>16}")

        is_times.append(is_time)
        bs_times.append(bs_time)
        is_comps.append(comp_is)
        bs_comps.append(comp_bs)

    return sizes, is_times, bs_times, is_comps, bs_comps

# --- Main ---
arr = [2, 5, 10, 15, 23, 35, 48, 60, 75, 90, 105, 120]
target = 35
idx, comps = interpolation_search(arr, target)
print(f"Array: {arr}")
print(f"Searching for: {target}")
print(f"Found at index: {idx}, Comparisons: {comps}")
print()
sizes, is_times, bs_times, is_comps, bs_comps = performance_analysis()

# --- Graphical Representation (Matplotlib) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Execution Time comparison
ax1.plot(sizes, is_times, marker='o', label='Interpolation Search', color='tab:blue')
ax1.plot(sizes, bs_times, marker='s', label='Binary Search', color='tab:orange')
ax1.set_xlabel('Array Size')
ax1.set_ylabel('Average Time (ms)')
ax1.set_title('Execution Time: Interpolation vs Binary Search')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Comparisons count
ax2.plot(sizes, is_comps, marker='o', label='Interpolation Search', color='tab:blue')
ax2.plot(sizes, bs_comps, marker='s', label='Binary Search', color='tab:orange')
ax2.set_xlabel('Array Size')
ax2.set_ylabel('Number of Comparisons')
ax2.set_title('Comparisons: Interpolation vs Binary Search')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('exp1_interpolation_search.png', dpi=150)
print("Saved plot to exp1_interpolation_search.png")
