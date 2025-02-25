'''
Relaunch process by its command.
v1.3.0
'''

from typing import Iterable
import subprocess as sub
import sys


def get_pids(process_name: str) -> list:
    '''
    get_pid(process_name: str) -> list:

    Get the PID of a process using "pgrep" command.
    '''
    # pgrep - displays processes selected by regex
    # -f - use full process name to match
    # -x - search for the exact name
    cmd = ['pgrep', '-f', '-x', f'{process_name}']

    with sub.Popen(cmd, stdout=sub.PIPE) as proc:
        result = proc.communicate()[0]

    result = result.decode().strip()

    if not result:
        raise ValueError(f'No process with name "{process_name}".')

    return list(map(int, result.split('\n')))


def kill_process(pid: int | str) -> None | str:
    '''
    kill_process(pid: int | str) -> bool:

    Stops a process with a specified PID.

    Return:
        *  None - success (no error)
        *  error message: str - fail
    '''
    cmd = ['kill', str(pid)]

    with sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE) as proc:
        err = proc.communicate()[1]

    if err:
        return err.decode()


def launch_process(command: str | Iterable) -> int:
    '''Run a command in an independent process.'''
    cmd = command
    if isinstance(cmd, str):
        cmd = cmd.split()

    proc = sub.Popen(cmd, close_fds = True)
    pid = proc.pid

    return pid


def relaunch_process(pid: int, command: list | str) -> int | str: # str = error#
    '''
    relaunch(pid: int, command: list | str) -> int | str:

    Kill process by "pid" and launch "command".

    Return:
        PID: int - process ID of the launched process (success)
        error message: str - killing the process wasn't successfull
    '''
    status = kill_process(pid)
    if status:
        return status
    new_pid = launch_process(command)

    return new_pid


def _draw_table(headers: Iterable, data: Iterable[Iterable], caption: str='', sep: str='-') -> None:
    '''
    Draws a table in the terminal.
    Args:
     	headers - a list of captions for each respectful column
     	data - a list of rows
     	caption - the title above the table
     	sep - a pattern that separates the table header
    '''
    VERTICAL_GAP = 2

    print(caption)
    print(sep*len(caption))

    sizes: Iterable[int] = [len(max(size, key=lambda x: len(str(x)))) for size in data]

    sections = []

    for index, header in enumerate(headers):
        string = str(header)
        gap = sizes[index] - len(string) + VERTICAL_GAP
        sections.append(string+' '*gap)

    print(''.join(sections))
    print(sep*len(caption))

    for row_ in data:
        row = []
        for index, coll in enumerate(row_):
            string = str(coll)
            gap = sizes[index] - len(string) + VERTICAL_GAP
            row.append(string+' '*gap)
        print(''.join(row))


def get_uptimes(pids: Iterable) -> list:
    '''Get uptimes of a bunch of processes by their PIDs in respective order.'''
    uptimes = []
    for pid in pids:
        with sub.Popen(['ps', '-p', str(pid), '-o', 'time'], stdout=sub.PIPE) as proc:

            uptime = proc.communicate()[0]
            uptime = uptime.decode()

            uptime = uptime.split('\n')[1]
            uptime = uptime.strip()

            uptimes.append(uptime)

    return uptimes


def select_process(pids: Iterable, _test=False) -> int:
    '''
    An interface that allows the user to select one process by its uptime
    if multiple are available.
    '''
    caption  = "There's multiple processes with the same name"
    headers = ["ID", "Process Uptime"]
    sep    = '-'

    # generate list with [id, uptime]
    uptimes = get_uptimes(pids)
    table = [[str(_id), uptime] for _id, uptime in enumerate(uptimes)]

    _draw_table(headers, table, caption, sep=sep)

    while True:
        choice = input("Enter ID: ")
        if choice.isnumeric():
            if len(pids)-1 >= int(choice):
                return pids[int(choice)]
        print("Incorrect ID! Try again.")
        # simplify testing
        if _test:
            break


def main():
    '''Relaunch process'''

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = input('Enter a command to relaunch: ')

    pids = get_pids(command)
    pid = pids[0]
    if len(pids) > 1:
        pid = select_process(pids)

    result = relaunch_process(pid, command)

    print(result)


if __name__ == "__main__":
    main()
