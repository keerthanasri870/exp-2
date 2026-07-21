import random
import string

# Generate random text of length 10000
def generate_text(length=10000):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# ---------------- Naive String Matching ----------------
def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    comparisons = 0

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1

    return comparisons

# ---------------- KMP Algorithm ----------------
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)

    lps = compute_lps(pattern)

    i = 0
    j = 0
    comparisons = 0

    while i < n:
        comparisons += 1

        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:
                j = lps[j - 1]

        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return comparisons

# ---------------- Rabin-Karp Algorithm ----------------
def rabin_karp(text, pattern):
    d = 256
    q = 101

    n = len(text)
    m = len(pattern)

    h = 1
    p = 0
    t = 0
    comparisons = 0

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):

        if p == t:
            for j in range(m):
                comparisons += 1
                if text[i + j] != pattern[j]:
                    break

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q

    return comparisons

# ---------------- Main Program ----------------
text = generate_text(10000)

pattern_lengths = [5, 10, 20, 50]

print("Comparison of String Matching Algorithms")
print("-" * 60)
print("{:<10}{:<20}{:<20}{:<20}".format(
    "Pattern", "Naive", "KMP", "Rabin-Karp"))

for length in pattern_lengths:
    start = random.randint(0, len(text) - length)
    pattern = text[start:start + length]

    naive = naive_search(text, pattern)
    kmp = kmp_search(text, pattern)
    rk = rabin_karp(text, pattern)

    print("{:<10}{:<20}{:<20}{:<20}".format(
        length, naive, kmp, rk))