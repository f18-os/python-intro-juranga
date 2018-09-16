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
    elif shell == 0: # child
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
                pipefds = os.pipe()
                #args = []
                child = os.fork()
                if child == 0:
                    os.close(pipefds[0])
                    os.dup2(pipefds[1], os.sys.stdout.fileno())
                    os.close(pipefds[1])
                    break
                else:
                    os.wait()
                    args = []
                    os.close(pipefds[1])
                    os.dup2(pipefds[0], os.sys.stdin.fileno())
                    os.close(pipefds[0])
                idx = idx + 1
            if command[idx] == '<' and idx+1 < command_len:
                idx = idx + 1
                os.close(sys.stdin.fileno())
                sys.stdin = open(command[idx])
                fd = sys.stdin.fileno()
                os.set_inheritable(fd, True)
                continue
            if command[idx] == '>' and idx+1 < command_len:
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
