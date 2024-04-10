
# started 2/8/2024
# Rich W.
# with
# GitHub Copilot

from collections import Counter
from scipy.stats import chisquare
import importlib
grtd = importlib.import_module("generate-random-test-data")

console_logging = False

def evaluate_randomness(return_data=False):

    # Generate some random numbers
    random_number = grtd.generate_random_number()
    random_number_list = grtd.generate_random_number_list(random_number)

    # Display the random numbers
    if console_logging:
        print(f"Random Numbers: {random_number_list}")

    # Count the frequency of each number
    counter = Counter(random_number_list)

    # Calculate the observed frequencies
    observed_frequencies = [counter[i] for i in range(1, 11)]

    # Calculate the expected frequencies (for a perfectly random sequence, each number should appear the same number of times)
    expected_frequencies = [len(random_number_list) / 10] * 10

    # Perform the Chi-Square Test
    chi_square_stat, p_value = chisquare(observed_frequencies, f_exp=expected_frequencies)

    # Display the results of the Chi-Square Test
    if console_logging: 
        print(f"Chi-Square Statistic: {chi_square_stat}")
        print(f"P-Value: {p_value}")

    # If the p-value is less than 0.05, we reject the null hypothesis that the sequence is random
    if console_logging:
        if p_value < 0.05:
            print(f"P-Value is less than 0.05, so the sequence is not random.")        
        else:
            print(f"P-Value is greater than 0.05, so the sequence is random.")

    if return_data:
        return random_number_list, observed_frequencies, expected_frequencies, chi_square_stat, p_value
    else:
        return p_value >= 0.05
    
if __name__ == '__main__':
    console_logging = True
    evaluate_randomness()