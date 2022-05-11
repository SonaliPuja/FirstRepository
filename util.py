import os


# create folder if not present
def create_folder(folder_path):
    # Check whether the specified path exists or not
    isExist = os.path.exists(folder_path)

    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(folder_path)
        print("The new directory is created!")


# delete file if present
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print("The file has been deleted successfully")

