'''
Script used to get output JSON files from text file of SQL query outputs

Author: Aron Gu
Date Created: October 7, 2023
'''
import json
import sys

"""
Description: Generate output JSON file for query 1 or 3 results

Parameters:
    line(string): String of data from a line in text file
    jsonl_file: File object to write to JSON file

Returns:
    None
"""
def query1(line, jsonl_file):
    json_data = {
        "writer": int(line)
    }
    # Write the JSON object to the output .jsonl file with a newline character
    json.dump(json_data, jsonl_file)
    jsonl_file.write('\n')

"""
Description: Generate output JSON file for query 2 results

Parameters:
    line(string): String of data from a line in text file
    jsonl_file: File object to write to JSON file

Returns:
    None
"""
def query2(line, jsonl_file):
    json_data = {
        "flwer": int(line)
    }
    # Write the JSON object to the output .jsonl file with a newline character
    json.dump(json_data, jsonl_file)
    jsonl_file.write('\n')

"""
Description: Generate output JSON file for query 4 results

Parameters:
    line(string): String of data from a line in text file
    jsonl_file: File object to write to JSON file

Returns:
    None
"""
def query4(line, jsonl_file):
    split_json_data = line.strip().split('|')
    json_data = {
        "usr": int(split_json_data[0]),
        "name": split_json_data[1]
    }
    json.dump(json_data, jsonl_file)
    jsonl_file.write('\n')

"""
Description: Generate output JSON file for query 5 or 6 results

Parameters:
    line(string): String of data from a line in text file
    jsonl_file: File object to write to JSON file

Returns:
    None
"""
def query5(line, jsonl_file):
    split_json_data = line.strip().split('|')
    json_data = {
        "writer": int(split_json_data[0]),
        "tdate": split_json_data[1],
        "text": split_json_data[2]
    }
    json.dump(json_data, jsonl_file)
    jsonl_file.write('\n')

"""
Description: Generate output JSON file for query 7 results

Parameters:
    line(string): String of data from a line in text file
    jsonl_file: File object to write to JSON file

Returns:
    None
"""
def query7(line, jsonl_file):
    split_json_data = line.strip().split('|')
    json_data = {
        "lname": split_json_data[0]
    }
    json.dump(json_data, jsonl_file)
    jsonl_file.write('\n')

"""
Description: Generate output JSON file for query 8 results

Parameters:
    line(string): String of data from a line in text file
    jsonl_file: File object to write to JSON file

Returns:
    None
"""
def query8(line, jsonl_file):
    split_json_data = line.strip().split('|')
    json_data = {
        "month": split_json_data[0],
        "tcnt": int(split_json_data[1]),
        "rep_cnt": int(split_json_data[2]),
        "ret_cnt": int(split_json_data[3]),
        "total": int(split_json_data[4])
    }
    json.dump(json_data, jsonl_file)
    jsonl_file.write('\n')

"""
Description: Generate output JSON file for query 9 results

Parameters:
    line(string): String of data from a line in text file
    jsonl_file: File object to write to JSON file

Returns:
    None
"""
def query9(line, jsonl_file):
    split_json_data = line.strip().split('|')
    json_data = {
        "writer": split_json_data[0],
        "tdate": split_json_data[1],
        "text": split_json_data[2],
        "rep_cnt": int(split_json_data[3]),
        "ret_cnt": int(split_json_data[4]),
        "sim_cnt": int(split_json_data[5])
    }
    json.dump(json_data, jsonl_file)
    jsonl_file.write('\n')

"""
Description: Generate output JSON file for query 9 results

Parameters:
    line(string): String of data from a line in text file
    jsonl_file: File object to write to JSON file

Returns:
    None
"""
def query10(line, jsonl_file):
    split_json_data = line.strip().split('|')
    json_data = {
        "usr": int(split_json_data[0]),
        "'top in retweets'": split_json_data[1]
    }
    json.dump(json_data, jsonl_file)
    jsonl_file.write('\n')

"""
Description: Main function to run program
Arguments:
    None

Returns:
    None
"""
def main():
    if len(sys.argv) > 3:
        # Define input and output file paths
        input_txt_file = sys.argv[1]
        queryNum = int(sys.argv[2])
        output_jsonl_file = sys.argv[3]

        # Open the input .txt file for reading and the output .jsonl file for writing
        with open(input_txt_file, 'r') as txt_file, open(output_jsonl_file, 'w') as jsonl_file:
            # Loop through each line in the input .txt file
            for line in txt_file:
                # Assuming each line is a valid JSON object (if not, you might need to clean/transform the data)
                if queryNum == 1 or queryNum == 3:
                    query1(line, jsonl_file)
                elif queryNum == 2:
                    query2(line, jsonl_file)
                elif queryNum == 4:
                    query4(line, jsonl_file)
                elif queryNum == 5 or queryNum == 6:
                    query5(line, jsonl_file)
                elif queryNum == 7:
                    query7(line, jsonl_file)
                elif queryNum == 8:
                    query8(line, jsonl_file)
                elif queryNum == 9:
                    query9(line, jsonl_file)
                elif queryNum == 10:
                    query10(line, jsonl_file)

if __name__=="__main__":
    main()