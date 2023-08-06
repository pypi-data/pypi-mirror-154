#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 10:01
# @Author  : chaolin
# @File    : CanoeTest.py
# @Software: PyCharm

import os
from time import sleep
from win32com.client.connect import *
import traceback
from platform8155.conf.read_config import readConfig
from logzero import logger

class CanoeSync(object):
    """Wrapper class for CANoe Application object"""
    Started = False
    Stopped = False

    def __init__(self):
        # Start the Flexray and Can
        canoe = win32com.client.Dispatch("CANoe.Application")
        self.System = canoe.System
        self.fr = canoe.GetBus("Flexray")
        self.can = canoe.GetBus("CAN")
        self.lin = canoe.GetBus("LIN")
        # a = SetupCanoe()
        # a.init_canoe()


    def fr_get_signal_value(self, pdu, signal):
        sig = self.fr.GetSignal(0, pdu, signal)
        return sig.Value

    def fr_send_signal_value(self, pdu, signal, value):
        sig = self.fr.GetSignal(0, pdu, signal)
        sig.Value = value
        sleep(1)
        if sig.Value == value:
            return True
        else:
            return False

    def can_get_signal_value(self, message, signal):
        sig = self.can.GetSignal(0, message, signal)
        return sig.Value

    def can_send_signal_value(self, message, signal, value):
        sig = self.can.GetSignal(0, message, signal)
        sig.Value = value
        sleep(1)
        if sig.Value == value:
            return True
        else:
            return False

    def lin_get_signal_value(self, message, signal):
        sig = self.lin.GetSignal(0, message, signal)
        return sig.Value

    def lin_send_signal_value(self, message, signal, value):
        sig = self.lin.GetSignal(0, message, signal)
        sig.Value = value
        sleep(1)
        if sig.Value == value:
            return True
        else:
            return False

    def change_UsgModSts(self, state):
        sig = self.fr.GetSignal(0, readConfig.get_signal('DHU_USAGEMODE_GROUP'), readConfig.get_signal('DHU_USAGEMODE_SIGNAL'))
        sig_value_pre = sig.Value
        sig.Value = state
        if (sig_value_pre == 0.0) & (state == 13.0):
            sleep(30)
        else:
            sleep(5)
        if sig.Value == state:
            return True
        else:
            return False

    def change_car_config(self, variable_name, variable_value):
        param = self.System.Namespaces("CEM::CC::Param")
        variable = param.Variables(variable_name)
        variable.Value = variable_value
        sleep(1)
        if variable.Value == variable_value:
            return True
        else:
            return False

    def change_car_config_2410(self, variable_name, variable_value):
        param = self.System.Namespaces("_SPACommon::CarConfig::Parameters")
        variable = param.Variables(variable_name)
        variable.Value = variable_value
        sleep(1)
        if variable.Value == variable_value:
            return True
        else:
            return False


    def change_car_config_2410_ext(self, variable_name, variable_value):
        param = self.System.Namespaces("_SPACommon::CarConfigExt::Parameters")
        variable = param.Variables(variable_name)
        variable.Value = variable_value
        sleep(1)
        if variable.Value == variable_value:
            return True
        else:
            return False




canoe_sync = CanoeSync()

#if __name__ == '__main__':
# a = CanoeSync()
# r = a.fr_send_signal_value("CEMBackBoneSignalIpdu01", "UsgModSts", 0.0)
# r = a.fr_get_signal_value("CEMBackBoneSignalIpdu01", "UsgModSts")
# r = a.can_get_signal_value("IHUInfoCanFr02", "FaderLvl")
# r = a.can_send_signal_value("AUDInfoCanFr01", "FaderLvlSts", 2.0)
# r = a.can_get_signal_value("AUDInfoCanFr01", "FaderLvlSts")
# r = a.lin_get_signal_value("CCSMLIN19Fr2_LIN19", "FanLvl_LIN19")
# print(r)
# r = a.lin_send_signal_value("CCSMLIN19Fr2_LIN19", "FanLvl_LIN19", 2.0)
# print(r)
# a.change_UsgModSts(13.0)
# a.change_car_config_2410("CC001_VEHICLE_TYPE", 3)
# r = a.change_car_config_1910("CC023_CRUISE_CONTROL", 3)
# a = SetupCanoe()
# a.init_canoe()
