# align
def align_up(alignment, x):
    """Rounds x up to nearest multiple of the alignment."""
    a = alignment
    return ((x + a - 1) // a) * a

def align_down(alignment, x):
    """Rounds x down to nearest multiple of the alignment."""
    a = alignment
    return (x // a) * a

def align(alignment, x):
    """Rounds x up to nearest multiple of the alignment."""
    return align_up(alignment, x)

# network utils
def ip (host):
    """Resolve host and return IP as four byte string"""
    import socket, struct
    return struct.unpack('I', socket.inet_aton(socket.gethostbyname(host)))[0]

def get_interfaces():
    """Gets all (interface, IPv4) of the local system."""
    import subprocess, re
    d = subprocess.check_output('ip -4 -o addr', shell=True)
    ifs = re.findall(r'^\S+:\s+(\S+)\s+inet\s+([^\s/]+)', d, re.MULTILINE)
    return [i for i in ifs if i[0] != 'lo']

# Stuff
def size(n, abbriv = 'B', si = False):
    """Convert number to human readable form"""
    base = 1000.0 if si else 1024.0
    if n < base:
        return '%d%s' % (n, abbriv)

    for suffix in ['K', 'M', 'G', 'T']:
        n /= base
        if n <= base:
            num = '%.02f' % n
            # while num[-1] == '0':
            #     num = num[:-1]
            # if num[-1] == '.':
            #     num = num[:-1]
            return '%s%s%s' % (num, suffix, abbriv)

    return '%.02fP%s' % (n, abbriv)

def read(path):
    """Open file, return content."""
    import os.path
    path = os.path.expanduser(os.path.expandvars(path))
    with open(path) as fd:
        return fd.read()

def write(path, data, create_dir = False):
    """Create new file or truncate existing to zero length and write data."""
    import os.path
    path = os.path.expanduser(os.path.expandvars(path))
    if create_dir:
        import os
        path = os.path.realpath(path)
        ds = path.split('/')
        f = ds.pop()
        p = '/'
        while True:
            try:
                d = ds.pop(0)
            except:
                break
            p = os.path.join(p, d)
            if not os.path.exists(p):
                os.mkdir(p)
    with open(path, 'w') as f:
        f.write(data)

def bash(cmd, timeout = None, return_stderr = False):
    """Execute cmd and return stdout and stderr in a tuple """
    import subprocess, time
    p = subprocess.Popen(['/bin/bash', '-c', cmd],
                         stdin  = subprocess.PIPE,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE)
    if timeout is None:
        o, e = p.communicate()
    else:
        t = time.time()
        while time.time() - t < timeout:
            time.sleep(0.01)
            if p.poll() is not None:
                break
        if p.returncode is None:
            p.kill()
        o, e = p.communicate()
    if return_stderr:
        return o, e
    return o

def isint(n):
    return isinstance(n, (int, long))
