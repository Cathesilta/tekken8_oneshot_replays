import re

def remove_spaces(input_string):
    return ''.join(input_string.split())

def keep_only_english_characters(s):
    # This regex matches any character that is not a lowercase or uppercase English letter
    return re.sub(r'[^a-zA-Z]', '', s)


def Levenshtein_distance(str1, str2):
    m, n = len(str1), len(str2)

    # Create a matrix to store the distances
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the matrix
    for i in range(m + 1):
        dp[i][0] = i  # Deletion
    for j in range(n + 1):
        dp[0][j] = j  # Insertion

    # Fill in the dp table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],    # Deletion
                                   dp[i][j - 1],    # Insertion
                                   dp[i - 1][j - 1]) # Substitution

    return dp[m][n]

def format_number_to_3_digit(number):
    return f"{number:03d}"