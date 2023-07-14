import time
import os

# user-specified duration values
activation_duration = 2
resting_duration = 5

# total_cycles is a dynamic value based on the activation and resting durations
total_cycles = int(1 * 20 / (activation_duration + resting_duration))

# specify the path of the output directory
directory_path = "C:/Users/samzi/Desktop/Slike turnir/"

# add a timestamp to the file name to create a new file each time the script is run
timestamp = time.strftime("%Y%m%d_%H-%M-%S")
file_path = os.path.join(directory_path, f"{timestamp}_cycles_output.txt")

# create the new output file
file = open(file_path, "w")

# run the cycles
for i in range(total_cycles):
    # Resting period
    print(f"Cycle {i+1} - Resting period")
    file.write(f"{time.ctime()} Cycle {i+1} - Resting period\n")
    time.sleep(resting_duration)

    # Activation period
    print(f"Cycle {i+1} - Activation period")
    file.write(f"{time.ctime()} Cycle {i+1} - Activation period\n")
    time.sleep(activation_duration)

# after all cycles, add one more Resting period
print(f"Cycle {total_cycles+1} - Resting period")
file.write(f"{time.ctime()} Cycle {total_cycles+1} - Resting period\n")
time.sleep(resting_duration)

# close the file after all cycles and the final Resting period
file.close()
print("Process has completed")
