import unittest

from sk import load_data

class TestLogisticRegression(unittest.TestCase):
    def test_load_data(self):
        data, target = load_data()
        assert data.shape == (1797, 64)

# How to run:
# 1. Change to the working folder:
# 2. Execute the tests:
#       pytest