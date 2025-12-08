import os
import shlex
import subprocess
import sys

import unittest

from . import configs

DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(DIR))
BENCHMARKS_DIR = os.path.join(REPO, "misc", "tests", "benchmarks")
FAST_DOWNWARD = os.path.join(REPO, "fast-downward.py")
SAS_FILE = os.path.join(REPO, "test.sas")
PLAN_FILE = os.path.join(REPO, "test.plan")
TASK = os.path.join(BENCHMARKS_DIR, "miconic/s1-0.pddl")
DOMAIN = os.path.join(BENCHMARKS_DIR, "miconic/domain.pddl")    

CONFIGS_NOLP = {}
CONFIGS_NOLP.update(configs.default_configs_optimal(core=True, extended=True))
CONFIGS_NOLP.update(configs.default_configs_satisficing(core=True, extended=True))


def escape_list(l):
    return " ".join(shlex.quote(x) for x in l)


def run_plan_script(task, config, debug):
    cmd = [sys.executable, FAST_DOWNWARD, "--plan-file", PLAN_FILE]
    if debug:
        cmd.append("--debug")
    if "--alias" in config:
        assert len(config) == 2, config
        cmd += config + [task]
    else:
        cmd += [task] + config
    print("\nRun: {}:".format(escape_list(cmd)))
    sys.stdout.flush()
    subprocess.check_call(cmd, cwd=REPO)


def translate(task):
    subprocess.check_call([
        sys.executable, FAST_DOWNWARD, "--sas-file", SAS_FILE, "--translate", task], cwd=REPO)


def cleanup():
    os.remove(SAS_FILE)
    
    try:
        os.remove(PLAN_FILE)
    except FileNotFoundError:
        pass

def setup_module(module):
    translate(TASK)


class TestAstar(unittest.TestCase):

        #def test_pass(self):
        #    self.assertTrue(True)
            
        def test_astar(self):
            '''A standard configuration of astar'''
            command = f'{FAST_DOWNWARD} {DOMAIN} {TASK} --search "astar(lmcut())"'
            result = subprocess.run(command, 
                                    shell=True, 
                                    capture_output=True)
            self.assertEqual(result.returncode, 
                             0, 
                             msg=f"STDOUT: {result.stdout.decode()}\nSTDERR: {result.stderr.decode()}")
        
        def test_astar_with_continue_on_solved(self):
            '''
            Continue on solved is a new argument to astar'''
            result = subprocess.run(f'{FAST_DOWNWARD} {DOMAIN} {TASK} --search "astar(lmcut(), continue_on_solved=true)"', 
                           shell=True, 
                           capture_output=True)
            self.assertEqual(result.returncode, 
                             0, 
                             msg=f"STDOUT: {result.stdout.decode()}\nSTDERR: {result.stderr.decode()}")
        


def teardown_module(module):
    cleanup()
