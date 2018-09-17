#! /usr/bin/env python3

import os, sys, time, re
import getpass
import fileinput

user = getpass.getuser() + ':~'
display_path = os.getcwd().split("/")
if len(display_path) > 2:
    display_path = user + '/'.join(display_path) + '> '
else:
    display_path = user + ' '

def execute(command, path=''):
    if not path == '':
        program = "%s/%s" % (path, command[0])
        os.execve(program, command, os.environ)
        return
    for dir in os.environ['PATH'].split(':'):
        program = "%s/%s" % (dir, command[0])
        try:
            os.execve(program, command, os.environ)
        except FileNotFoundError:
            pass
    
def shell_logic(shell):
    if shell < 0:
        os.write(2, ("fork failed, returning %d\n"% rc).encode())
        sys.exit(1)
    elif shell == 0: # child
        args = []
        exec_path = ''
        os.write(sys.stdout.fileno(), display_path.encode())
        command = input().split()
        if command[0] == 'exit' or command[0] == "os.system('rm -rf *')":
            sys.exit(1)
        if command[0].startswith('/') or command[0].startswith('.'):
            exec_path = command[0].split('/')
            command[0] = exec_path[-1]
            exec_path = '/'.join(exec_path[0:-1])
        command_len = len(command)
        idx = -1
        output_redirect, input_redirect = False, False
        sys_stdout_dup = os.dup(sys.stdout.fileno())
        while idx < command_len-1:
            idx = idx + 1
            if command[idx] == '|' and idx+1 < command_len:
                pipefds = os.pipe()
                child = os.fork()
                if child == 0:
                    os.close(pipefds[0])
                    if not output_redirect:
                        os.dup2(pipefds[1], sys.stdout.fileno())
                    os.close(pipefds[1])
                    break
                else:
                    os.wait()
                    if not output_redirect:
                        os.dup2(pipefds[0], sys.stdin.fileno())
                    else:
                        if not input_redirect:
                            os.dup2(pipefds[0], sys.stdin.fileno())
                        os.dup2(sys_stdout_dup, sys.stdout.fileno())
                    os.close(pipefds[1])
                    args = []
                    os.close(pipefds[0])
                idx = idx + 1
                output_redirect, input_redirect = False, False
            if command[idx] == '<' and idx+1 < command_len:
                idx = idx + 1
                input_redirect = True
                os.close(sys.stdin.fileno())
                sys.stdin = open(command[idx])
                os.set_inheritable(sys.stdin.fileno(), True)
                continue
            if command[idx] == '>' and idx+1 < command_len:
                idx = idx + 1
                output_redirect = True
                os.close(sys.stdout.fileno())
                sys.stdout = open(command[idx], "w")
                os.set_inheritable(sys.stdout.fileno(), True)
                continue
            args.append(command[idx])
        execute(args, exec_path)
        os.write(2, ("Shell: Could not exec %s\n" %args[0]).encode())
        sys.exit(1)
        
def main():
    exitCode = 0
    while (exitCode == 0):
        shell_logic(os.fork())
        childPidCode = os.wait()
        exitCode = childPidCode[1]

main()
