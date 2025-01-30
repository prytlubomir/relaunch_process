import unittest
import warnings
import subprocess as sub

import relaunch


class TestRelaunch(unittest.TestCase):

    dummy = ['python3.11', 'server.py']

    def setUp(self):
        proc = sub.Popen(
            self.dummy,
            close_fds=True,
            stdout=sub.PIPE,
            stderr=sub.PIPE,
            shell=True
        )
        self.pid = proc.pid
        warnings.simplefilter('ignore', category=ResourceWarning)

    def tearDown(self):
        with sub.Popen(['kill', str(self.pid)]) as proc:
            pass




class TestGetPid(TestRelaunch):

    def test_get_pid(self):
        pid = relaunch.get_pid(' '.join(self.dummy))
        self.assertEqual(pid, self.pid)



class TestKillProcess(TestRelaunch):

    def test_killing_process(self):
        self.assertEqual(relaunch.kill_process(self.pid), 0)



class TestKillNonexistingProcess(TestRelaunch):

    def test_killing_nonexisting_process(self):
        self.tearDown()
        self.assertEqual(relaunch.kill_process(self.pid), 1)



class TestLaunch(TestRelaunch):

    def setUp(self):
        warnings.simplefilter('ignore', category=ResourceWarning)
    def test_lauch(self):
        self.pid = relaunch.launch_process(self.dummy)
        self.assertIsInstance(self.pid, int)

    def validate_pid(self):
        cmd = ['ps', '-p', str(self.pid)]
        with sub.Popen(cmd, stdout=sub.PIPE) as proc:
            result = proc.communicate()[0]
        result = [item.strip() for item in result.decode().split('\n')]
        self.assertTrue(len(result) > 1)
        self.assertTrue(result[1])
