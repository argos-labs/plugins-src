"""
====================================
 :mod:`argoslabs.microsoft.sharepoint`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for SharePoint
"""
#
# Authors
# ===========
#
# * Kyobong An
#
# Change Log
# --------
#
#  * [2021/10/27]
#     - starting
#

################################################################################
import os
import re
import sys
from shareplum import Site
from shareplum import Office365
from shareplum.site import _Folder
from shareplum.site import Version
from alabs.common.util.vvargs import func_log, get_icon_path, ModuleContext, \
    ArgsError, ArgsExit, vv_base64_decode


################################################################################
def _get_safe_filename(fn):
    return "".join([c for c in fn if c.isalpha() or c.isdigit() or
                    c in (' ', '.', '-', '@')]).rstrip()


def _get_safe_next_filename(fn):
    fn, ext = os.path.splitext(fn)
    for n in range(1, 1000000):
        nfn = f'{fn} ({n})' + ext
        if not os.path.exists(nfn):
            return nfn


def get_filepath_in_folder(folder, wildcard):
    file_list = os.listdir(folder)
    re_file_list = []
    for file in file_list:
        if wildcard.match(file):
            re_file_list.append(folder + '\\' + file)
    return re_file_list


def get_filelist(folder, wildcard):
    file_list = []
    for i in range(len(folder.files)):
        if wildcard.match(folder.files[i].get('Name')):
            file_list.append(folder.files[i].get('Name'))
    return file_list


class SharePoint(object):
    def __init__(self, argspec):
        self.argspec = argspec
        self.site = self.access_sharepoint()
        self.folder = self.site.Folder(argspec.folder)
        self.wildcard = re.compile(vv_base64_decode(argspec.wildcard))
        if argspec.target_folder:
            self.target_folder = self.site.Folder(argspec.target_folder)

        if argspec.folder_op == 'Create Folder':
            self.folder_create()
        elif argspec.folder_op == 'Delete Folder':
            self.folder_delete()
        elif argspec.folder_op == 'Upload Folder':
            self.upload(get_filepath_in_folder(self.argspec.out_folder, self.wildcard))
        elif argspec.folder_op == 'Download Folder':
            self.download(get_filelist(self.folder, self.wildcard))
        elif argspec.folder_op == 'Copy Folder':    # folder안에 정규식을 이용해서 이동시킬 파일을 선택
            self.file_copy(get_filelist(self.folder, self.wildcard), self.argspec.file_list_copyname)

        elif argspec.file_op == 'Copy File':    # file_copy(이동시킬파일, 이동시킬때 변경할 이름)
            self.file_copy(self.argspec.file_list_name, self.argspec.file_list_copyname)
        elif argspec.file_op == 'Upload File':
            self.upload(self.argspec.file_list)
        elif argspec.file_op == 'Download File':
            self.download(self.argspec.file_list_name)

        elif argspec.delete_op == 'Delete Folder':
            self.folder_delete()
        elif argspec.delete_op == 'Delete File':
            if self.argspec.file_list_name:
                self.file_delete(self.argspec.file_list_name)
            else:
                self.file_delete(get_filelist(self.folder, self.wildcard))

    def access_sharepoint(self):    # sharepoint 사이트에 접근하는 곳
        authcookie = Office365(self.argspec.url,
                               username=self.argspec.id,
                               password=self.argspec.pw).GetCookies()
        site = Site(self.argspec.site, version=Version.v365, authcookie=authcookie)
        return site

    def folder_create(self):
        self.site.Folder(self.argspec.folder+'/'+self.argspec.new_folder)._create_folder()
        print(f"Create {self.argspec.new_folder} folder")

    def upload(self, file_list):
        for file in file_list:
            with open(file, 'rb') as file_obj:
                self.folder.upload_file(file_obj.read(), os.path.basename(file))
                file_obj.close()
        print(f"Successful upload of {len(file_list)} files")

    def download(self, file_list):
        for file in file_list:
            with open(self.argspec.out_folder+"\\"+file, 'wb') as file_obj:
                file_obj.write(self.folder.get_file(file))
                file_obj.close()
        print(f"Copy {len(file_list)} files")

    def file_copy(self, org_file, copy_file):
        if not copy_file:    # copyfilename이 없을 경우 기존 이름을 사용
            copy_file = org_file

        if len(org_file) != len(copy_file):
            raise Exception('The number of "Files Name" and "Files Rename" is different.')

        if self.target_folder:    # target 폴더가 있을경우에 타겟 폴더에 업로드
            for i in range(len(org_file)):
                self.target_folder.upload_file(self.folder.get_file(org_file[i]), copy_file[i])
        elif self.argspec.file_list_copyname:    # 타겟폴더가 없는 경우. 카피할 폴더에 적용. 대신 copyname이 있어야함.(없을 경우 의미x)
            for i in range(len(org_file)):
                self.folder.upload_file(self.folder.get_file(org_file[i]), copy_file[i])
                # self.folder.delete_file(org_file[i])    # rename을 하려면 기존파일을 삭제하는데. copy 하는게 데이터 손실을 방지
        print(f"Copy {len(org_file)} files")

    def folder_delete(self):
        self.folder.delete_folder(self.argspec.folder)
        print(f"Delete {self.argspec.folder} folder")

    def file_delete(self, file_list):
        for file in file_list:
            self.folder.delete_file(file)

        print(f"Delete {len(file_list)} files")


