import csv
import os # Used for file path operations and checks

def find_replace_from_csv(csv_path, input_path, output_path, has_header=False):
    """
    Reads find and replace pairs from a CSV file and applies them to an input text file,
    saving the result to an output file.

    Args:
        csv_path (str): Path to the CSV file.
                        Expected format: first column is 'find_text', second column is 'replace_text'.
        input_path (str): Path to the input text file.
        output_path (str): Path to save the modified text file.
        has_header (bool): True if the CSV file has a header row to skip, False otherwise.
    """
    replacements = []
    try:
        with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            if has_header:
                try:
                    next(reader) # Skip the header row
                    print("CSV header row skipped.")
                except StopIteration:
                    print("Warning: CSV file is empty even after attempting to skip header.")
                    # Proceed, replacements list will be empty.
            for i, row in enumerate(reader):
                if len(row) >= 2:
                    # Strip whitespace from both find and replace terms
                    find_text = row[0].strip()
                    replace_text = row[1].strip()
                    if not find_text: # Skip if the find_text is empty after stripping
                        print(f"Warning: Skipping row {i+2 if has_header else i+1} in CSV because 'find' term is empty after stripping whitespace.")
                        continue
                    replacements.append((find_text, replace_text))
                else:
                    # Adjust row number if header was skipped for accurate warning
                    row_num_for_warning = i + 2 if has_header else i + 1
                    print(f"Warning: Skipping row {row_num_for_warning} in CSV due to insufficient columns: {row}")
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_path}'")
        return False # Indicate failure
    except Exception as e:
        print(f"Error reading CSV file '{csv_path}': {e}")
        return False # Indicate failure

    if not replacements:
        print("No valid replacement pairs found or loaded from the CSV file.")
        # Try to copy input to output if no replacements, as user expects an output file
        try:
            with open(input_path, mode='r', encoding='utf-8') as infile:
                content = infile.read() # Read content first
            with open(output_path, mode='w', encoding='utf-8') as outfile:
                outfile.write(content)
            print(f"No replacements made. Input file content copied to '{output_path}'")
            return True # Indicate success (file copied)
        except FileNotFoundError:
            print(f"Error: Input text file not found at '{input_path}' (when trying to copy).")
            return False
        except Exception as e:
            print(f"Error processing files when no replacements: {e}")
            return False

    try:
        with open(input_path, mode='r', encoding='utf-8') as infile:
            content = infile.read()
    except FileNotFoundError:
        print(f"Error: Input text file not found at '{input_path}'")
        return False # Indicate failure
    except Exception as e:
        print(f"Error reading input file '{input_path}': {e}")
        return False # Indicate failure

    # Perform the replacements
    # The order of replacements is determined by their order in the CSV file.
    print(f"\nPerforming {len(replacements)} replacements...")
    for find_text, replace_text in replacements:
        original_content_len = len(content)
        content = content.replace(find_text, replace_text)
        if len(content) != original_content_len:
            print(f"  Replaced '{find_text}' with '{replace_text}'")
        # else:
            # print(f"  Term '{find_text}' not found.") # Can be verbose, uncomment if needed

    try:
        with open(output_path, mode='w', encoding='utf-8') as outfile:
            outfile.write(content)
        print(f"\nSuccessfully processed file. Output saved to '{output_path}'")
        return True # Indicate success
    except Exception as e:
        print(f"Error writing output file '{output_path}': {e}")
        return False # Indicate failure

# --- Main execution block ---
if __name__ == "__main__":
    print("--- Text Replacer from CSV (Interactive) ---")

    # Get CSV file path from user
    csv_file_path = ""
    while True:
        csv_file_path_input = input("Enter the path to the CSV file (e.g., replacements.csv): ").strip()
        if not csv_file_path_input:
            print("CSV file path cannot be empty. Please try again.")
            continue
        if os.path.exists(csv_file_path_input) and os.path.isfile(csv_file_path_input):
            csv_file_path = csv_file_path_input
            break
        else:
            print(f"Error: File not found or is not a file at '{csv_file_path_input}'. Please enter a valid path.")

    # Ask if the CSV has a header row
    csv_has_header = False
    while True:
        header_input = input("Does your CSV file have a header row? (yes/no, default: no): ").strip().lower()
        if header_input in ['yes', 'y']:
            csv_has_header = True
            break
        elif header_input in ['no', 'n', '']: # Empty input defaults to 'no'
            csv_has_header = False
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    # Get input text file path from user
    input_text_file_path = ""
    while True:
        input_text_file_path_input = input("Enter the path to the input text file (e.g., input.txt): ").strip()
        if not input_text_file_path_input:
            print("Input text file path cannot be empty. Please try again.")
            continue
        if os.path.exists(input_text_file_path_input) and os.path.isfile(input_text_file_path_input):
            input_text_file_path = input_text_file_path_input
            break
        else:
            print(f"Error: File not found or is not a file at '{input_text_file_path_input}'. Please enter a valid path.")

    # Suggest a default output file name based on the input file name
    input_dir, input_filename = os.path.split(input_text_file_path)
    input_name_part, input_ext_part = os.path.splitext(input_filename)
    # Ensure suggested_output_filename is in the same directory as input, or current if input_dir is empty
    suggested_output_dir = input_dir if input_dir else "."
    suggested_output_filename = os.path.join(suggested_output_dir, f"{input_name_part}_modified{input_ext_part}")

    # Get output text file path from user
    output_text_file_path_input = input(f"Enter the path for the output text file (press Enter for default: '{suggested_output_filename}'): ").strip()
    output_text_file_path = output_text_file_path_input if output_text_file_path_input else suggested_output_filename

    # Confirm paths before processing
    print(f"\n--- Configuration ---")
    print(f"  CSV file:         {csv_file_path}")
    print(f"  CSV has header:   {'Yes' if csv_has_header else 'No'}")
    print(f"  Input text file:  {input_text_file_path}")
    print(f"  Output text file: {output_text_file_path}")
    print(f"-----------------------\n")

    # Run the main function
    if find_replace_from_csv(csv_file_path, input_text_file_path, output_text_file_path, csv_has_header):
        print("\nOperation completed successfully.")
    else:
        print("\nOperation encountered errors.")


