import unittest
import warnings
import subprocess as sub

import relaunch


class TestRelaunch(unittest.TestCase):

    dummy = ['python3.11', 'server.py']

    def setUp(self):
        self.pid = self.start_process(self.dummy)
        warnings.simplefilter('ignore', category=ResourceWarning)

    def tearDown(self):
        self.kill_process(self.pid)
    
    def start_process(self, cmd: list | str) -> int:
        proc = sub.Popen(
            cmd,
            close_fds=True,
            stdout=sub.PIPE,
            stderr=sub.PIPE,
            shell=True
        )
        return proc.pid
    
    def kill_process(self, pid: int) -> None:
        with sub.Popen(['kill', str(pid)]) as _:
            pass




class TestGetPid(TestRelaunch):

    def setUp(self):
        super().setUp()
        self.false_pid = self.start_process([*self.dummy, '2'])

    def tearDown(self):
        super().tearDown()
        self.kill_process(self.false_pid)

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
