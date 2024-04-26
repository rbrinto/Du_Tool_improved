#!/usr/bin/env python3

# OPS445 Assignment 2
# Script: duim.py 
# Author: Rasheeque Ahnaf Brinto

'''The python code in this file (duim.py) is original work written by
the author. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.'''

# Description: This tool is an advanced version of du tool providing better output.
# Date: 26th March 2024

import subprocess, sys
import argparse

########################

if len(sys.argv) < 2:
    print("     Error: Try duim.py -h for help")
    # running script without any arguments.
    sys.exit

########################

def parse_command_args():
        
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts", epilog="Copyright 2024") 
    # creates an ArgumentParser object from the argparse module.
    
    parser.add_argument("target", nargs="?", help="The directory to scan.")
    # not an argument. just part of help message and not directly used by user but used by main function only to access path
    
    parser.add_argument("-H", "--human-readable", action="store_true", help="Print sizes in human readable format (e.g. 1K 23M 2G)")
    # Human readable option argument with help message 
    
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # Length argument with default value 20
    
    return parser.parse_args()

########################

def percent_to_graph(percent: int, total_chars: int) -> str:
    # Returning a string representing a bar graph with a specified percentage.

    try:
        # check for out of range inputs
        if not 0 <= percent <= 100:
            raise ValueError("Percent must be between 0 and 100.")
        # checking for input output range and making sure correct integer range is provided
        if total_chars <= 0:
            raise ValueError("Total characters must be a positive integer.")

        # Calculate the number of symbols and spaces
        num_symbols = int(round((percent / 100 * total_chars)))
        
        # num_symbols = int(percent / 100 * total_chars)
        # if round() is not used, checking script fails to pass the test so I added it.
        
        num_spaces = total_chars - num_symbols
        # calculates the total number of spaces 

        # Return the bar graph string
        return '~' * num_symbols + ' ' * num_spaces 

    except ValueError as ve:
        
        print(f"ValueError: {ve}")
        return '' # avoiding output 'None' from happening

########################

def call_du_sub(location: str) -> list:
    # using subprocess to call `du -d 1 + location`, return raw list
    try:
        # Using subprocess.Popen to run the command 'du -d 1 <target_directory>'
        process = subprocess.Popen(['du', '-d', '1', location], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # performing multiple actions in one line and saving them from process variable
        stdout, stderr = process.communicate() # 
        
        # Getting the stdout and stderr from the process

        # Checking to see if there is any error in the process
        if process.returncode != 0:
            
            # If there's an error, print the stderr and return an empty list
            
            print("Error:", stderr.decode('utf-8'))
            #reference: https://docs.python.org/3/library/stdtypes.html#str.decode
            return []
        
        # Decode the stdout and split lines
        output_lines = stdout.decode('utf-8').split('\n')
        
        # Filtering empty lines 
        output_lines = [line for line in output_lines if line.strip()]
        
        # Filter out empty lines from the list of strings representing output lines.
        # This list iterates over each line in the output_lines list and 
        # includes it in the new list. condition: if it is not empty after stripping whitespace.

        return output_lines
    
    except Exception as e:
        
        print(f"Error occurred: {e}") # printiong the stored error in 'e'
        return [] # returning list

########################

def create_dir_dict(raw_dat: list) -> dict:
    # Get list from du_sub, return dictionary {'directory': size} where size is in bytes.
    
    directory_dict = {}  
    # Initializing an empty dictionary to store directory sizes

    try:
        # Iterating through each line in the raw data list derived from du_sub
        for line in raw_dat: 
            
            # Splitting each line by whitespace to separate size and directory and storing them separately
            
            size, directory = line.split(maxsplit=1)
            #reference: https://stackoverflow.com/questions/30437566/python-str-split-is-it-possible-to-only-specify-the-limit-parameter
            
            # Converting size to integer
            size = int(size)
            
            # Store directory and size in the dictionary
            directory_dict[directory] = size
        
        #returning variable filled with dictionary keys and values
        return directory_dict

    except ValueError as ve: # storing and returning error as ve variable
        
        print(f"ValueError: {ve}")
        return {} # returning empty to avoid 'None' output

########################

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str: # untouched function provided by instructor
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

########################

def main():
    args = parse_command_args() 
    # calling function
    
    target_directory = args.target
    # fetching directory
    
    # Perform DU operation
    output_lines = call_du_sub(target_directory)
    
    if not output_lines:
        
        # avoid crashing for empty line errors
        print("No data received.")
        return
    
    total_size = 0
    for line in output_lines:
        
        # saving splittted data
        size, directory = line.split(maxsplit=1) # reference: line 130
        
        # converting size to int to avoid concatenation errors
        size = int(size)
        
        # increment beforehand
        total_size += size
        
        # using round value to recover the lost portion in size int() otherwise we are seeing 1% loss in the output data for the concatenation
        percent = int(round((size / total_size) * 100))
        
        # fetching and storing graph data
        graph = percent_to_graph(percent, args.length)
        
        # using provided human readable function to manupulate data and store
        human_readable_size = bytes_to_human_r(size)
        
        #printing variables in loop format
        print(f"{percent:3}% [{graph}] {human_readable_size} {directory}")
    
    # total size for human readable calculation
    total_size_human_readable = bytes_to_human_r(total_size)
    
    # printing total size
    print(f"Total: {total_size_human_readable} {target_directory}")

########################

if __name__ == "__main__":
    main()
    # calling main function

