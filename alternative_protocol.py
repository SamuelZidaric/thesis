import time
import os

# user-specified duration values
activation_duration = 2
resting_duration = 5
total_time = 1 * 20  # Total time is set here as 20 seconds

# specify the path of the output directory
directory_path = "C:/Users/samzi/Desktop/Slike turnir/"

# add a timestamp to the file name to create a new file each time the script is run
timestamp = time.strftime("%Y%m%d-%H-%M-%S")
file_path = os.path.join(directory_path, f"{timestamp}_cycles_output.txt")

# create the new output file
file = open(file_path, "w")

# Start time for the whole process
start_time_total = time.time()

# Initialize cycle count
cycle_count = 0

while True:
    cycle_count += 1

    # Resting period
    start_time = time.time()
    print(f"Cycle {cycle_count} - Resting period")
    file.write(time.ctime() + f" Cycle {cycle_count} - Resting period\n")
    while time.time() < start_time + resting_duration:
        pass

    # Check if total time limit has been reached before starting Activation period
    if time.time() - start_time_total >= total_time:
        # If time limit reached, add one final Resting period and break
        print(f"Cycle {cycle_count+1} - Resting period")
        file.write(time.ctime() + f" Cycle {cycle_count+1} - Resting period\n")
        final_resting_start_time = time.time()  # Save the start time of final resting period
        while time.time() < final_resting_start_time + resting_duration:
            pass
        break

    # Activation period
    start_time = time.time()
    print(f"Cycle {cycle_count} - Activation period")
    file.write(time.ctime() + f" Cycle {cycle_count} - Activation period\n")
    while time.time() < start_time + activation_duration:
        pass

    # Check if total time limit has been reached after Activation period
    if time.time() - start_time_total >= total_time:
        # If time limit reached, add one final Resting period and break
        print(f"Cycle {cycle_count+1} - Resting period")
        file.write(time.ctime() + f" Cycle {cycle_count+1} - Resting period\n")
        final_resting_start_time = time.time()  # Save the start time of final resting period
        while time.time() < final_resting_start_time + resting_duration:
            pass
        break

file.close()
print("Process has been completed")
