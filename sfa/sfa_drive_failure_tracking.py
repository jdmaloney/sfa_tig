#!/usr/bin/env python3

# Import standard libraries
import csv
import sys
import datetime
import configparser
import mariadb

# Import third-party libraries
from ddn.sfa.api import \
    APIConnect, APIDisconnect, \
    SFADiskDrive, SFAStorageSystem

# Check if serial number exists in DB already
def db_check_match(serial_number):
    config = configparser.ConfigParser()
    config.read('/etc/telegraf/sfa/sfa_db.cfg')

    db_username = config['DB_Config']['db_user']
    db_password = config['DB_Config']['db_pass']
    db_host = config['DB_Config']['db_host']
    db_db = config['DB_Config']['db_name']

    conn = mariadb.connect(
            host=config['DB_Config']['db_host'],
            port=3306,
            user=config['DB_Config']['db_user'],
            password=config['DB_Config']['db_pass'],
            db=config['DB_Config']['db_name'])
    cur = conn.cursor()
    try:
        query = ('SELECT serial_number from failed_drives WHERE serial_number = %s')
        cur.execute(query, (serial_number,))
    except Exception as e:
        print(f"Error committing transaction: {e}")

    match = cur.fetchone()
    if match == None:
        return 0
    else:
        return 1

    conn.close()

# Insert new failed drive into DB
def db_add_drive(unit_name, serial_number, enclosure_position, disk_slot, vendor, model, drive_interface, media_type, capacity, fw_version):
    config = configparser.ConfigParser()
    config.read('/etc/telegraf/sfa/sfa_db.cfg')

    db_username = config['DB_Config']['db_user']
    db_password = config['DB_Config']['db_pass']
    db_host = config['DB_Config']['db_host']
    db_db = config['DB_Config']['db_name']

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    conn = mariadb.connect(
            host=config['DB_Config']['db_host'],
            port=3306,
            user=config['DB_Config']['db_user'],
            password=config['DB_Config']['db_pass'],
            db=config['DB_Config']['db_name'])
    cur = conn.cursor()
    try:
        query = ('INSERT INTO failed_drives(timestamp, storage_unit, serial_number, enclosure_index, slot_index, drive_vendor, drive_model, drive_type, drive_speed, drive_capacity, drive_fw_rev) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        cur.execute(query, (timestamp, unit_name, serial_number, enclosure_position, disk_slot, vendor, model, drive_interface, media_type, capacity, fw_version,))
    except Exception as e:
        print(f"Error committing transaction: {e}")

    conn.commit()
    conn.close()

# Pull list of bad drives from the array and associated drive information
def pull_sfa_bad_drives(con_ip, con_user, con_pass):
    try:
        # set up API context
        APIConnect("https://" + con_ip, auth=(con_user, con_pass))
        system = SFAStorageSystem.get()
        unit_name = system.Name

        components = SFADiskDrive.getAll()
        for component in components:
            if component.DiskHealthState == 1:
                drive_type=component.DeviceType
                if drive_type == 1:
                    drive_interface = "SATA"
                elif drive_type == 2:
                    drive_interface = "SAS"
                elif drive_type == 4:
                    drive_interface = "NVME"
                drive_speed_type=component.RotationSpeed
                if 0 <= drive_speed_type <=5:
                    media_type = "HDD"
                elif drive_speed_type == 6:
                    media_type = "NVME"
                disk_slot=component.DiskSlotNumber
                enclosure_position=component.EnclosurePosition
                raw_capacity=component.RawCapacity
                serial_number=component.SerialNumber
                vendor=component.VendorID
                model=component.ProductID
                blocksize=component.BlockSize
                fw_version=component.ProductRevision
                capacity = blocksize * raw_capacity
                
                is_matched = db_check_match(serial_number)

                if is_matched == 0:
                    db_add_drive(unit_name, serial_number, enclosure_position, disk_slot, vendor, model, drive_interface, media_type, capacity, fw_version)

        # End API context
        APIDisconnect()

    except:
        print("Conection Failed")

def main():
    '''
    Main processing function
    '''
    with open('/etc/telegraf/sfa/sfas.csv', newline='') as csvfile:
        sfa_units = list(csv.reader(csvfile))

    for s in sfa_units:
        controller_ip = s[0]
        controller_user = s[1]
        controller_password = s[2]
        pull_sfa_bad_drives(controller_ip,controller_user,controller_password)

# Allow other programs to source this one as a library
if __name__ == '__main__':
    try:
        main()
    finally:
        sys.exit(0)
