import os

import unittest
import unittest.mock
import warnings

import re
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
        )
        while True:
            if os.path.exists(f'/proc/{proc.pid}'):
                return proc.pid
            print('It does not exists!')

    def kill_process(self, pid: int) -> None:
        with sub.Popen(['kill', str(pid)]) as _:
            pass




class TestGetPids(TestRelaunch):

    def setUp(self):
        super().setUp()
        self.false_pid = self.start_process([*self.dummy, '2'])

    def tearDown(self):
        super().tearDown()
        self.kill_process(self.false_pid)

    def test_get_pid(self):
        pid = relaunch.get_pids(' '.join(self.dummy))
        self.assertEqual(pid, [self.pid])


class TestSelectProcess(TestRelaunch):
    def setUp(self):
        self.pids = [self.start_process(self.dummy) for _ in range(2)]

    def tearDown(self):
        for pid in self.pids:
            self.kill_process(pid)

    @unittest.mock.patch('builtins.input', return_value='a')
    def test_with_invalid_input(self, mock_input):
        with unittest.mock.patch('builtins.print') as mock_print:
            relaunch.select_process(self.pids, _test=True)
            mock_print.assert_called_with("Incorrect ID! Try again.")

    def test_with_valid_input(self):
        with unittest.mock.patch('builtins.input') as mock_input:
            mock_input.return_value = '0'
            pid = relaunch.select_process(self.pids, _test=True)
            self.assertTrue(pid in self.pids)
            self.tearDown()
            self.setUp()
            mock_input.return_value = '1'
            pid = relaunch.select_process(self.pids, _test=True)


class TestGetUptimes(TestRelaunch):
    def setUp(self):
        self.pids = [self.start_process(self.dummy) for _ in range(2)]

    def tearDown(self):
        for pid in self.pids:
            self.kill_process(pid)

    def test_get_uptimes(self):
        uptimes = relaunch.get_uptimes(self.pids)
        pattern = re.compile(r"\d+:\d{2}:\d{1,2}")

        self.assertTrue(uptimes, all(map(pattern.match, uptimes)))



class TestKillProcess(TestRelaunch):

    def test_killing_process(self):
        self.assertEqual(relaunch.kill_process(self.pid), None)



class TestKillNonexistingProcess(TestRelaunch):

    def test_killing_nonexisting_process(self):
        self.tearDown()
        self.assertIsInstance(relaunch.kill_process(self.pid), str)



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


class TestRelaunchProcess(TestRelaunch):

    def tearDown(self):
        super().tearDown()
        self.kill_process(self.new_pid)

    def test_success(self):
        self.new_pid = relaunch.relaunch_process(self.pid, self.dummy)
        self.assertIsInstance(self.new_pid, int)

    def test_fail(self):
        super().tearDown()
        self.new_pid = relaunch.relaunch_process(self.pid, self.dummy)
        self.assertIsInstance(self.new_pid, str)
