import sys,psutil,subprocess,os

def is_root(pid):
    try:
        return psutil.Process(pid).username()=="root"
    except:
        return False

def run_e(cmd):
    try:
        return subprocess.run(["pkexec"]+cmd,check=True)
    except:
        return subprocess.run(["sudo","-A"]+cmd,check=True)

def kill(pid):
    cmd=["kill","-15",str(pid)]
    if is_root(pid):
        return run_e(cmd)
    return subprocess.run(cmd)

if __name__=="__main__":
    pid=int(sys.argv[1])
    kill(pid)
