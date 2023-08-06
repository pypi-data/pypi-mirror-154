from argh import arg, expects_obj
import os
import sys
import time
import subprocess
import psutil
import shutil
import git
import socket
import pathlib
import season
import dizest
import multiprocessing as mp
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
import platform

def portchecker(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        port = int(port)
        s.connect(("127.0.0.1", port))
        return True
    except:
        pass
    return False

PATH_WIZ = season.path.lib
PATH_DIZEST = os.path.dirname(os.path.dirname(__file__))

PATH_WORKINGDIR = os.getcwd()
PATH_WEBSRC = os.path.join(PATH_WORKINGDIR, "websrc")
PATH_DIZEST_CONFIG = os.path.join(PATH_WORKINGDIR, "dizest.json")

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def install():
    fs = dizest.util.os.storage(PATH_WORKINGDIR)
    fs.remove("websrc")
    
    print("install wiz...")
    PATH_PUBLIC_SRC = os.path.join(PATH_WIZ, 'data')
    shutil.copytree(PATH_PUBLIC_SRC, PATH_WEBSRC)
    git.Repo.clone_from("https://github.com/season-framework/wiz-ide", os.path.join(PATH_WEBSRC, 'plugin'))
    fs.write(os.path.join(PATH_WEBSRC, 'config', 'installed.py'), "started = '" + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + "'")
    
    print("install dizest...")
    shutil.copytree(os.path.join(PATH_DIZEST, 'res', 'websrc'), os.path.join(PATH_WEBSRC, 'branch', 'main'))

    if fs.exists(PATH_DIZEST_CONFIG) == False:
        fs.write.json(PATH_DIZEST_CONFIG, {"db": {"type": "sqlite"}, "version": dizest.version})
    print("installed!")

def update():
    install()

@arg('-f', default=None, help='workflow.dzw')
def flow(f=None):
    if f is None:
        print("dizest run -f workflow.dzw")
        return
    
    fs = dizest.util.os.storage(PATH_WORKINGDIR)
    package = fs.read.json(f)
    workflow = dizest.Workflow(package, cwd=PATH_WORKINGDIR, user="daemon", auth="admin", develop=False, logger=print, command=True)
    flows = workflow.flows()
    for flow in flows:
        print(flow)

@arg('--host', default=None, help='0.0.0.0')
@arg('--port', default=0, help='3000')
@arg('-f', default=None, help='workflow.dzw')
def run(f=None, host="0.0.0.0", port=3000):
    if f is not None:
        # fs = dizest.util.os.storage(PATH_WORKINGDIR)
        # package = fs.read.json(f)
        # workflow = dizest.Workflow(package, cwd=PATH_WORKINGDIR, user="daemon", auth="admin", develop=False, logger=print, command=True)
        # workflow.run("zrjzackezlufnrr2-1651384139666")
        return

    fs = dizest.util.os.storage(PATH_WEBSRC)
    if fs.exists() is False:
        install()
    
    config = fs.read.json(PATH_DIZEST_CONFIG, dict())
    if 'version' not in config:
        config['version'] = dizest.version

    # port finder
    startport = port
    if 'port' in config and port <= 0:
        startport = int(config['port'])
    if startport <= 0:
        startport = 3000
    while portchecker(startport):
        startport = startport + 1
    config['port'] = startport
    
    # host finder
    if 'host' in config and host is None:
        host = config['host']
    if host is None:
        host = '0.0.0.0'
    config['host'] = host
    config['path'] = PATH_WORKINGDIR

    # save dizest config
    fs.write.json(PATH_DIZEST_CONFIG, config)

    # build config
    PATH_CONFIG_BASE = os.path.join(PATH_DIZEST, 'res', 'config', 'server.py')
    PATH_CONFIG = os.path.join(PATH_WEBSRC, 'config', 'server.py')

    data = fs.read.text(PATH_CONFIG_BASE)
    data = data.replace("__PORT__", str(startport))
    data = data.replace("__HOST__", str(host))
    fs.write.text(PATH_CONFIG, data)
    
    # copy config
    fs.copy(os.path.join(PATH_DIZEST, 'res', 'config', 'wiz.py'), os.path.join("config", "wiz.py"))

    # run server
    publicpath = os.path.join(PATH_WEBSRC, 'public')
    apppath = os.path.join(publicpath, 'app.py')

    if os.path.isfile(apppath) == False:
        print("Invalid Project path: dizest structure not found in this folder.")
        return

    def run_ctrl():
        env = os.environ.copy()
        env['WERKZEUG_RUN_MAIN'] = 'true'
        cmd = str(sys.executable) + " " +  str(apppath)
        subprocess.call(cmd, env=env, shell=True)

    ostype = platform.system().lower()
    if ostype == 'linux':
        while True:
            try:
                proc = mp.Process(target=run_ctrl)
                proc.start()
                proc.join()
            except KeyboardInterrupt:
                for child in psutil.Process(proc.pid).children(recursive=True):
                    child.kill()
                return
            except:
                pass
    else:
        run_ctrl()