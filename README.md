# SFA TIG
These two checks are used to monitor and ingest data from DDN SFA Units running SFA 11.x or 12.x  Data for all component healths/degraded states/hardware status etc. are gathered from every SFA apppliance using the DDN REST API.   Descriptions of the scripts are below along with implementation details for each.

## Overall Deployment
Have the latest DDN python module installed, that matches the version of your newest/most up-to-date SFA appliance.  Python version 3.8+ is recommended, but v3.6.8 is the lowest version tested 

## SFA Health
This section pulls a lot of data from the SFA unit with regard to system health, some of the things it pulls are:
- SFA version
- Temperatures
- Fan speeds
- Voltages
- Pool information
- VD Information
- Enclosure helath
- SEP/SAS connector/expander health
- Power supplies
- UPS batteries
- Internal Disk Health
- Application Stack Health

Data from this check is collected by Telegraf and is put into the InfluxDB database(s) configured in the Telegraf.  It runs every 5 minutes by default, more requent shouldn't be needed.  If this check hits lots of SFA units dialing it back to once per 10 minutes may be needed

## SFA Drive Failure
This check pulls in information about failed drives in all monitored units an puts the data into a distinct database such that they can be centrally tracked for ease of analysis.  The information below is captured:
- Subsystem name
- Serial number
- enclosure index
- enclosure slot index
- drive firmware version
- drive vendor
- drive capacity
- drive type (HDD/SSD)
- Time of Failure recorded

This allows for much easier coorelation spotting across units and systems and lets you see how well the units are performing as well.  This check is also exectuted by Telegraf but injects its information into an SQL database (and returns no text for Telegraf on ingest into InfluxDB).  This keeps all check-execution consistent even if the data destination is different. The necessary DB schema for this database is defined in the drive_failures.sql file.   
