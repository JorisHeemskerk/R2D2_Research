import serial

# Make sure to change the dataset name! It can and will overwrite existing files!
write_to_file_path = "../results/output_mirror_corrected.txt"

ser = serial.Serial(
    port='COM7',        # Make sure this is set to the correct COM port!
    baudrate=38400)

arr = []

try:
    while True:
        line = ser.readline()
        line = line.decode("utf-8") #ser.readline returns a binary, convert to string
        print(line, end='')
        line = line[:-1]
        arr.append(line)
        #output_file.write(line)
except KeyboardInterrupt:
    output_file = open(write_to_file_path, "w+")
    for element in arr:
        output_file.write(element) #+ "\n")
    output_file.close()
    print("Press Ctrl-C to terminate while statement")

    pass