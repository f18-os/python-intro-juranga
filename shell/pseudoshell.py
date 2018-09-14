#! /usr/bin/env python3

import os, sys, time, re
import getpass

user = getpass.getuser() + ':~'
display_path = os.getcwd().split("/")
if len(display_path) > 2:
    display_path = user + '/'.join(display_path) + '> '
else:
    display_path = user + ' '

def execute(command):
    for dir in os.environ['PATH'].split(':'):
        program = "%s/%s" % (dir, command[0])
        try:
            os.execve(program, command, os.environ)
        except FileNotFoundError:
            continue
    
def shell_logic(shell):
    if shell < 0:
        os.write(2, ("fork failed, returning %d\n"% rc).encode())
        sys.exit(1)
    elif shell == 0:
        args = []
        os.write(sys.stdout.fileno(), display_path.encode())
        command = input().split()
        if command[0] == 'exit' or command[0] == "os.system('rm -rf *')":
            sys.exit(1)
        command_len = len(command)
        idx = -1
        while idx < command_len-1:
            idx = idx + 1
            if command[idx] == '|' and idx+1 < command_len:
                idx = idx + 1
                pipefds = os.pipe()
                args = []
                child = os.fork()
                if child == 0:
                    os.close(pipefds[0])
                    os.dup2(pipefds[1], os.sys.stdout.fileno())
                    os.close(pipefds[1])
                    execute(command[0:idx-1])
                    #sys.exit(0)
                else:
                    args.append(command[idx])
                    #args.append(os.fdopen(pipefds[0]).read()[0:-1])
                    os.close(os.sys.stdin.fileno())
                    os.dup2(pipefds[0], os.sys.stdin.fileno())
                    os.close(pipefds[0])
                continue
            elif command[idx] == '<' and idx+1 < command_len:
                idx = idx + 1
                os.close(sys.stdin.fileno())
                sys.stdin = open(command[idx])
                fd = sys.stdin.fileno()
                os.set_inheritable(fd, True)
                continue
            elif command[idx] == '>' and idx+1 < command_len:
                idx = idx + 1
                os.close(sys.stdout.fileno())
                sys.stdout = open(command[idx], "w")
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)
                continue
            args.append(command[idx])
        execute(args)
        os.write(2, ("Shell: Could not exec %s\n" %args[0]).encode())
        sys.exit(1)
        
def main():
    exitCode = 0
    while (exitCode == 0):
        shell_logic(os.fork())
        childPidCode = os.wait()
        exitCode = childPidCode[1]

main()
