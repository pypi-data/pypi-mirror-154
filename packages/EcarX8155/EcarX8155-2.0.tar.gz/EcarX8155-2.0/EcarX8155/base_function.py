import os, time, subprocess, re
from platform8155.lib.canoe import canoe_sync
from platform8155.conf.read_config import readConfig





class BaseFunction(object):
    def __init__(self):
        pass

    """
        :param module_name : 功能模块
        :param methodName: 方法名字
        :param select_func:
        :param select_zone:
        :param sel_int_val:
        :param method_desc：
        """
    def set_interface_condition(self, module_name, method_name, select_func,
                          select_zone, sel_int_val, method_desc):
        os.system('adb shell am startservice --es module %s --es methodName %s '
          '--ei selectFunction %d --ei selectZone %d --ei selectIntValue %d '
          ' --es methodDesc %s --ez saveLog false com.ecarx.adaptapitext/.TestService' %(module_name, method_name, select_func, select_zone,sel_int_val, method_desc))

        """
        :param module_name : 功能模块
        :param methodName: 方法名字
        :param select_func:
        :param method_desc：
        :return
        """

    # 获取当前开关状态  ON OFF
    def  get_interface_val(self, module_name, method_name, select_func, method_desc):

        os.system('adb shell am startservice --es module %s --es methodName %s '
                  '--ei selectFunction %d --es methodDesc %s '
                  '--ez saveLog true com.ecarx.adaptapitext/.TestService' %(module_name, method_name, select_func, method_desc))

        time.sleep(1)

        # 获取当前值进行结果判断
        command = 'adb shell cat /storage/emulated/0/AdaptApiTest/AdaptApiTestLog.log'
        res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, encoding='utf-8')  # 使用管道
        read_result = str(res.stdout.readlines())  # 获取输出结果

        temp = re.split(r'\\t|\\n', read_result)  # 去掉\t \n
        sn_str = ''.join(temp).replace(',', '').replace(' ', '').replace("'", '')  # 去掉无用符号
        # print(sn_str)
        end_index = sn_str.rfind("=")  # 后面反向查找
        final = sn_str[end_index + 1:len(sn_str) - 1]  # 取到结果
        res.terminate()

        return final
        #获取当前开关状态  ON OFF   需要zone 用这个
    def get_interface_val_zone(self, module_name, method_name, select_func, select_zone, method_desc):
        os.system('adb shell am startservice --es module %s --es methodName %s '
                  '--ei selectFunction %d --ei selectZone %d  --es methodDesc %s '
                  '--ez saveLog true com.ecarx.adaptapitext/.TestService' % (
                      module_name, method_name, select_func, select_zone, method_desc))

        time.sleep(1)

        # 获取当前值进行结果判断
        command = 'adb shell cat /storage/emulated/0/AdaptApiTest/AdaptApiTestLog.log'
        res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, encoding='utf-8')  # 使用管道
        read_result = str(res.stdout.readlines())  # 获取输出结果

        temp = re.split(r'\\t|\\n', read_result)  # 去掉\t \n
        sn_str = ''.join(temp).replace(',', '').replace(' ', '').replace("'", '')  # 去掉无用符号
        # print(sn_str)
        end_index = sn_str.rfind("=")  # 后面反向查找
        final = sn_str[end_index + 1:len(sn_str) - 1]  # 取到结果
        final = final.replace(" ", "")
        res.terminate()

        return final





    def clear_logfile(self):
        os.system('adb shell rm -f /storage/emulated/0/AdaptApiTest/AdaptApiTestLog.log')  # 删除Log避免对个后续结果查找影响

    def check_test_result(self, result_list):
        result_check_na = 0
        result_check_ng = 0
        result_check_ok = 0
        if result_list == []:
            return 'NG'
        for i in result_list:
            if i == 'NA':
                result_check_na += 1
            elif i == 'NG':
                result_check_ng += 1
            elif i == 'OK':
                result_check_ok += 1
        if result_check_na != 0:
            return 'NA'
        elif result_check_ng != 0:
            return 'NG'
        else:
            return 'OK'

    def print_adapt_api_prop(self, module_name, select_func, method_desc):
        print('adb shell am startservice --es module %s --es methodName isFunctionSupported'
                  ' --ei selectFunction %d --es methodDesc %s '
                  '--ez saveLog true com.ecarx.adaptapitext/.TestService' % (module_name, select_func, method_desc))
        time.sleep(1)
        # 获取当前functionstatus 状态
    def get_adapt_api_prop(self,module_name,select_func,method_desc):
        os.system('adb shell am startservice --es module %s --es methodName isFunctionSupported'
                  ' --ei selectFunction %d --es methodDesc %s '
                  '--ez saveLog true com.ecarx.adaptapitext/.TestService' %(module_name, select_func, method_desc))
        time.sleep(1)

        # 获取当前值进行结果判断
        command = 'adb shell cat /storage/emulated/0/AdaptApiTest/AdaptApiTestLog.log'
        res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, encoding='utf-8')  # 使用管道
        read_result = str(res.stdout.readlines())  # 获取输出结果

        temp = re.split(r'\\t|\\n', read_result)  # 去掉\t \n
        sn_str = ''.join(temp).replace(',', '').replace(' ', '').replace("'", '')  # 去掉无用符号
        # print(sn_str)
        end_index = sn_str.rfind("=")  # 后面反向查找
        final = sn_str[end_index + 1:len(sn_str) - 1]  # 取到结果
        res.terminate()

        return final
        #  获取当前functionstatus 状态   需要ZONE用这个方法
    def get_adapt_api_props(self, module_name, select_func, select_zone, method_desc):
        os.system('adb shell am startservice --es module %s --es methodName isFunctionSupported'
                  ' --ei selectFunction %d --ei selectZone %d --es methodDesc %s '
                  '--ez saveLog true com.ecarx.adaptapitext/.TestService' % (
                  module_name, select_func, select_zone, method_desc))
        time.sleep(1)

        # 获取当前值进行结果判断
        command = 'adb shell cat /storage/emulated/0/AdaptApiTest/AdaptApiTestLog.log'
        res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, encoding='utf-8')  # 使用管道
        read_result = str(res.stdout.readlines())  # 获取输出结果

        temp = re.split(r'\\t|\\n', read_result)  # 去掉\t \n
        sn_str = ''.join(temp).replace(',', '').replace(' ', '').replace("'", '')  # 去掉无用符号
        # print(sn_str)
        end_index = sn_str.rfind("=")  # 后面反向查找
        final = sn_str[end_index + 1:len(sn_str) - 1]  # 取到结果
        res.terminate()

        return final








    def set_interface_condition_float(self, module_name, method_name, select_func,
                                      select_zone, sel_int_val, method_desc):
        os.system('adb shell am startservice --es module %s --es methodName %s '
                  '--ei selectFunction %d --ei selectZone %d --ef selectFloatValue %.1f '
                  ' --es methodDesc %s --ez saveLog false com.ecarx.adaptapitext/.TestService' % (
                      module_name, method_name, select_func, select_zone, sel_int_val, method_desc))

    """
        :param module_name : 功能模块
        :param methodName: 方法名字
        :param select_func:
        :param method_desc：
        :return
        """





    def get_interface_val_float(self, module_name, method_name, select_func, select_zone, method_desc):
        os.system('adb shell am startservice --es module %s --es methodName %s '
                  '--ei selectFunction %d --ei selectZone %d  --es methodDesc %s '
                  '--ez saveLog true com.ecarx.adaptapitext/.TestService' % (
                      module_name, method_name, select_func, select_zone, method_desc))

        # 'adb shell am startservice --es module "Car" --es methodName "getCustomizeFunctionValue" --ei selectFunction 0x10060100  ' \
        # '--es methodDesc "空调温度" --ez saveLog true com.ecarx.adaptapitext/.TestService'

        time.sleep(1)

        # 获取当前值进行结果判断
        command = 'adb shell cat /storage/emulated/0/AdaptApiTest/AdaptApiTestLog.log'
        res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, encoding='utf-8')  # 使用管道
        read_result = str(res.stdout.readlines())  # 获取输出结果

        temp = re.split(r'\\t|\\n', read_result)  # 去掉\t \n
        sn_str = ''.join(temp).replace(',', '').replace(' ', '').replace("'", '')  # 去掉无用符号
        # print(sn_str)
        end_index = sn_str.rfind("=")  # 后面反向查找
        final = sn_str[end_index + 1:len(sn_str) - 1]  # 取到结果
        final = final.replace(" ", "")
        res.terminate()

        return final



