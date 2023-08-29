import os
import glob
import base64
import pprint


# ==========================================================================
def _get_icon(mod_spec):
    md = os.path.abspath(os.path.dirname(__file__))
    icon_f = None
    for f in glob.glob(os.path.join(md, 'icon.*')):
        icon_f = f
        break  # 첫번째 아이콘만 처리
    if not icon_f:
        return False
    mod_spec['icon_filename'] = os.path.basename(icon_f)
    with open(icon_f, 'rb') as ifp:
        rb = ifp.read()
    icon = base64.b64encode(rb)
    mod_spec['icon'] = icon.decode('ascii')
    return True


# ==========================================================================
def _save_icon(mod_spec, icon_name):
    wb = base64.b64decode(mod_spec['icon'])
    with open(icon_name, 'wb') as ofp:
        ofp.write(wb)


################################################################################
if __name__ == '__main__':
    mod_spec = {
        'name': 'mod_spec test',
    }
    _get_icon(mod_spec)
    pprint.pprint(mod_spec)
    _save_icon(mod_spec, 'icon2.png')

