
import sys
from argoslabs.argos_service_jp.parsehub_api.tests.test_me import TU
from unittest import TestLoader, TextTestRunner


################################################################################
if __name__ == "__main__":
    suite = TestLoader().loadTestsFromTestCase(TU)
    result = TextTestRunner(verbosity=2).run(suite)
    ret = not result.wasSuccessful()
    sys.exit(ret)
