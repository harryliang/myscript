#encoding=utf8

"""
@author: harry
@created: 2015-10-13
@description: find from which version that code is added.
"""

import envoy
import argparse

def get_content(commit):
    cmd = 'git checkout {0} {1}'.format(commit, target_f)
    envoy.run(cmd)
    content = file(target_f).read()
    return content

def find_code(commit_list, code):
    for commit in commit_list:
        if code in get_content(commit):
            print 'code first found in commit: {}'.format(commit)
            return commit
    else:
        print 'code not found in any commit!'
        return None

def recovery():
    cmd = 'git checkout HEAD {}'.format(target_f)
    envoy.run(cmd)

def show_diff(commit):
    cmd = 'git difftool {} {}'.format(commit, target_f)
    envoy.run(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument('-c', '--code', required=True)
    args = parser.parse_args()

    target_f = args.file
    code = args.code

    cmd = 'git log {0} | grep commit'.format(target_f)
    result = envoy.run(cmd)
    output = result.std_out.split('\n')
    commit_list = []
    for line in output:
        if 'commit ' in line:
            commit_list.append(line[7:])
    commit_list.reverse()

    commit = find_code(commit_list, code)
    recovery()
    if commit:
        show_diff(commit)
