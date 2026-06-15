
import sys,psutil,subprocess

def run_e(cmd):
    try:
        return subprocess.run(["pkexec"]+cmd,check=True)
    except:
        return subprocess.run(["sudo","-A"]+cmd,check=True)

def kill_tree(pid,force=False):
    try:
        p=psutil.Process(pid)
        children=p.children(recursive=True)

        for c in children:
            kill_single(c.pid,force)

        kill_single(pid,force)
    except:
        pass

def kill_single(pid,force):
    sig="-9" if force else "-15"
    cmd=["kill",sig,str(pid)]
    run_e(cmd)

if __name__=="__main__":
    pid=int(sys.argv[1])
    kill_tree(pid,force=False)
