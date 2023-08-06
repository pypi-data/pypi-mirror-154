# dirs_dict.py
import os


# todo Is it easy to safely write stuff on disk?
def write_dirs_structure_from_dict(folder_structure: dict,
                                   root_dir: str = './') -> None:
    if {} == folder_structure:
        # Do nothing
        return
    # key  : name of file or directory, does not include trailing '/'
    # value: type(value) determines if key or directory
    for key, value in folder_structure.items():
        if dict == type(value):
            # Directory named key, append '/'
            directory_name: str = root_dir + key + '/'
            # Attempt making dir, abort if it exists already
            try:
                os.makedirs(directory_name)
                # Folder does not already exist:  proceed.
                print("--------------------------------------")
                print("Creating new folder: %s" % directory_name)
                print("  >>  Recursive call")
                print(" > Directory name: %s" % directory_name)
                print(" > Folders: %s" % value)
                write_dirs_structure_from_dict(
                    folder_structure=value,
                    root_dir=directory_name
                )
            except FileExistsError:
                # Folder already exists:  abort!
                print("Directory already exists: %s" % directory_name)
                exit(1)
        elif str == type(value):
            # File named key
            file_name = root_dir + key
            write_file_to_disk(
                filename=file_name,
                contents=value
            )
        else:
            print("Somehow, %s was not a string." % value)
            exit(1)
    # Folder structure created.
    return


def write_file_to_disk(filename: str,
                       contents: str) -> None:
    with open(filename, 'w') as file:
        file.write(contents)
    return


if __name__ == "__main__":
    print("Running dirs_dict.py directly.")
    example_dir_structure = {
        'example_folder': {
            'file_A.txt': "contents of file A",
            'file_B.txt': "contents of file B",
            'empty_sub_folder': {
                # Empty.
            }
        }
    }
    example_root_dir = "./"
    print()
    print("Example dictionary: %s" % example_dir_structure)
    write_dirs_structure_from_dict(
        folder_structure=example_dir_structure,
        root_dir=example_root_dir
    )
