'''
Relaunch python process by its command.
v1.1.1
'''

from typing import Iterable
import subprocess as sub


def get_pids(process_name: str) -> list:
    '''
    get_pid(process_name: str) -> int:

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


def _draw_table(topics: Iterable, data: Iterable[Iterable], title: str='', sep: str='-') -> None:

    VERTICAL_GAP = 2

    print(title)
    print(sep*len(title))

    sizes: Iterable[int] = [len(max(size, key=lambda x: len(str(x)))) for size in data]

    sections = []

    for index, topic in enumerate(topics):
        string = topic
        gap = sizes[index] - len(string) + VERTICAL_GAP
        sections.append(string+str(gap))

    print(''.join(sections))
    print(sep*len(title))

    for row_ in data:
        row = []
        for index, coll in enumerate(row_):
            string = coll
            gap = sizes[index] - len(string) + VERTICAL_GAP
            row.append(string+' '*gap)
        print(''.join(row))


def get_uptimes(pids: list) -> list:
    uptimes = []
    for pid in pids:
        with sub.Popen(['ps', '-p', str(pid), '-o', 'time'], stdout=sub.PIPE) as proc:

            uptime = proc.communicate()[0]
            uptime = uptime.decode()

            uptime = uptime.split('\n')[1]
            uptime = uptime.strip()

            uptimes.append(uptime)

    return uptimes


def select_process(pids: list, _test=False) -> int:

    title  = "There's multiple processes with the same name"
    topics = ["ID", "Process Uptime"]
    sep    = '-'

    # generate list with [id, uptime]
    uptimes = get_uptimes(pids)
    table = [[str(_id), uptime] for _id, uptime in enumerate(uptimes)]

    _draw_table(topics, table, title, sep=sep)

    while True:
        pid = input("Enter ID: ")
        if pid.isnumeric():
            if len(pids)-1 <= int(pid):
                return pids[int(pid)]
        print("Incorrect ID! Try again.")
        # simplify testing
        if _test:
            break


def main():
    '''Relaunch process'''
    command = input('Enter a command to relaunch: ')
    pids = get_pids(command)

    pid = pids[0]

    if len(pids) > 1:
        pid = select_process(pids)

    kill_process(pid)
    new_pid = launch_process(command)

    print(new_pid)


if __name__ == "__main__":
    main()
