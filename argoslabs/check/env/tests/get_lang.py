# from __future__ import print_function
# # import wx
# import ctypes
# import locale
# from ctypes.wintypes import (
#     DWORD,
#     WORD,
#     INT,
#     WCHAR,
#     HANDLE
# )
#
# LOCALE_NAME_MAX_LENGTH = 85
#
# LOCALE_INVARIANT = 0x007F
# LOCALE_USER_DEFAULT =- 0x0400
# LOCALE_SYSTEM_DEFAULT = 0x0800
#
# KL_NAMELENGTH = 9
#
# kernel32 = ctypes.windll.Kernel32
# user32 = ctypes.windll.User32
#
#
# if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
#     ULONG_PTR = ctypes.c_ulong
# elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
#     ULONG_PTR = ctypes.c_ulonglong
# else:
#     ULONG_PTR =ctypes. c_ulong
#
#
# LCID = DWORD
# LANGID = WORD
# GEOTYPE = DWORD
# HKL = HANDLE
# DWORD_PTR = ULONG_PTR
# PWSTR = ctypes.POINTER(WCHAR)
#
#
# # LCID GetUserDefaultLCID();
# GetUserDefaultLCID = kernel32.GetUserDefaultLCID
# GetUserDefaultLCID.restype = LCID
#
# user_default_lcid = GetUserDefaultLCID()
# print('kernel32.GetUserDefaultLCID:', user_default_lcid)
# if user_default_lcid in locale.windows_locale:
#     print(
#         'kernel32.GetUserDefaultLCID canonical name:',
#         locale.windows_locale[user_default_lcid]
#     )
#
# else:
#     print('kernel32.GetUserDefaultLCID canonical name: None')
# # LCID GetSystemDefaultLCID();
# GetSystemDefaultLCID = kernel32.GetSystemDefaultLCID
# GetSystemDefaultLCID.restype = LCID
#
# system_default_lcid = GetSystemDefaultLCID()
# print()
# print('kernel32.GetSystemDefaultLCID:', system_default_lcid)
# if system_default_lcid in locale.windows_locale:
#     print(
#         'kernel32.GetSystemDefaultLCID canonical name:',
#         locale.windows_locale[system_default_lcid]
#     )
#
# else:
#     print('kernel32.GetSystemDefaultLCID canonical name: None')
# # int GetUserDefaultLocaleName(
# #   LPWSTR lpLocaleName,
# #   int    cchLocaleName
# # );
# GetUserDefaultLocaleName = kernel32.GetUserDefaultLocaleName
# GetUserDefaultLocaleName.restype = INT
#
# user_locale_name = (WCHAR * LOCALE_NAME_MAX_LENGTH)()
# GetUserDefaultLocaleName(
#     ctypes.byref(user_locale_name),
#     LOCALE_NAME_MAX_LENGTH
# )
#
# print()
#
# print('kernel32.GetUserDefaultLocaleName:', user_locale_name.value)
#
# # int GetSystemDefaultLocaleName(
# #   LPWSTR lpLocaleName,
# #   int    cchLocaleName
# # );
# GetSystemDefaultLocaleName = kernel32.GetSystemDefaultLocaleName
# GetSystemDefaultLocaleName.restype = INT
#
# system_locale_name = (WCHAR * LOCALE_NAME_MAX_LENGTH)()
# GetSystemDefaultLocaleName(
#     ctypes.byref(system_locale_name),
#     LOCALE_NAME_MAX_LENGTH
# )
#
# print('kernel32.GetSystemDefaultLocaleName:', system_locale_name.value)
#
# # LANGID GetUserDefaultUILanguage();
# GetUserDefaultUILanguage = kernel32.GetUserDefaultUILanguage
# GetUserDefaultUILanguage.restype = LANGID
#
# user_default_ui_language = GetUserDefaultUILanguage()
#
# print()
# print('kernel32.GetUserDefaultUILanguage:', user_default_ui_language)
# if user_default_ui_language in locale.windows_locale:
#     print(
#         'kernel32.GetUserDefaultUILanguage canonical name:',
#         locale.windows_locale[user_default_ui_language]
#     )
#
# else:
#     print('kernel32.GetUserDefaultUILanguage canonical name: None')
#
#
# print()
# # LANGID GetSystemDefaultUILanguage();
# GetSystemDefaultUILanguage = kernel32.GetSystemDefaultUILanguage
# GetSystemDefaultUILanguage.restype = LANGID
#
# system_default_ui_language = GetSystemDefaultUILanguage()
#
# print('kernel32.GetSystemDefaultUILanguage:', system_default_ui_language)
#
# if system_default_ui_language in locale.windows_locale:
#     print(
#         'kernel32.GetSystemDefaultUILanguage canonical name:',
#         locale.windows_locale[system_default_ui_language]
#     )
# else:
#     print('kernel32.GetSystemDefaultUILanguage canonical name: None')
#
#
# # LANGID GetUserDefaultLangID();
# GetUserDefaultLangID = kernel32.GetUserDefaultLangID
# GetUserDefaultLangID.restype = LANGID
#
# user_default_langid = GetUserDefaultLangID()
#
# print()
# print('kernel32.GetUserDefaultLangID:', user_default_langid)
#
# if user_default_langid in locale.windows_locale:
#     print(
#         'kernel32.GetUserDefaultLangID canonical name:',
#         locale.windows_locale[user_default_langid]
#     )
#
# else:
#     print('kernel32.GetUserDefaultLangID canonical name: None')
#
# # LANGID GetSystemDefaultLangID();
# GetSystemDefaultLangID = kernel32.GetSystemDefaultLangID
# GetSystemDefaultLangID.restype = LANGID
#
# system_default_langid = GetSystemDefaultLangID()
# print()
# print('kernel32.GetSystemDefaultLangID:', system_default_langid)
#
# if system_default_langid in locale.windows_locale:
#     print(
#         'kernel32.GetSystemDefaultLangID canonical name:',
#         locale.windows_locale[system_default_langid]
#     )
# else:
#     print('kernel32.GetSystemDefaultLangID canonical name: None')
#
#
# # HKL GetKeyboardLayout(
# #   DWORD idThread
# # );
#
# GetKeyboardLayout = user32.GetKeyboardLayout
# GetKeyboardLayout.restype = HKL
#
# def LOWORD(l):
#     return WORD(DWORD_PTR(l).value & 0xffff)
#
#
# keyboard_layout = GetKeyboardLayout(DWORD(0))
# keyboard_langid = LANGID(LOWORD(keyboard_layout).value)
# print()
# print('user32.GetKeyboardLayout:', keyboard_langid.value)
# # BOOL GetKeyboardLayoutNameW(
# #   LPWSTR pwszKLID
# # );
#
# if keyboard_langid.value in locale.windows_locale:
#     print(
#         'user32.GetKeyboardLayout canonical name:',
#         locale.windows_locale[keyboard_langid.value]
#     )
#
# else:
#     print('user32.GetKeyboardLayout canonical name: None')
#
#
# wx_default = wx.Locale.GetSystemLanguage()
# print('\n')
# print('wx.Locale.GetSystemLanguage: ' + str(wx_default))
#
# lang_info = wx.Locale.GetLanguageInfo(wx_default)
#
# print('wx.LanguageInfo.LocaleName:', lang_info.GetLocaleName())
# print('wx.LanguageInfo.CanonicalName:', lang_info.CanonicalName)
# print('wx.LanguageInfo.Description:', lang_info.Description)
# print('wx.LanguageInfo.Language:', lang_info.Language)
