'''
Relaunch python process by its command.
v1.0.2
'''

from typing import Iterable
import subprocess as sub


def get_pid(process_name: str) -> int:
    '''
    get_pid(process_name: str) -> int:

    Get the PID of a process using "pgrep" command.
    '''
    # pgrep - displays processes selected by regex
    # -f - use full process name to match
    cmd = ['pgrep', '-f', process_name]

    with sub.Popen(cmd, stdout=sub.PIPE) as proc:
        result = proc.communicate()[0]

    result = result.decode().strip()

    if not result:
        raise ValueError(f'Process name {process_name} not found.')

    return int(result)


def kill_process(pid: int | str) -> bool:
    '''
    kill_process(pid: int | str) -> bool:

    Stops a process with a specified PID.

    Return:
        *  0 | False - success (no error)
        *  1 | True  - fail (wrong PID)
    '''
    cmd = ['kill', str(pid)]

    with sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE) as proc:
        err = proc.communicate()[1]

    if err:
        return 1
    return 0


def launch_process(command: str | Iterable) -> int:
    '''Run a command in an independent process.'''
    cmd = command
    if isinstance(cmd, str):
        cmd = cmd.split()

    proc = sub.Popen(cmd, close_fds = True)
    pid = proc.pid

    return pid


def main():
    '''Relaunch process'''
    command = 'python3.11 server.py'
    pid = get_pid(command)
    kill_process(pid)
    new_pid = launch_process(command)

    print(new_pid)


if __name__ == "__main__":
    main()
