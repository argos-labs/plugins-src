# from winreg import ConnectRegistry, OpenKey, EnumKey, QueryValueEx, \
#     HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER
#
# # aKey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
# # aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
# aKey = r"Control Panel\Desktop\WindowMetrics\AppliedDPI"
# aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
#
# print(r"*** Reading from %s ***" % aKey)
#
# aKey = OpenKey(aReg, aKey)
# # asubkey = OpenKey(aKey, 'AppliedDPI')
# val = QueryValueEx(aKey, 96)
# print(val)
#
# # for i in range(1024):
# #     try:
# #         asubkey_name = EnumKey(aKey, i)
# #         asubkey = OpenKey(aKey, asubkey_name)
# #         val = QueryValueEx(asubkey, "DisplayName")
# #         print(val)
# #     except EnvironmentError:
# #         break
#


import os, winreg
proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()

if proc_arch == 'x86' and not proc_arch64:
    arch_key = 0
elif proc_arch == 'x86' or proc_arch == 'amd64':
    arch_key = winreg.KEY_WOW64_64KEY
else:
    raise Exception("Unhandled arch: %s" % proc_arch)

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                     r"Control Panel\Desktop\WindowMetrics", 0,
                     winreg.KEY_READ | arch_key)
try:
    dn = winreg.QueryValueEx(key, 'AppliedDPI')
    print(dn[0]//96*100)
finally:
    key.Close()

    # key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | arch_key)
    # for i in range(0, winreg.QueryInfoKey(key)[0]):
    #     skey_name = winreg.EnumKey(key, i)
    #     skey = winreg.OpenKey(key, skey_name)
    #     try:
    #         dn = winreg.QueryValueEx(skey, 'DisplayName')
    #         print(dn[0])
    #     except OSError as e:
    #         if e.errno == errno.ENOENT:
    #             # DisplayName doesn't exist in this skey
    #             pass
    #     finally:
    #         skey.Close()
