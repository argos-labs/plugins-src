
import sys
from argoslabs.storage.boxii.tests.test_me import TU
from unittest import TestLoader, TextTestRunner


################################################################################
if __name__ == "__main__":
    suite = TestLoader().loadTestsFromTestCase(TU)
    result = TextTestRunner(verbosity=2).run(suite)
    ret = not result.wasSuccessful()
    sys.exit(int(ret))
