import configparser
import os
import sys

ALERT_THRESHOLD = 86400
WARNING_THRESHOLD = 864000
ERROR_MESSAGES = []
WARNING_MESSAGES = []
OUTPUT_FILE = "output.txt"

config_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".conf"):
            config_files.append(os.path.join(root, file))

for file in config_files:
    config = configparser.ConfigParser()
    config.read(file)
    for section in config.sections():
        if config.has_option(section, "frozenTimePeriodInSecs"):
            frozenTimePeriodInSecs = config.getint(section, "frozenTimePeriodInSecs")
            if frozenTimePeriodInSecs < ALERT_THRESHOLD:
                ERROR_MESSAGES.append(
                    f"The index `{section}` in `{file}` has a frozenTimePeriodInSecs of `{frozenTimePeriodInSecs}` which is less than the required value of `{ALERT_THRESHOLD}`"
                )
            elif frozenTimePeriodInSecs < WARNING_THRESHOLD:
                WARNING_MESSAGES.append(
                    f"The index `{section}` in `{file}` has a frozenTimePeriodInSecs of `{frozenTimePeriodInSecs}` which is less than the recommended value of `{WARNING_THRESHOLD}`"
                )

with open(OUTPUT_FILE, "w") as f:
    if ERROR_MESSAGES:
        print(f"::set-output name=status::failure")
        f.write("### Errors :red_circle:\n")
        f.write("\n".join(ERROR_MESSAGES))
    else:
        f.write("### No errors found! :tada:\n")
    if WARNING_MESSAGES:
        f.write("\n### Warnings :warning:\n")
        f.write("\n".join(WARNING_MESSAGES))