##################################################################################################################################以上黄宏凯


    '''空调状态初始化'''
    def hvac_init(self):
        # MAX AC恢复为关闭
        base_func.set_interface_condition(readConfig.get_adapt_api('MODULE_NAME'),
                                          readConfig.get_adapt_api('METHOD_NAME_SET'),
                                          readConfig.get_havc_func_ac_max('SELECT_FUNCTION'),
                                          readConfig.get_havc_func_ac_max('SELECT_ZONE'),
                                          readConfig.get_havc_func_ac_max('SELECT_INT_VAL_OFF'),
                                          'Set_AUTO_OFF')
        time.sleep(1)
        #温度恢复22度
        base_func.set_interface_condition_float(readConfig.get_adapt_api('MODULE_NAME'),
                                                readConfig.get_adapt_api('METHOD_NAME_SET_HAVC'),
                                                readConfig.get_havc_func_temp('SELECT_FUNCTION'),
                                                readConfig.get_havc_func_temp('ZONE_ROW_1_LEFT'), 22.0,
                                                "Set_driver_temp_22.0")
        time.sleep(0.5)
        base_func.set_interface_condition_float(readConfig.get_adapt_api('MODULE_NAME'),
                                                readConfig.get_adapt_api('METHOD_NAME_SET_HAVC'),
                                                readConfig.get_havc_func_temp('SELECT_FUNCTION'),
                                                readConfig.get_havc_func_temp('ZONE_ROW_1_RIGHT'), 22.0,
                                                "Set_passer_temp_22.0")
        time.sleep(0.5)
        # 温度同步恢复为关闭
        base_func.set_interface_condition(readConfig.get_adapt_api('MODULE_NAME'),
                                          readConfig.get_adapt_api('METHOD_NAME_SET'),
                                          readConfig.get_havc_func_temp_dual('SELECT_FUNCTION'),
                                          readConfig.get_havc_func_temp_dual('SELECT_ZONE'),
                                          readConfig.get_havc_func_temp_dual('SELECT_INT_VAL_OFF'),
                                          'Set_TEMP_SYNC_OFF')
        time.sleep(0.5)

        # 吹风模式为吹窗
        base_func.set_interface_condition(readConfig.get_adapt_api('MODULE_NAME'),
                                          readConfig.get_adapt_api('METHOD_NAME_SET'),
                                          readConfig.get_havc_func_blowing_mode('SELECT_FUNCTION'),
                                          readConfig.get_havc_func_blowing_mode('ZONE_ROW_1_LEFT'),
                                          readConfig.get_havc_func_blowing_mode('BLOWING_FRONT_WINDOW'),
                                          "Set_blowing_mode_WINDOW")

        # 手动吹风风量恢复4级
        base_func.set_interface_condition(readConfig.get_adapt_api('MODULE_NAME'),
                                          readConfig.get_adapt_api('METHOD_NAME_SET'),
                                          readConfig.get_havc_func_fan_speed('SELECT_FUNCTION'),
                                          readConfig.get_havc_func_fan_speed('ZONE_ROW_1_LEFT'),
                                          0x10020104,
                                          "Set_Fan_Speed_Level_4")

        # AUTO恢复开启状态
        base_func.set_interface_condition(readConfig.get_adapt_api('MODULE_NAME'),
                                          readConfig.get_adapt_api('METHOD_NAME_SET'),
                                          readConfig.get_havc_func_auto('SELECT_FUNCTION'),
                                          readConfig.get_havc_func_auto('ZONE_ROW_1_LEFT'),
                                          readConfig.get_havc_func_auto('SELECT_INT_VAL_ON'),
                                          'Set_AUTO_ON')
        time.sleep(0.5)
        # AC恢复开启状态
        base_func.set_interface_condition(readConfig.get_adapt_api('MODULE_NAME'),
                                          readConfig.get_adapt_api('METHOD_NAME_SET'),
                                          readConfig.get_havc_func_ac('SELECT_FUNCTION'),
                                          readConfig.get_havc_func_ac('SELECT_ZONE'),
                                          readConfig.get_havc_func_ac('SELECT_INT_VAL_ON'),
                                          'Set_AC_ON')


        # 自动吹风风量恢复3级
        base_func.set_interface_condition(readConfig.get_adapt_api('MODULE_NAME'),
                                          readConfig.get_adapt_api('METHOD_NAME_SET'),
                                          readConfig.get_havc_func_auto_fan_speed('SELECT_FUNCTION'),
                                          readConfig.get_havc_func_auto_fan_speed('ZONE_ROW_1_LEFT'),
                                          0x10020102,
                                          "Set_AUTO_Fan_Speed_Level_3")
        time.sleep(0.5)
        #循环模式为外循环
        base_func.set_interface_condition(readConfig.get_adapt_api('MODULE_NAME'),
                                          readConfig.get_adapt_api('METHOD_NAME_SET'),
                                          readConfig.get_havc_func_circulation('SELECT_FUNCTION'),
                                          readConfig.get_havc_func_circulation('SELECT_ZONE'),
                                          readConfig.get_havc_func_circulation('CIRCULATION_OUTSIDE'),
                                          'Set_CIRCULATION_OUTSIDE')
        time.sleep(0.5)




    def fr_signal_val_compare(self, pdu, signal, compare_val):
        try:
            signal_val = canoe_sync.fr_get_signal_value(pdu, signal)
            print(signal_val)
            if signal_val != compare_val:
                return 'OK'
            else:
                return 'NG'
        except Exception as e:
            return 'NG'

















base_func = BaseFunction()