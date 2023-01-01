"""
====================================
 :mod:`argoslabs.dropbox.api`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Dropbox API
"""
# Authors
# ===========
#
# * Irene Cho
#
# --------
#
#  * [2021/06/04]
#     - starting

################################################################################
import os
import sys
import dropbox
import warnings
from io import StringIO

from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path

warnings.filterwarnings(action="ignore", message="unclosed",
                        category=ResourceWarning)


################################################################################
@func_log
def tab(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        token = argspec.token
        dbx = dropbox.Dropbox(oauth2_access_token=token)
        if argspec.directory == '/':
            d_location = ''
        else:
            d_location = argspec.directory
        if argspec.op == 'File/Folder Lists':
            with StringIO() as outst:
                t = dbx.files_list_folder(d_location).entries
                outst.write('type,name,path,date_modified,size')
                outst.write('\n')
                for ent in t:
                    if isinstance(ent, dropbox.files.FolderMetadata):
                        outst.write(
                            'folder' + ',' + ent.name + ',' + ent.path_lower + ',' + ',')
                    else:
                        outst.write(
                            'file' + ',' + ent.name + ',' + ent.path_lower + ',' + str(
                                ent.client_modified) + ',' + str(ent.size))
                    outst.write('\n')
                print(outst.getvalue(), end='')
        elif argspec.op == 'Upload Files':
            cnt = 0
            for ent in argspec.files:
                try:
                    with open(ent, "rb") as f:
                        location = d_location + '/' + os.path.basename(ent)
                        _ = dbx.files_upload(f.read(), location, mute=True)
                        f.close()
                    cnt += 1
                except Exception as err:
                    msg = str(err)
                    mcxt.logger.error(msg)
                    sys.stderr.write('%s%s' % (msg, os.linesep))
                    return 9
            print(f'Successfully uploaded {cnt} files', end='')
        elif argspec.op == 'Download Files/Folder':
            res = []
            if argspec.fdirectory:
                for i in argspec.fdirectory:
                    res.append(dbx.files_get_metadata(i))
            if argspec.directory:
                temp = dbx.files_list_folder(d_location).entries
                res += temp
            for ent in res:
                try:
                    with StringIO() as outst:
                        if isinstance(ent, dropbox.files.FolderMetadata):
                            location = os.path.join(argspec.output,
                                                    ent.name + '.zip')
                            _ = dbx.files_download_zip_to_file(location,
                                                               ent.path_lower)
                        else:
                            location = os.path.join(argspec.output, ent.name)
                            _ = dbx.files_download_to_file(location, ent.id)
                        outst.write(location)
                        outst.write('\n')
                        print(outst.getvalue(), end='')
                except Exception as err:
                    msg = str(err)
                    mcxt.logger.error(msg)
                    sys.stderr.write('%s%s' % (msg, os.linesep))
                    return 9
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
            group='9',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Dropbox',
            icon_path=get_icon_path(__file__),
            description='Managing a dropbox',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # ##################################### for app optional parameters
        mcxt.add_argument('op', display_name='OP Type', help='operation types',
                          choices=['File/Folder Lists', 'Upload Files',
                                   'Download Files/Folder'])
        # ----------------------------------------------------------------------
        mcxt.add_argument('token', display_name='Token', help='Token',
                          input_method='password')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--files', display_name='Files to Upload',
                          input_method='fileread', action='append',
                          help='An absolute filepath to upload to dropbox')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--directory', display_name='Dropbox Folder Location',
                          help='Dropbox folder location')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--fdirectory', display_name='Dropbox File Location',
                          help='Dropbox file location', action='append')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--output', display_name='Output Path',
                          input_method='folderwrite',
                          help='An absolute filepath to save a file')
        argspec = mcxt.parse_args(args)
        return tab(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
