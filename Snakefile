import json

# config #######################################################################
config_file = "config.txt"

with open(config_file, "r") as f:
    data = f.read()

f.close()
config = json.loads(data)


################################################################################
rule DVF:
    output:
        "demofile3.txt"
    script:
        "pure/scripts/test.py"
