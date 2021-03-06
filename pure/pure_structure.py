import os

def createStructure(output_dir, input_files):
    """
    Creates the structure used for the pipeline pure. Links files to the directories we are working with
    """
    # create the directory base tree
    os.mkdir(output_dir)
    tree = ["bins", "input", "virome", "plasmidome", "log"]
    for path in tree:
        current_path = os.path.join(output_dir, path)
        os.mkdir(current_path)

    # link input files to the input_dir
    input_dir = output_dir, "input"
    for path in input_files:
        os.symlink(path, os.path.join(input_dir, path.basename(path))

    # create subdirs in virome
    virome_dir = os.path.join(output_dir, "virome")
    tree = ["virsorter", "marvel", "deepvirfinder"]
    for path in tree:
        current_path = os.path.join(virome_dir, path)
        os.mkdir(current_path)

    # create subdirs in plasmidome
    plasmidome_dir = os.path.join(output_dir, "plasmidome")
    tree = ["plasflow"]
    for path in tree:
        current_path = os.path.join(plasmidome_dir  , path)
        os.mkdir(current_path)
