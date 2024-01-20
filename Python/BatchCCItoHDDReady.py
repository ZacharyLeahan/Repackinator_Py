import os
import subprocess
import shutil

#This script needs to be run as administrator to register the Repackinator tool for context menu use and os file operations.    

# Register Repackinator for context menu
def run_repackinator_register(repackinator_path):
    register_cmd = f'"{repackinator_path}" -a=register'
    print(f"Executing register command: {register_cmd}")
    subprocess.run(register_cmd, shell=True)

# Find CCI files in a directory even if they are in subdirectories
def find_cci_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.cci'):
                yield os.path.join(root, file)

# Extract the CCI file and move the extracted contents
def extract_and_move(cci_file, repackinator_path, output_directory):
    game_name = os.path.basename(cci_file)

    # Skip files that end with ".2.cci" The Repackinator tool is smart enough to extract .2.cci files when extracting .1.cci files.
    if game_name.endswith(".2.cci"):
        print(f"Skipping {cci_file}")
        return
    
    # Construct the extraction command
    cmd = f'"{repackinator_path}" --action=Extract --input="{cci_file}"'
    
    # Print the command for debugging
    print(f"Executing command: {cmd}")

    # Run the extraction command
    subprocess.run(cmd, shell=True)

    # Determine the source and destination paths for moving
    source_path = os.path.join(os.path.dirname(cci_file), game_name)
    dest_path = os.path.join(output_directory, game_name)

    # Determine the source and destination paths for moving
    extracted_folder_name = os.path.splitext(game_name)[0]
    source_path = os.path.join(os.path.dirname(cci_file), extracted_folder_name)
    dest_path = os.path.join(output_directory, extracted_folder_name)

    # Debugging prints
    print(f"Source Path: {source_path}")
    print(f"Destination Path: {dest_path}")

      # Ensure destination directory exists
    os.makedirs(dest_path, exist_ok=True)

    # Check if source path exists and then move
    if os.path.exists(source_path):
        # Move the contents of the extracted folder to the destination
        for item in os.listdir(source_path):
            source_item = os.path.join(source_path, item)
            dest_item = os.path.join(dest_path, item)
            try:
                if os.path.isfile(source_item):
                    shutil.move(source_item, dest_item)
                elif os.path.isdir(source_item):
                    shutil.move(source_item, dest_item)
                else:
                    print(f"Item not found: {source_item}")
            except Exception as e:
                print(f"Error moving item {source_item}: {e}")
        
        # Remove the source folder, now it should be empty or contain only unprocessed items
        try:
            shutil.rmtree(source_path)
        except OSError as e:
            print(f"Error removing directory {source_path}: {e}")
    else:
        print(f"Warning: Extracted folder not found for {cci_file}")

def main():
    cci_directory = "E:\\XBOX Master Game Collection [CCI]\\PAL\\CCI" # Change this to the directory where your CCI files are located
    repackinator_path = "C:\\Repackinator-win-x64\\repackinator.exe" # Change this to the path where you have Repackinator installed
    output_directory = "E:\\output" # Change this to the directory where you want the extracted files to be placed

    for cci_file in find_cci_files(cci_directory):
        extract_and_move(cci_file, repackinator_path, output_directory)
        print(f"Processed {cci_file}")

if __name__ == "__main__":
    main()