################################################################################
@func_log
def do_sharepoint(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        SharePoint(argspec)
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='3',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Share Point',
            icon_path=get_icon_path(__file__),
            description='Sharepoint',
    ) as mcxt:
        # ######################################## for app dependent options
        # ----------------------------------------------------------------------
        mcxt.add_argument('--folder-op', show_default=True,
                          input_group='radio=operation;default',
                          choices=['Create Folder', 'Upload Folder', 'Download Folder', 'Copy Folder'],
                          display_name='Folder op',
                          help='Choose which features to use')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--file-op', show_default=True,
                          input_group='radio=operation',
                          choices=['Copy File', 'Upload File', 'Download File'],
                          display_name='File op',
                          help='Choose which features to use')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--delete-op', show_default=True,
                          input_group='radio=operation',
                          choices=['Delete Folder', 'Delete File'],
                          display_name='Delete Folder/File',
                          help='Warning. This function deletes a folder or a specific file.')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--out-folder',
                          display_name='Upload/Save Folder',
                          input_method='folderwrite',
                          help='Folder to upload or save')
        # -----------------------------------------------------------------------
        mcxt.add_argument('--file-list', action='append',
                          display_name='Files Upload',
                          input_method='fileread',
                          help='Files to upload')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--new-folder',
                          input_group='in SharePoint',
                          display_name='New Folder',
                          help='SharePoint New Folder')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--file-list-name', action='append',
                          input_group='in SharePoint',
                          display_name='Files name',
                          help='Select files in SharePoint')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--file-list-copyname', action='append',
                          input_group='in SharePoint',
                          display_name='Files Copy Name',
                          help='Files copy name. ')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--target-folder',
                          input_group='in SharePoint',
                          display_name='Target Folder',
                          help='Move to target folder')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--wildcard', default='',
                          display_name='Src file wildcard',
                          input_method='base64',
                          help='In folder opeartion use matching wildcard.')
        # ##################################### for app dependent parameters
        mcxt.add_argument('url',
                          display_name='Share Point URL',
                          help='Enter your Sharepoint URL')
        # ----------------------------------------------------------------------
        mcxt.add_argument('id',
                          display_name='ID',
                          help='Enter your Sharepoint ID')
        # ----------------------------------------------------------------------
        mcxt.add_argument('pw',
                          input_method='password',
                          display_name='Pass Word',
                          help='Enter your Sharepoint Pass Word')
        # ----------------------------------------------------------------------
        mcxt.add_argument('site',
                          display_name='Site URL',
                          help='Enter your Sharepoint Site URL')
        # ----------------------------------------------------------------------
        mcxt.add_argument('folder',
                          display_name='Site Folder',
                          help='SharePoint Folder')
        argspec = mcxt.parse_args(args)
        return do_sharepoint(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
