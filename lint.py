import configparser
import os

ALERT_THRESHOLD = 86400
WARNING_THRESHOLD = 864000

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
                print(
                    "::error::{} has a frozenTimePeriodInSecs of {} which is less than the ALERT_THRESHOLD of {}".format(
                        file, frozenTimePeriodInSecs, ALERT_THRESHOLD
                    )
                )
            elif frozenTimePeriodInSecs < WARNING_THRESHOLD:
                print(
                    "::warning::{} has a frozenTimePeriodInSecs of {} which is less than the WARNING_THRESHOLD of {}".format(
                        file, frozenTimePeriodInSecs, WARNING_THRESHOLD
                    )
                )
