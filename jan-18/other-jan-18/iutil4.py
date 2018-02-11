import pickle as pkl
import zipfile as zf
import gzip as zfg
import os
import time
import math
import time
import shutil
import subprocess
import threading
class utils:
    class error():
        def no_file_err(name):
            if name[0] != '/':
                name = name+'./'
            name_split = name.split('/')
            pref = ''.join([i+'/' for i in name_split[:-1]])[:-1]
            f = name_split[-1]
            if not os.path.isfile(name) and os.path.isdir(name) :
                    utils.error.error('file not found')
        def file_name_err(name):
            if name == '':
                utils.error.error('file nothing')
            if not isinstance(name,str):
                utils.error.error('file not str')
        def file_zip_name_err(name):
            name = name.split('/')
            fi = name[-1]
            fe = fi.split('.')[-1]
            if not fe in ['zip','gz','pkz']:
                utils.error.error('unkown zip type')
        def error(err,*args):
            if len(args) > 0:
                erd = args[0]
            else:
                erd = ''
            class file_Nothing(Exception):
                pass
            class file_Not_Found(Exception):
                pass
            class file_Not_Str(Exception):
                pass
            class unkown_Zip_Type(Exception):
                pass
            if 'file nothing' == err:
                r = file_Nothing('a file name cannot be an empty string')
            if 'file not found':
                r = file_Not_Found('file was not found in directory')
            if 'file not found' and False:
                r = file_Not_Found('directory containing file was not found')
            if 'file not str' == err:
                r = file_Not_Str('file name must be a string')
            if 'unkown zip type' == err:
                r = unkown_Zip_Type('file comression can only be done in .zip or .gz files')
            if isinstance(r,str):
                raise(Exception(r))
            else:
                raise(r)
    class pickle:
        def write(name,dat):
            utils.error.file_name_err(name)
            with open(name,'wb') as f:
                pkl.dump(dat,f)
        def read(name):
            utils.error.file_name_err(name)
            utils.error.no_file_err(name)
            with open(name,'rb') as f:
                return pkl.load(f)
    class zipf:
        def write(zipname,filename):
            if not isinstance(filename,list):
                utils.error.file_name_err(filename)
                utils.error.no_file_err(filename)
            utils.error.file_name_err(zipname)
            fe = zipname.split('.')[-1]
            if fe == 'zip':
                if os.path.exists(filename) and not os.path.isfile(filename):
                    shutil.make_archive(zipname[:-4], 'zip', filename)
                else:
                    with zf.ZipFile(zipname,mode='w') as zipobj:
                        if isinstance(filename,list):
                            for nw in filename:
                                zipobj.write(nw)
                        else:
                            zipobj.write(filename)
            elif fe == 'gz' or fe == 'pkz':
                with zfg.open(zipname,mode='wb') as zipobj:
                    zipobj.write(open(filename,'rb').read())
        def read(zipname,*args,r=False):
            utils.error.no_file_err(zipname)
            utils.error.file_zip_name_err(zipname)
            fe = zipname.split('.')[-1]
            if fe == 'zip':
                with zf.ZipFile(zipname) as zipobj:
                    zipobj.extractall(path=args[0])
            elif fe == 'gz' or fe == 'pkz':
                filename = args[0]
                with zfg.open(zipname) as zipobj:
                    open(filename,'wb').write(zipobj.read())
        def output(zipfile,filename):
            d = utils.zipf.read(zipfile,filename)
            open(filename,'wb').write(d)
    class slice:
        def split(filename,*args,size='500k',zipf=False,thread=True):
            if isinstance(size,int):
                size = int(size)
            if isinstance(size,str):
                if size[-1] in ['b','B']:
                    size = size[:-1]
                size = int(size[:-1])*{'k':1000,'K':1000,'m':1000**2,'M':1000**2,'g':1000**3,'G':1000**3}[size[-1]]
            if len(args) == 0:
                outname = filename.split('.')[0]
            else:
                outname = args[0]
            if outname in os.listdir():
                shutil.rmtree(outname)
            utils.error.no_file_err(filename)
            f = open(filename,'rb').read()
            l = len(f)
            os.makedirs(outname)
            pl = 0
            for i in range(0,(l//size+1)*size,size):
                pl += 1
                hv = outname+'/'+str(pl)
                open(hv,'wb').write(f[i:i+size])
            if zipf != False:
                ts = []
                if thread:
                    for i in os.listdir(outname):
                        t = threading.Thread(target=utils.zipf.write,args=(outname+'/'+i+'.'+zipf,outname+'/'+i))
                        ts.append(t)
                        t.start()
                    for i in range(len(ts)):
                        ts[i].join()
                    for i in os.listdir(outname):
                        if i.isnumeric():
                            os.remove(outname+'/'+i)
                else:
                    for i in os.listdir(outname):
                        utils.zipf.write(outname+'/'+i+'.'+zipf,outname+'/'+i)
                        os.remove(outname+'/'+i)
        def join(foldername,*args,zipf=False):
            if len(args) == 0:
                outname = './'+foldername+'_'
            else:
                outname = args[0]
            names = []
            for i in os.listdir(foldername):
                if zipf != False:
                    names.append(int(i[:-len(zipf)-1]))
            names.sort()
            if outname in os.listdir():
                os.remove(outname)
            f = open(outname,'ab')
            for i in names:
                cfile = foldername+'/'+str(i)
                if zipf != False:
                    utils.zipf.read(cfile+'.'+zipf,cfile)
                    fo = open(cfile,'rb').read()
                    os.remove(cfile)
                else:
                    fo = open(cfile,'rb').read()
                f.write(fo)
    class pkfold:
        def write(foldername,data,zt='zip',size='1m',thread=True):
            utils.pickle.write('main.pkl',data)
            utils.slice.split('main.pkl',foldername,zipf=zt,size=size,thread=thread)
            utils.zipf.write(foldername+'.zip',foldername)
        def read(foldername,zt='zip'):
            utils.zipf.read(foldername,foldername[:-len(zt)-2])
            utils.slice.join(foldername[:-4],'main.pkl',zipf=zt)
            out = utils.pickle.read('main.pkl')
            os.remove('main.pkl')
            return out
    class shell:
        def __new__(self,*args):
            if len(args) == 1:
                proc = subprocess.Popen(
                    args[0],
                    shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                    )
                red = proc.stdout.read()
                open('shell_output.txt','wb').write(red)
                out = open('shell_output.txt').read()
                os.remove('shell_output.txt')
                return out
        class ls:
            def __new__(self,*args):
                if len(args) < 2:
                    return os.listdir(args[0] if len(args) > 0 else './')
                else:
                    return [os.listdir(i) for i in args]
            def ls_(*args):
                x = utils.shell.ls(args)
                if len(x) > 0:
                    if isinstance(x[0],list):
                        out = []
                        for i in x:
                            out += i
                        return out
                    return x
                return []
        def copy(fr,to):
            shutil.copy2(fr,to)
        def rm(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)
            return
    class ion:
        def pair(x,chs,depth=0):
            hold = {}
            dep = 0
            pl = 0
            ret = {}
            for i in x:
                if i == chs[0]:
                    dep += 1
                    hold[dep] = pl
                elif i == chs[1]:
                    if depth == 0 or dep <= depth:
                        ret[hold[dep]] = pl
                    dep -= 1
                pl += 1
            return ret
def gz():
    d = [i for i in range(1000000)]

    utils.pkfold.write('main',d,zt='gz',size='1k',thread=True)

    d2 = utils.pkfold.read('main.zip',zt='gz')
    print(d2 == d)
if __name__ == '__main__':
    gz()
