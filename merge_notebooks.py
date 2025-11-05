# check if the package exists
try:
    import nbformat as nbf
    #import nbmerge
    import os
except ImportError:
    print("nbformat package is not installed. Please install it using 'pip install nbformat'.")
    exit(1)

def merge_notebooks(input_files, output_file):
    """
    Merges multiple Jupyter notebooks into a single notebook.

    Parameters:
    input_files (list): List of paths to the input notebook files.
    output_file (str): Path to the output merged notebook file.
    """
    merged_notebook = nbf.v4.new_notebook()
    merged_notebook.cells = []

    for input_file in input_files:
        with open(input_file, 'r', encoding='utf-8') as f:
            notebook = nbf.read(f, as_version=4)
            merged_notebook.cells.extend(notebook.cells)

    with open(output_file, 'w', encoding='utf-8') as f:
        nbf.write(merged_notebook, f)

def choose_path():
    """
    Prompts the user to choose a directory and returns the path.
    """
    #Get all Folders in the current directory
    current_directory = os.getcwd() + "/GP2"
    folders = [f for f in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, f))]
    print("Available folders:")
    for i, folder in enumerate(folders):
        print(f"{i + 1}: {folder}")
    choice = input("Enter the number of the folder you want to choose: ")
    try:
        choice_index = int(choice) - 1
        if 0 <= choice_index < len(folders):
            return os.path.join(current_directory, folders[choice_index])
        else:
            print("Invalid choice. Please try again.")
            return choose_path()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return choose_path()
    
def order_of_notebooks():
    """
    Prompts the user to choose the order of notebooks to merge.
    """
    current_directory = os.getcwd()
    notebooks = [f for f in os.listdir(current_directory) if f.endswith('.ipynb')]
    print("Available notebooks:")
    for i, notebook in enumerate(notebooks):
        print(f"{i + 1}: {notebook}")
    
    order = input("Enter the numbers of the notebooks to merge in the desired order (comma-separated): ")
    try:
        indices = [int(i.strip()) - 1 for i in order.split(',')]
        if all(0 <= i < len(notebooks) for i in indices):
            return [notebooks[i] for i in indices]
        else:
            print("Invalid choice. Please try again.")
            return order_of_notebooks()
    except ValueError:
        print("Invalid input. Please enter numbers separated by commas.")
        return order_of_notebooks()
    
if __name__ == "__main__":
    # Choose the path
    path = choose_path()
    os.chdir(path)
    
    # Get the order of notebooks
    notebook_order = order_of_notebooks()
    
    # Merge notebooks
    output_file = "merged_notebook.ipynb"
    merge_notebooks(notebook_order, output_file)
    
    print(f"Merged notebooks into {output_file}")