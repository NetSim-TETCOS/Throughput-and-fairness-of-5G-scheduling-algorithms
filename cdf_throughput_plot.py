import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the file path
file_path = 'C:\\Users\\MARK\\OneDrive - TETCOS\\Desktop\\Visual Studio Code\\5G usecase scheduling algo\\Mobility\\throughput_full_rayleigh_mobility.csv'

# Load data from Excel CSV file
data = pd.read_csv(file_path)

# Extract SINR values for each scheduling method
sinr_round_robin = data['Round Robin']
sinr_proportional_fair = data['Proportional Fair']
sinr_max_throughput = data['Max Throughput']

# Calculate the cumulative distribution function (CDF) for each scheduling method
sorted_sinr_round_robin = np.sort(sinr_round_robin)
cdf_round_robin = np.arange(1, len(sorted_sinr_round_robin) + 1) / len(sorted_sinr_round_robin)

sorted_sinr_proportional_fair = np.sort(sinr_proportional_fair)
cdf_proportional_fair = np.arange(1, len(sorted_sinr_proportional_fair) + 1) / len(sorted_sinr_proportional_fair)

sorted_sinr_max_throughput = np.sort(sinr_max_throughput)
cdf_max_throughput = np.arange(1, len(sorted_sinr_max_throughput) + 1) / len(sorted_sinr_max_throughput)

# Plot the CDF for each scheduling method
plt.plot(sorted_sinr_round_robin, cdf_round_robin, linestyle='-', linewidth=2, label='Round Robin')
plt.plot(sorted_sinr_proportional_fair, cdf_proportional_fair, linestyle='-', linewidth=2, label='Proportional Fair')
plt.plot(sorted_sinr_max_throughput, cdf_max_throughput, linestyle='-', linewidth=2, label='Max Throughput')

# Plot settings
plt.xlabel('X (Mbps)')
plt.ylabel('Probability (Throughput <= X)')
plt.title('CDF of Throughtput for different scheduling algorithms')
plt.grid(True)
plt.legend()
plt.show()
