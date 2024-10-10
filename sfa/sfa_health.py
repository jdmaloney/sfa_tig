#!/usr/bin/env python3

# Import standard libraries
import csv
import sys

# Import third-party libraries
from ddn.sfa.api import \
    APIConnect, APIDisconnect, \
    SFAController, SFADiskDrive, SFADiskSlot, \
    SFAEnclosure, SFAExpander, SFAFan, \
    SFAICLChannel, SFAICLIOC, SFAInternalDiskDrive, \
    SFAIOC, SFAJob, SFAPowerSupply, SFASEP, \
    SFAStorageSystem, SFAStoragePool, SFATemperatureSensor, SFAUPS, \
    SFAVirtualDisk, SFAVoltageSensor, SFASASConnector, SFAVirtualMachine

def pull_sfa_health(con_ip, con_user, con_pass):
    try:
        # set up API context
        APIConnect("https://" + con_ip, auth=(con_user, con_pass))
        system = SFAStorageSystem.get()
        unit_name = system.Name
        
        # Get Controller Information
        components = SFAController.getAll()
        for component in components:
            dirty_cache_kib = component.DirtySystemCache
            dirty_cache_percent = component.DirtySystemCachePercent
            fw_release = component.FWRelease
            health_state_index = component.HealthState
            if health_state_index == 1:
                health_string = "HEALTH_OK"
            elif health_state_index == 2:
                health_string = "HEALTH_NON_CRITICAL"
            elif health_state_index == 3:
                health_string = "HEALTH_CRITICAL"
            else:
                health_string = "UNKOWN"
            icc_state = component.ICCState
            if icc_state == 1:
                icc_state_string = "ICC_STATE_UP"
            elif icc_state == 2:
                icc_state_string = "ICC_STATE_DOWN"
            elif icc_state == 3:
                icc_state_string = "ICC_STATE_DEGRADED"
            else:
                icc_state_string = "UNKNOWN"
            con_index = component.Index
            system_disks_failed = component.SystemDiskMembersFailed
            system_disk_state = component.SystemDiskMirrorState
            if system_disk_state == 0:
                system_disk_state_string = "MIRROR_STATE_OK"
            elif system_disk_state == 1:
                system_disk_state_string = "MIRROR_STATE_REDUCED"
            elif system_disk_state == 3:
                system_disk_state_string = "MIRROR_STATE_REBUILDING"
            elif system_disk_state == 3:
                system_disk_state_string = "MIRROR_STATE_INOPERATIVE"
            else:
                system_disk_state_string = "UNKOWN"
            uptime_seconds = component.Uptime
            print('sfa_controller_health,unit=' + unit_name + ',controller_index=' + str(con_index) + ' dirty_cache_kib=' + str(dirty_cache_kib) + ',dirty_cache_percent=' + str(dirty_cache_percent) + ',fw_release="' + fw_release + '",health_state_index=' + str(health_state_index) + ',health_string="' + health_string + '",icc_state_index=' + str(icc_state) + ',icc_state_string="' + icc_state_string + '",system_disks_failed=' + str(system_disks_failed) + ',system_disk_state_index=' + str(system_disk_state) + ',system_disk_state_string="' + system_disk_state_string + '",controller_uptime_seconds=' + str(uptime_seconds))

        # Getting Pool Information
        components = SFAStoragePool.getAll()
        for component in components:
            name = component.Name
            d_timeout = component.DiskTimeout
            free_spare_blocks = component.FreeCapacitySpare
            member_count = component.MemberCount
            member_count_healthy = component.MemberCountHealthy
            state = component.State
            if state == 1:
                health = "OPTIMAL"
            elif state == 2:
                health = "SUBOPTIMAL-REDUCED"
            elif state == 3:
                health = "SUBOPTIMAL-REBUILDING"
            elif state == 4:
                health = "SUBOPTIMAL-REBALANCING"
            elif state == 0:
                health = "WAITING"
            sparing = component.SparingPolicy
            if sparing == 0:
                spolicy = "DEFAULT"
            elif sparing == 1:
                spolicy = "AUTO"
            elif sparing == 2:
                spolicy = "MANUAL"
            elif sparing == 3:
                spolicy = "SWAP"
            elif sparing == 4:
                spolicy = "DISTRIBUTED"
            print('sfa_pool_health,unit=' + unit_name + ',pool=' + name + ' health_status=' + str(state) + ',health_string="' + health + '",sparing_policy=' + str(sparing) + ',sparing_string="' + spolicy + '",disk_timeout=' + str(d_timeout) + ',free_spare_blocks=' + str(free_spare_blocks) + ',member_count_health=' + str(member_count_healthy) + ',member_count=' + str(member_count))

        # Getting Virtual Disk Information
        components = SFAVirtualDisk.getAll()
        for component in components:
            name = component.Name
            auto_verify = component.AutoVerifyStatus
            bad_blocks = component.BadBlockCount
            critical = component.Critical
            dirty_cache_kib = component.DirtyCache
            home_con_index = component.HomeControllerIndex
            home_con_rp_index = component.HomeControllerRPIndex
            home_con_rp_name = component.HomeRPName
            pref_home_con_index = component.PreferredHomeControllerIndex
            pref_home_con_rp_index = component.PreferredHomeControllerRPIndex
            pref_home_con_rp_name = component.PreferredHomeRPName
            verify_enabled = component.VerifyEnabled
            forced_write_through = component.ForcedWriteThrough
            if auto_verify == 0:
                verify_status_string = "Disabled"
            elif auto_verify == 1:
                verify_status_string = "Active"
            elif auto_verify == 2:
                verify_status_string = "Enabled_Not_Active"
            write_locked = component.AutoWriteLocked
            if not write_locked:
                write_locked_state = 0
            else:
                write_locked_state = 1
            child_health_state = component.ChildHealthState
            if child_health_state == 1:
                child_health = "HEALTH_OK"
                child_health_error = 0
            elif child_health_state == 2:
                child_health = "NON_CRITICAL_ERROR"
                child_health_error = 1
            elif child_health_state == 3:
                child_health = "CRITICAL_ERROR"
                child_health_error = 1
            forced_write_reasons = component.ForcedWriteThroughReasons
            if forced_write_reasons == 1:
                fwt_reason = "UPS"
            elif forced_write_reasons == 2:
                fwt_reason = "OVERTEMP"
            elif forced_write_reasons == 3:
                fwt_reason = "VOLTAGE"
            elif forced_write_reasons == 4:
                fwt_reason = "NONREDUNDANT_PSU"
            elif forced_write_reasons == 5:
                fwt_reason = "SCWB_DISABLED"
            elif forced_write_reasons == 6:
                fwt_reason = "ENCL_UPDATE"
            else:
                fwt_reason = "NONE"
            vd_health = component.HealthState
            if vd_health == 1:
                vd_health_string = "HEALTH_OK"
            elif vd_health == 2:
                vd_health_string = "NON_CRITICAL_ERROR"
            elif vd_health == 3:
                vd_health_string = "CRITICAL_ERROR"
            rebuild_job_id = component.RebuildJobOID
            if not rebuild_job_id:
                rebuild_running = 0
            else:
                rebuild_running = 1

            print('sfa_vd_health,unit=' + unit_name + ',vd=' + name + ' auto_write_locked_string="' + str(write_locked) + '",auto_write_locked_status_code=' + str(write_locked_state) + ',verify_status_string="' + verify_status_string + '",verify_status_code=' + str(auto_verify) + ',bad_blocks=' + str(bad_blocks) + ',dirty_cache_kib=' + str(dirty_cache_kib) + ',home_con_index=' + str(home_con_index) + ',home_con_rp_index=' + str(home_con_rp_index) + ',home_con_rp_name="' + home_con_rp_name + '",pref_home_con_index=' + str(pref_home_con_index) + ',pref_home_con_rp_index=' + str(pref_home_con_rp_index) + ',pref_home_con_rp_name="' + pref_home_con_rp_name + '",verify_enabled_string="' + str(verify_enabled) + '",forced_write_through_string="' + str(forced_write_through) + '",forced_write_through_reason="' + fwt_reason + '",child_health_string="' + child_health + '",child_health_state=' + str(child_health_error) + ',vd_health_string="' + vd_health_string + '",vd_health_state=' + str(vd_health) + ',rebuild_running=' + str(rebuild_running))

        # Get Drive Summary
        components = SFADiskDrive.getAll()
        drives_healthy, drives_failed, drives_failure_predicted, drives_locked, drives_unformatted, drives_formatting, drives_unusable, drives_unkown = 0, 0, 0, 0, 0, 0, 0, 0
        for component in components:
            drive_health_state = component.DiskHealthState
            if drive_health_state == 0:
                drives_healthy += 1
            elif drive_health_state == 1:
                drives_failed += 1
            elif drive_health_state == 2:
                drives_failure_predicted += 1
            elif drive_health_state == 3:
                drives_locked += 1
            elif drive_health_state == 4:
                drives_unformatted += 1
            elif drive_health_state == 5:
                drives_formatting += 1
            elif drive_health_state == 6:
                drives_unusable += 1
            else:
                drives_unkown += 1
        print('sfa_drive_health,unit=' + unit_name + ' drives_healthy=' + str(drives_healthy) + ',drives_failed=' + str(drives_failed) + ',drives_failure_predicted=' + str(drives_failure_predicted) + ',drives_locked=' + str(drives_locked) + ',drives_unformatted=' + str(drives_unformatted) + ',drives_formatting=' + str(drives_formatting) + ',drives_unusable=' + str(drives_unusable) + ',drives_unkown=' + str(drives_unkown))

        # Get UPS Information
        components = SFAUPS.getAll()
        for component in components:
            ac_failure = component.ACFailure
            if not ac_failure:
                ac_fail_true = 0
            else:
                ac_fail_true = 1
            battery_life_left = component.BatteryLifeRemaining
            charge_remaining = component.EstimatedChargeRemaining
            enclosure_position = component.EnclosurePosition
            enclosure_index = component.EnclosureIndex
            raw_recharge_time = str(component.EstimatedRechargeTime)
            if raw_recharge_time == "None":
                recharge_time = 0
            else:
                recharge_time = raw_recharge_time
            run_time = component.EstimatedRunTime
            fault_present = component.Fault
            if not fault_present:
                fault_state_true = 0
            else:
                fault_state_true = 1
            health_state = component.HealthState
            if health_state == 1:
                health_string = "HEALTH_OK"
                health_error = 0
            elif health_state == 2:
                health_string = "HEALTH_NON_CRITICAL"
                health_error = 1
            elif health_state == 3:
                health_string = "HEALTH_CRITICAL"
                health_error = 1
            predict_failure = component.PredictFailure
            if not predict_failure:
                predict_fail_true = 0
            else:
                predict_fail_true = 1
            ups_failure = component.UPSFailure
            if not ups_failure:
                ups_fail_true = 0
            else:
                ups_fail_true = 1
            warning_status = component.WarningStatus
            if warning_status == 0:
                ups_warn_string = "UPS_WARN_NONE"
            elif warning_status == 1:
                ups_warn_string = "UPS_WARN_TEMP_FAILURE"
            elif warning_status == 2:
                ups_warn_string = "UPS_WARN_LOW_VOLTAGE"
            elif warning_status == 3:
                ups_warn_string = "UPS_WARN_TEMP_WARNING"
            elif warning_status == 4:
                ups_warn_string = "UPS_WARN_REPLACE_REQUIRED"
            elif warning_status == 5:
                ups_warn_string = "UPS_WARN_LOW_CHARGE"
            print('sfa_ups_health,unit=' + unit_name + ',enclosure_index=' + str(enclosure_index) + ',enclosure_position=' + str(enclosure_position) + ' ac_failure=' + str(ac_fail_true) + ',battery_days_left=' + str(battery_life_left) + ',charge_percent=' + str(charge_remaining) + ',recharge_time=' + str(recharge_time) + ',run_time=' + str(run_time) + ',fault_present=' + str(fault_state_true) + ',health_state_string="' + str(health_string) + '",health_error=' + str(health_error) + ',predict_fail_true=' + str(predict_fail_true) + ',ups_fail_true=' + str(ups_fail_true) + ',ups_warn_status="' + str(ups_warn_string) + '"')

        # Get Power Supply Information
        components = SFAPowerSupply.getAll()
        for component in components:
            ac_failure = component.ACFailure
            if not ac_failure:
                ac_failed_true = 0
            else:
                ac_failed_true = 1
            dc_failure = component.DCFailure
            if not dc_failure:
                dc_failed_true = 0
            else:
                dc_failed_true = 1
            enclosure_position = component.EnclosurePosition
            health_state = component.HealthState
            if health_state == 1:
                health_failure = 0
                health_string = "HEALTH_OK"
            elif health_state == 2:
                health_failure = 1
                health_string = "HEALTH_NON_CRITICAL"
            elif health_state == 3:
                health_failure = 1
                health_string = "HEALTH_CRITICAL"
            is_present = component.Present
            if not is_present:
                is_present_state = 0
            else:
                is_present_state = 1
            raw_location = str(component.Location)
            stripped_location = raw_location.strip()
            location = stripped_location.replace(" ", "_")
            power_state = component.PowerState
            if not power_state:
                is_powered = 0
            else:
                is_powered = 1
            psu_fault = component.Fault
            if not psu_fault:
                psu_fault_true = 0
            else:
                psu_fault_true =1
            print('sfa_psu_health,unit=' + unit_name + ',enclosure_position=' + str(enclosure_position) + ',location=' + location + ' ac_failure=' + str(ac_failed_true) + ',dc_failure=' + str(dc_failed_true) + ',health_failure=' + str(health_failure) + ',health_state_string="' + health_string + '",is_present=' + str(is_present_state) + ',is_powerd=' + str(is_powered) + ',psu_fault_true=' + str(psu_fault_true))

        # Get Fan Information
        components = SFAFan.getAll()
        for component in components:
            fan_speed_rpm = component.CurrentSpeed
            enclosure_position = component.EnclosurePosition
            fault = component.Fault
            if not fault:
                fan_fault_true = 0
            else:
                fan_fault_true = 1
            health_state = component.HealthState
            if health_state == 1:
                health_string = "HEALTH_OK"
                health_failure = 0
            elif health_state == 2:
                health_string = "HEALTH_NON_CRITICAL"
                health_failure = 1
            elif health_state == 3:
                health_string = "HEALTH_CRITICAL"
                health_failure = 1
            raw_location = str(component.Location)
            stripped_location = raw_location.strip()
            location = stripped_location.replace(" ", "_")
            present = component.Present
            if not present:
                fan_present = 0
            else:
                fan_present = 1
            print('sfa_fan_health,unit=' + unit_name + ',enclosure_position=' + str(enclosure_position) + ',location=' + location + ' fan_speed_rpm=' + str(fan_speed_rpm) + ',fan_fault_true=' + str(fan_fault_true) + ',health_failure=' + str(health_failure) + ',health_state_string="' + health_string + '",is_present=' + str(fan_present))
        
        # Get Temperature Information
        components = SFATemperatureSensor.getAll()
        for component in components:
            temp_celsius = component.CurrentReading
            enclosure_position = component.EnclosurePosition
            health_state = component.HealthState
            if health_state == 1:
                health_string = "HEALTH_OK"
                health_failure = 0
            elif health_state == 2:
                health_string = "HEALTH_NON_CRITICAL"
                health_failure = 1
            elif health_state == 3:
                health_string = "HEALTH_CRITICAL"
                health_failure = 1
            raw_location = str(component.Location)
            stripped_location = raw_location.strip()
            location = stripped_location.replace(" ", "_")
            present = component.Present
            if not present:
                sensor_present = 0
            else:
                sensor_present = 1
            print('sfa_temp_health,unit=' + unit_name + ',enclosure_position=' + str(enclosure_position) + ',location=' + location + ' temp_celsius=' + str(temp_celsius) + ',health_failure=' + str(health_failure) + ',health_state_string="' + health_string + '",is_present=' + str(sensor_present))

        # Get Enclosure Information
        components = SFAEnclosure.getAll()
        for component in components:
           fault = component.Fault
           if not fault:
               fault_true = 0
           else:
               fault_true = 1
           health_state = component.HealthState
           if health_state == 1:
                health_string = "HEALTH_OK"
                health_failure = 0
           elif health_state == 2:
                health_string = "HEALTH_NON_CRITICAL"
                health_failure = 1
           elif health_state == 3:
                health_string = "HEALTH_CRITICAL"
                health_failure = 1
           enclosure_position = component.Position
           enc_type_id = component.Type
           if enc_type_id == 1:
               enc_type = "DISK"
           elif enc_type_id == 2:
               enc_type = "CONTROLLER"
           elif enc_type_id == 3:
               enc_type = "UPS"
           print('sfa_enc_health,unit=' + unit_name + ',enclosure_position=' + str(enclosure_position) + ',enclosure_type=' + str(enc_type) + ' health_failure=' + str(health_failure) + ',health_state_string="' + health_string + '",enclosure_fault=' + str(fault_true))

        # Get Expander Information
        components = SFAExpander.getAll()
        for component in components:
            enclosure_position = component.EnclosurePosition
            fault = component.Fault
            if not fault:
               fault_true = 0
            else:
               fault_true = 1
            health_state = component.HealthState
            if health_state == 1:
                health_string = "HEALTH_OK"
                health_failure = 0
            elif health_state == 2:
                health_string = "HEALTH_NON_CRITICAL"
                health_failure = 1
            elif health_state == 3:
                health_string = "HEALTH_CRITICAL"
                health_failure = 1
            raw_location = str(component.Location)
            stripped_location = raw_location.strip()
            location = stripped_location.replace(" ", "_")
            is_present = component.Present
            if not is_present:
                present = 0
            else:
                present = 1
            print('sfa_expander_health,unit=' + unit_name + ',enclosure_position=' + str(enclosure_position) + ',location=' + str(location) + ' health_failure=' + str(health_failure) + ',health_state_string="' + health_string + '",expander_fault=' + str(fault_true) + ',is_present=' + str(present))

        # Get Voltage Sensor Information
        components = SFAVoltageSensor.getAll()
        for component in components:
            current_reading_mv = component.CurrentReading
            enclosure_position = component.EnclosurePosition
            health_state = component.HealthState
            if health_state == 1:
                health_string = "HEALTH_OK"
                health_failure = 0
            elif health_state == 2:
                health_string = "HEALTH_NON_CRITICAL"
                health_failure = 1
            elif health_state == 3:
                health_string = "HEALTH_CRITICAL"
                health_failure = 1
            raw_location = str(component.Location)
            stripped_location = raw_location.strip()
            location = stripped_location.replace(" ", "_")
            over_volt_fail_raw = component.OverVoltageFailure
            if not over_volt_fail_raw:
                over_volt_fail = 0
            else:
                over_volt_fail = 1
            over_volt_warn_raw = component.OverVoltageWarning
            if not over_volt_warn_raw:
                over_volt_warn = 0
            else:
                over_volt_warn = 1
            under_volt_fail_raw = component.UnderVoltageFailure
            if not under_volt_fail_raw:
                under_volt_fail = 0
            else:
                under_volt_fail = 1
            under_volt_warn_raw = component.UnderVoltageWarning
            if not under_volt_warn_raw:
                under_volt_warn = 0
            else:
                under_volt_warn = 1
            print('sfa_voltage_sensor_health,unit=' + unit_name + ',enclosure_position=' + str(enclosure_position) + ',location=' + str(location) + ' health_failure=' + str(health_failure) + ',health_state_string="' + health_string + '",current_reading_mv=' + str(current_reading_mv) + ',over_volt_fail=' + str(over_volt_fail) + ',over_volt_warn=' + str(over_volt_warn) + ',under_volt_fail=' + str(under_volt_fail) + ',under_volt_warn=' + str(under_volt_warn))

        # Get SEP Info
        components = SFASEP.getAll()
        for component in components:
            enclosure_position = component.EnclosurePosition
            raw_failure = component.Failure
            if not raw_failure:
                is_failed = 0
            else:
                is_failed = 1
            health_state = component.HealthState
            if health_state == 1:
                health_string = "HEALTH_OK"
                health_failure = 0
            elif health_state == 2:
                health_string = "HEALTH_NON_CRITICAL"
                health_failure = 1
            elif health_state == 3:
                health_string = "HEALTH_CRITICAL"
                health_failure = 1
            raw_location = str(component.Location)
            stripped_location = raw_location.strip()
            location = stripped_location.replace(" ", "_")
            raw_present = component.Present
            if not raw_present:
                is_present = 0
            else:
                is_present = 1
            print('sfa_sep_health,unit=' + unit_name + ',enclosure_position=' + str(enclosure_position) + ',location=' + str(location) + ' health_failure=' + str(health_failure) + ',health_state_string="' + health_string + '",is_present=' + str(is_present) + ',is_failed=' + str(is_failed))

        # Get SAS Connector Information
        components = SFASASConnector.getAll()
        for component in components:
            enclosure_position = component.EnclosurePosition
            raw_fault = component.Fault
            if not raw_fault:
                is_faulted = 0
            else:
                is_faulted = 1
            health_state = component.HealthState
            if health_state == 1:
                health_string = "HEALTH_OK"
                health_failure = 0
            elif health_state == 2:
                health_string = "HEALTH_NON_CRITICAL"
                health_failure = 1
            elif health_state == 3:
                health_string = "HEALTH_CRITICAL"
                health_failure = 1
            ses_status = component.SESStatus
            if ses_status == 1:
                ses_state = "SES_STATUS_OK"
            elif ses_status == 2:
                ses_state = "SES_STATUS_CRITICAL"
            elif ses_status == 3:
                ses_state = "SES_STATUS_NON_CRITICAL"
            elif ses_status == 4:
                ses_state = "SES_STATUS_UNRECOVERABLE"
            elif ses_status == 5:
                ses_state = "SES_STATUS_NOT_INSTALLED"
            elif ses_status == 6:
                ses_state = "SES_STATUS_UNKNOWN"
            elif ses_status == 7:
                ses_state = "SES_STATUS_NOT_ AVAILABLE"
            elif ses_status == 8:
                ses_state = "SES_STATUS_NO_ACCESS"
            raw_name = component.Name
            stripped_name = raw_name.strip()
            name = stripped_name.replace(" ", "_")
            print('sfa_sas_connector_health,unit=' + unit_name + ',enclosure_position=' + str(enclosure_position) + ',name=' + str(name) + ' health_failure=' + str(health_failure) + ',health_state_string="' + health_string + '",is_faulted=' + str(is_faulted) + ',ses_status="' + str(ses_state) + '"')

        # Get Internal Disk Information
        components = SFAInternalDiskDrive.getAll()
        for component in components:
            enclosure_position = component.EnclosureIndex
            raw_mirror_state = component.MirrorState
            if raw_mirror_state == 1:
                mirror_string = "MIRROR_STATE_MEMBER"
                mirror_not_healthy = 0
            elif raw_mirror_state == 2:
                mirror_string = "MIRROR_STATE_FAILED"
                mirror_not_healthy = 1
            elif raw_mirror_state == 3:
                mirror_string = "MIRROR_STATE_STOPPED"
                mirror_not_healthy = 1
            elif raw_mirror_state == 4:
                mirror_string = "MIRROR_STATE_COPYING"
                mirror_not_healthy = 1
            elif raw_mirror_state == 5:
                mirror_string = "MIRROR_STATE_MISSING"
                mirror_not_healthy = 1
            elif raw_mirror_state == 7:
                mirror_string = "MIRROR_STATE_NOTMIR"
                mirror_not_healthy = 1
            elif raw_mirror_state == 7:
                mirror_string = "MIRROR_STATE_SYSDISK"
                mirror_not_healthy = 1
            elif raw_mirror_state == 8:
                mirror_string = "MIRROR_STATE_NOTPRESENT"
                mirror_not_healthy = 1
            elif raw_mirror_state == 9:
                mirror_string = "MIRROR_STATE_SPARE"
                mirror_not_healthy = 1
            elif raw_mirror_state == 10:
                mirror_string = "MIRROR_STATE_BADMIR"
                mirror_not_healthy = 1
            ses_status = component.SESStatus
            if ses_status == 1:
                ses_state = "SES_STATUS_OK"
            elif ses_status == 2:
                ses_state = "SES_STATUS_CRITICAL"
            elif ses_status == 3:
                ses_state = "SES_STATUS_NON_CRITICAL"
            elif ses_status == 4:
                ses_state = "SES_STATUS_UNRECOVERABLE"
            elif ses_status == 5:
                ses_state = "SES_STATUS_NOT_INSTALLED"
            elif ses_status == 6:
                ses_state = "SES_STATUS_UNKNOWN"
            elif ses_status == 7:
                ses_state = "SES_STATUS_NOT_ AVAILABLE"
            elif ses_status == 8:
                ses_state = "SES_STATUS_NO_ACCESS"
            raw_drive_type = component.Type
            if raw_drive_type == 1:
                drive_type = "SYSTEM"
            elif raw_drive_type == 2:
                drive_type = "APPLICATION"
            position = component.Position
            print('sfa_internaldisk_health,unit=' + unit_name + ',enclosure_position=' + str(enclosure_position) + ',position=' + str(position) + ' mirror_not_healthy=' + str(mirror_not_healthy) + ',mirror_string="' + mirror_string + '",ses_state="' + ses_state + '"')

        # Get Stack Information
        components = SFAVirtualMachine.getAll()
        for component in components:
            con_index = component.ControllerIndex
            child_state = component.ChildHealthState
            if child_state == 1:
                child_failure = 0
            elif child_state == 2:
                child_failure = 1
            elif child_state == 3:
                child_failure = 1
            health_state = component.HealthState
            if health_state == 1:
                health_failure = 0
            elif health_state == 2:
                health_failure = 1
            elif health_state == 3:
                health_failure = 1
            raw_is_running = component.IsRunning
            if not raw_is_running:
                running = 0
            else:
                running = 1
            vm_name = component.Name
            vp_index = component.VirtualProcessorIndex
            if vm_name:
                print('sfa_vm_health,unit=' + unit_name + ',controller=' + str(con_index) + ',ap=' + str(vp_index) + ',name=' + vm_name + ' is_running=' + str(running) + ',fault_status=' + str(health_failure) + ',child_fault_status=' + str(child_failure))
            
        # destroy API context
        APIDisconnect()

    except:
        exc_type, exc_value, tb = sys.exc_info()
        if tb is not None:
            prev = tb
            curr = tb.tb_next
        while curr is not None:
            prev = curr
            curr = curr.tb_next
        print(prev.tb_frame.f_locals)
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
        pull_sfa_health(controller_ip,controller_user,controller_password)

# Allow other programs to source this one as a library
if __name__ == '__main__':
    try:
        main()
    finally:
        sys.exit(0)
