
import unittest

from . import main

class MyTests(unittest.TestCase):
    def test_my_method(self):
        # ... test logic ...
        pass
    
class TestDriverMain(unittest.TestCase):
    def test_main_invocation(self):
        args = '/home/builder/src/misc/tests/benchmarks/miconic/domain.pddl /home/builder/src/misc/tests/benchmarks/miconic/s1-0.pddl --search "astar(lmcut())"'
        main.main()
        pass
