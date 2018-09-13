#! /usr/bin/env python3

import os, sys, time, re

display_path = os.getcwd().split("/")
if len(display_path) > 2:
    display_path = '/'.join(display_path) + '> '
else:
    display_path = 'student:> '

def shell_logic(shell):
    if shell < 0:
        os.write(2, ("fork failed, returning %d\n"% rc).encode())
        sys.exit(1)

    elif shell == 0:
        os.write(1, display_path.encode())
        command = input().split()
        args = []
        if command[0] == 'exit':
            sys.exit(1)
        for idx in range(0, len(command)):
            if command[idx] == '<':
                idx = idx + 1
                os.close(0)
                sys.stdin = open(command[idx])
                fd = sys.stdin.fileno()
                os.set_inheritable(fd, True)
                #os.write(2, ("Child: opened fd=%d for input\n" %fd).encode())
                continue
            if command[idx] == '>':
                idx = idx + 1
                os.close(1)
                sys.stdout = open(command[idx], "w")
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)
                #os.write(2, ("Child: opened fd=%d for writing\n" %fd).encode())
                break
            args.append(command[idx])
    
        for dir in os.environ['PATH'].split(':'):
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError:
                continue

        os.write(2, ("Shell: Could not exec %s\n" %args[0]).encode())
        sys.exit(1)
        
def main():
    exitCode = 0
    while (exitCode == 0):
        shell_logic(os.fork())
        childPidCode = os.wait()
        exitCode = childPidCode[1]

main()
