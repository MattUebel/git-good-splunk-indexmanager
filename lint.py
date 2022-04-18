import configparser
import os
import sys

ALERT_THRESHOLD = 86400
WARNING_THRESHOLD = 864000
EXIT_CODE = 0
ERROR_MESSAGES = []
WARNING_MESSAGES = []

# recursively find all .conf files in the app directory
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
                    f"{file} has a frozenTimePeriodInSecs of {frozenTimePeriodInSecs} which is less than the required value of {ALERT_THRESHOLD}"
                )
                EXIT_CODE += 1
            elif frozenTimePeriodInSecs < WARNING_THRESHOLD:
                WARNING_MESSAGES.append(
                    f"{file} has a frozenTimePeriodInSecs of {frozenTimePeriodInSecs} which is less than the recommended value of {WARNING_THRESHOLD}"
                )

if EXIT_CODE > 0:
    print(f"::error::{EXIT_CODE} errors found: {ERROR_MESSAGES}")
    sys.exit(EXIT_CODE)
else:
    print("::success::No errors found")
    if WARNING_MESSAGES:
        print(
            f"::warning::However, {len(WARNING_MESSAGES)} warnings found: {WARNING_MESSAGES}"
        )
    sys.exit(EXIT_CODE)
