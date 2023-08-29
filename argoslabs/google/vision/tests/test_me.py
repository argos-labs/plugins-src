
"""
====================================
 :mod:`argoslabs.google.vision`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/07]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/11/05]
#     - Debug: module 'google.cloud.vision' has no attribute 'types'
#  * [2020/03/07]
#     - Chagne group "google" => "Google"
#  * [2019/10/31]
#     - add ocr output type option (--ocr-output)
#  * [2019/10/16]
#     - add opencv result
#  * [2019/09/24]
#     - 'Text' or 'Full Text' => 'OCR' internally with 'Full Text'
#  * [2019/09/13]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.google.vision import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    CRED = 'vision-4ca68bb81fbf.json'

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_failure(self):
        try:
            _ = main('-vvv')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0020_failure(self):
        try:
            _ = main('invalid-json')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        try:
            _ = main('invalid-json', 'invalid-op')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0030_failure(self):
        try:
            r = main(TU.CRED, 'invalid-op', 'invalid-img')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

        try:
            r = main(TU.CRED, 'OCR', 'invalid-img')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0080_invalid_credential(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main('invalid.json', 'OCR', 'text-01.png',
                     '--output-image', 'text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.endswith('to The Economist'))

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0100_text_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'OCR', 'text-01.png',
                     '--output-image', 'text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.endswith('to The Economist'))

            r = main(TU.CRED, 'OCR', 'text-01.png',
                     '--ocr-output', 'page',
                     '--output-image', 'text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.split('\n')[-1] ==
                            'Choose your subscription to The Economist')

            r = main(TU.CRED, 'OCR', 'text-01.png',
                     '--ocr-output', 'paragraph',
                     '--output-image', 'text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.split('\n')[-1] ==
                            'Choose your subscription to The Economist')

            r = main(TU.CRED, 'OCR', 'text-01.png',
                     '--ocr-output', 'word',
                     '--output-image', 'text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.split('\n')[-1] ==
                            'Economist')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0110_text_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'OCR', 'text-02.png',
                     '--output-image', 'text-02.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.endswith('烈士家属代表。'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0120_text_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'OCR', 'text-03.png',
                     '--output-image', 'text-03.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.endswith('立たされています。'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0130_text_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'OCR', 'text-04.png',
                     '--output-image', 'text-04.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.endswith('이 제공됩니다.'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0140_full_text_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'OCR', 'full-text-01.png',
                     '--output-image', 'full-text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.endswith('Arch Otolaryngol Head Neck Surg. 2003 : 129 : 215-218'))

            r = main(TU.CRED, 'OCR', 'full-text-01.png',
                     '--ocr-output', 'page',
                     '--output-image', 'full-text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.split('\n')[0] == 'Urokinase - Type Plasminogen '
                'Activator Receptor Expression in Adenoid Cystic Carcinoma of the Skull Base')

            r = main(TU.CRED, 'OCR', 'full-text-01.png',
                     '--ocr-output', 'paragraph',
                     '--output-image', 'full-text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.split('\n')[-1] == 'Arch Otolaryngol Head Neck Surg . 2003 : 129 : 215-218')

            r = main(TU.CRED, 'OCR', 'full-text-01.png',
                     '--ocr-output', 'word',
                     '--output-image', 'full-text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.split('\n')[0] == 'Urokinase')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0145_full_text_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'OCR', 'MyReport_kishi_approve-01.png',
                     '--output-image', 'MyReport_kishi_approve-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            # self.assertTrue(out.endswith('08/09/2019\nNo'))
            self.assertTrue(out.endswith('$36.46\nNo'))

            r = main(TU.CRED, 'OCR', 'MyReport_kishi_approve-01.png',
                     '--ocr-output', 'page',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.split('\n')[0] == 'MEAL - NUL GROUP')

            r = main(TU.CRED, 'OCR', 'MyReport_kishi_approve-01.png',
                     '--ocr-output', 'paragraph',
                     # '--output-image', 'full-text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.split('\n')[-1] == 'No')

            r = main(TU.CRED, 'OCR', 'MyReport_kishi_approve-01.png',
                     '--ocr-output', 'word',
                     # '--output-image', 'full-text-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.split('\n')[0] == 'MEAL')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0150_full_text_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'OCR', 'full-text-02.png',
                     '--output-image', 'full-text-02.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.endswith('《小学校的钟声》里他运用意识流形态技法,勾勒出离开故乡之后与'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0160_full_text_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'OCR', 'full-text-03.jpg',
                     '--output-image', 'full-text-03.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            # self.assertTrue(out.endswith('の概念が重視されるべきであることが分かった。\n-80-'))
            self.assertTrue(
                out.endswith('て「スピード」や「度合い」の概念が重視されるべきであることが分かった。\n- 80-') or
                out.endswith('て「スピード」や「度合い」の概念が重視されるべきであることが分かった。\n- 80 -')
            )
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0170_full_text_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'OCR', 'full-text-04.png',
                     '--output-image', 'full-text-04.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out.endswith('1. 최종논문에 저자의 소속/ 성함/ 논문정보를 모두 기제하였는가?(국문/영문)'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0180_face_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'Face', 'faces-01.jpg',
                     '--output-image', 'faces-01.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out == '2')

            r = main(TU.CRED, 'Face', 'faces-02.jpg',
                     '--output-image', 'faces-02.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out == '1')

            r = main(TU.CRED, 'Face', 'faces-03.jpg',
                     '--output-image', 'faces-03.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out == '3')

            r = main(TU.CRED, 'Face', 'faces-04.png',
                     '--output-image', 'faces-04.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            self.assertTrue(out in ('8', '9'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0190_label_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'Label', 'label-01.jpg',
                     # '--output-image', 'label-01.out.jpg',  # no output image for Label
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] in ('Dog', 'Plant', 'Sky'))

            r = main(TU.CRED, 'Label', 'label-02.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] in ('Dog', 'Brown'))

            r = main(TU.CRED, 'Label', 'label-03.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] in ('Outerwear', 'Product', 'Blue'))

            r = main(TU.CRED, 'Label', 'label-04.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] in
                            ('Automotive parking light', 'Motor vehicle', 'Car', 'Road'))
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0200_landmark_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'Landmark', 'landmark-01.jpg',
                     '--output-image', 'landmark-01.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            # self.assertTrue(rows[1][0] == 'Champ de Mars')
            self.assertTrue(len(rows) == 3)
            r = main(TU.CRED, 'Landmark', 'landmark-02.jpg',
                     '--output-image', 'landmark-02.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Taj Mahal')

            r = main(TU.CRED, 'Landmark', 'landmark-03.jpg',
                     '--output-image', 'landmark-03.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Piazza dei Miracoli')

            r = main(TU.CRED, 'Landmark', 'landmark-04.jpg',
                     '--output-image', 'landmark-04.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
            # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Gwanghwamun Gate')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0210_logo_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'Logo', 'logo-01.jpg',
                     '--output-image', 'logo-01.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Google')

            r = main(TU.CRED, 'Logo', 'logo-02.jpg',
                     '--output-image', 'logo-02.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'IBM')

            r = main(TU.CRED, 'Logo', 'logo-03.png',
                     '--output-image', 'logo-03.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Apple Inc.')

            r = main(TU.CRED, 'Logo', 'logo-04.jpg',
                     '--output-image', 'logo-04.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Nike')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0220_localized_object_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'Localized Object', 'local-01.png',
                     '--output-image', 'local-01.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Food')

            r = main(TU.CRED, 'Localized Object', 'local-02.jpg',
                     '--output-image', 'local-02.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Bicycle wheel')

            r = main(TU.CRED, 'Localized Object', 'local-03.jpg',
                     '--output-image', 'local-03.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Wheel')

            r = main(TU.CRED, 'Localized Object', 'local-04.png',
                     '--output-image', 'local-04.out.png',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Houseplant')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0230_localized_object_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'Localized Object', 'label-01.jpg',
                     '--output-image', 'label-01.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Dog')

            r = main(TU.CRED, 'Localized Object', 'label-02.jpg',
                     '--output-image', 'label-02.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Dog')

            r = main(TU.CRED, 'Localized Object', 'label-03.jpg',
                     '--output-image', 'label-03.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Tie')

            r = main(TU.CRED, 'Localized Object', 'label-04.jpg',
                     '--output-image', 'label-04.out.jpg',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == 'Car')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # ==========================================================================
    def test0240_dominant_colors_success(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        outfile = 'stdout.txt'
        try:
            r = main(TU.CRED, 'Dominant Colors', 'property-01.jpg',
                     # '--output-image', 'property-01.out.jpg',  # no output image
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile, encoding='utf-8') as ifp:
                out = ifp.read()
                # print(out)
            rows = list()
            with open(outfile, encoding='utf-8') as ifp:
                cr = csv.reader(ifp)
                for row in cr:
                    rows.append(row)
            self.assertTrue(rows[1][0] == '0.01451832801103592')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    # # ==========================================================================
    # def test0250_pdf_text_success(self):
    #     outfile = 'stdout.txt'
    #     try:
    #         r = main(TU.CRED, 'OCR', 'MyReport_kishi_approve.PDF',
    #                  '--output-image', 'MyReport_kishi_approve.out.PDF',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         print(out)
    #         self.assertTrue(out.endswith('to The Economist'))
    #
    #         r = main(TU.CRED, 'OCR', 'MyReport_kishi_approve.PDF',
    #                  '--ocr-output', 'page',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         print(out)
    #         self.assertTrue(out.split('\n')[-1] ==
    #                         'Choose your subscription to The Economist')
    #
    #         r = main(TU.CRED, 'OCR', 'MyReport_kishi_approve.PDF',
    #                  '--ocr-output', 'paragraph',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         print(out)
    #         self.assertTrue(out.split('\n')[-1] ==
    #                         'Choose your subscription to The Economist')
    #
    #         r = main(TU.CRED, 'OCR', 'MyReport_kishi_approve.PDF',
    #                  '--ocr-output', 'word',
    #                  '--outfile', outfile)
    #         self.assertTrue(r == 0)
    #         with open(outfile, encoding='utf-8') as ifp:
    #             out = ifp.read()
    #         print(out)
    #         self.assertTrue(out.split('\n')[-1] ==
    #                         'Economist')
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(True)
    #     finally:
    #         if os.path.exists(outfile):
    #             os.remove(outfile)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
