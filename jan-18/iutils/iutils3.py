import pickle as pkl
import zipfile as zf
import gzip as zfg
import os
import time
import math
import time
import shutil
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
                with zf.ZipFile(zipname,mode='w') as zipobj:
                    if isinstance(filename,list):
                        for nw in filename:
                            zipobj.write(nw)
                    else:
                        zipobj.write(filename)
            elif fe == 'gz' or fe == 'pkz':
                with zfg.open(zipname,mode='wb') as zipobj:
                    zipobj.write(open(filename,'rb').read())
        def read(zipname,*args):
            utils.error.no_file_err(zipname)
            utils.error.file_zip_name_err(zipname)
            fe = zipname.split('.')[-1]
            if fe == 'zip':
                with zf.ZipFile(zipname) as zipobj:
                    if args == []:
                        filename = zipobj.namelist()[0]
                    else:
                        filename = args[0]
                    with zipobj.open(filename,mode='r') as f:
                        return f.read()
            elif fe == 'gz' or fe == 'pkz':
                with zfg.open(zipname) as zipobj:
                    return zipobj.read()
        def output(zipfile,filename):
            d = utils.zipf.read(zipfile,filename)
            open(filename,'wb').write(d)
    class pkz:
        def write(zipname,data,tempname=None):
            utils.error.no_file_err(zipname)
            if tempname in [None]:
                tempname = 'data.pkl'
            utils.error.file_name_err(tempname)
            utils.pickle.write(tempname,data)
            utils.zipf.write(zipname,tempname)
            os.remove(tempname)
        def read(zipname,tempname=None):
            utils.error.no_file_err(zipname)
            if tempname in [None,'']:
                tempname = 'data.pkl'
            utils.error.file_name_err(tempname)
            utils.zipf.output(zipname,tempname)
            out = utils.pickle.read(tempname)
            os.remove(tempname)
            return out
    class slice:
        def split(filename,*args,size=None):
            if isinstance(size,int):
                size = int(size)
            if isinstance(size,str):
                if size[-1] in ['b','B']:
                    size = size[:-1]
                size = int(size[:-1])*{'k':1000,'K':1000,'m':1000**2,'M':1000**2,'g':1000**3,'G':1000**3}[size[-1]]
            if size == None:
                size = 4000
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
                open(outname+'/'+str(pl),'wb').write(f[i:i+size])
        def join(foldername,*args):
            if len(args) == 0:
                outname = './'+foldername+'_'
            else:
                outname = args[0]
            names = []
            for i in os.listdir(foldername):
                names.append(int(i))
            names.sort()
            if outname in os.listdir():
                os.remove(outname)
            f = open(outname,'ab')
            for i in names:
                cfile = foldername+'/'+str(i)
                f.write(open(cfile,'rb').read())
    class pkfold:
        def write(foldername,data,zt='zip',size='1m'):
            utils.pkz.write('main.'+zt,data)
            utils.slice.split('main.'+zt,foldername,size=size)
            if 'main.'+zt in os.listdir():
                os.remove('main.'+zt)
        def read(foldername,zt='pkz'):
            utils.slice.join(foldername,'replica.'+zt)
            out = utils.pkz.read('replica.'+zt)
            os.remove('replica.'+zt)
            return out
    class shell:
        def ls(path):
            return os.listdir(path)
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
if __name__ == '__main__':
    utils.zipf.write('main.zip',['main.py','main'])
