import os

def createStructure(output_dir):
    """
    Creates the structure used for the pipeline pure.  
    """
    os.mkdir(output_dir)
    tree = ["bins", "assembly", "virome", "plasmidome", "log"]
    for path in tree:
        current_path = os.path.join(output_dir, path)
        os.mkdir(current_path)

    virome_dir = os.path.join(output_dir, "virome")
    tree = ["virsorter", "marvel", "deepvirfinder"]
    for path in tree:
        current_path = os.path.join(virome_dir, path)
        os.mkdir(current_path)
