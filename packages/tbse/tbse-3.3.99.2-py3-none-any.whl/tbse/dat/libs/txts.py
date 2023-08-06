import sys,os
def get(s):
    try:
        return {
'version':'3.3.2',
'path':os.sep.join(sys.argv[0].split(os.sep)[:-2]),
'hlp':open(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/README.md').read(),
'install files':'tool.py libs/txts.py libs/dol.py libs/clearqq.py',
'upd':'''\
Update info:
    ---- 3.3.2 ----
1.Fixed known issues
2.Author forgot what he updated
3.Removed Herobrine
Last releases:
    ---- 3.3.1 25a ----
1.Comments and strings (ps: echo 'this is a string';here are some comment texts)
2.Escape characters (ps: `echo '#q#a#.##'` output `'& #`
    ---- 3.3 ----
1.Runtime command (Type shell command like 'tb -c cmd1:arg1 cmd2:arg2 ...')
2.Runtime file running (Type shell command like 'tb file1.tb file2.tb ...')
3.Toggle the shell prompt (Type 'ps' to toggle then type 'insh' to try)
4.Wait a few time (Type 'wait')
5.Extra functions (Testing)
6.Setup package no longer relies package 'tb'
7.Removed Herobrine
'''
}[s]
    except KeyError:
        raise ValueError('txts.py: failed to get "%s"'%s)
if __name__=='__main__':
    print(sys.argv[0])
    for x in ('version','path','hlp','install files','upd','this is a falied key'):
        print('\033[33mtxts.get\033[92;100m(\033[0;95m"%s"\033[92;100m)\033[0m\n%s'%(x,get(x)))
