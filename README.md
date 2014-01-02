Metering
========

scripts to read meter data and fill into MySQL database

The MT171.py script needs to be started once and will then read the meter regulary.
The sleep command almost at the end of the script will pause between reading the meter.

Only when there was a change in read values a line will be written to the log and the database will be updated.
From the time a kwh value changes the mean power in Wats is calculated per hour and also kwh per day and kwh per year.

table 'map' has the translation to log file vallue names.

