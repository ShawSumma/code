import pickle as pkl
import zipfile as zf
import gzip as zfg
import os
import time
import math
import sys
import argparse
import time
class utils:
    class error():
        def no_file_err(name):
            name_split = name.split('/')
            pref = ''.join([i+'/' for i in name_split[:-1]])[:-1]
            f = name_split[-1]
            lstd = os.listdir(pref)
            if not f in lstd:
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
            if fe != 'zip' and fe != 'gz':
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
            if not name in os.listdir():
                utils.error('file not found')
            with open(name,'rb') as f:
                return pkl.load(f)
    class zipf:
        def write(zipname,filename):
            utils.error.file_name_err(filename)
            utils.error.file_name_err(zipname)
            fe = zipname.split('.')[-1]
            if fe == 'zip':
                with zf.ZipFile(zipname,mode='w') as zipobj:
                    zipobj.write(filename)
            elif fe == 'gz':
                with zfg.open(zipname,mode='wb') as zipobj:
                    zipobj.write(open(filename,'rb').read())
        def read(zipname,*args):
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
            elif fe== 'gz':
                with zfg.open(zipname) as zipobj:
                    return zipobj.read()
        def output(zipfile,filename):
            d = utils.zipf.read(zipfile,filename)
            open(filename,'wb').write(d)
    class pkz:
        def write(data,zipname,tempname=None):
            if tempname in [None]:
                tempname = 'data.pkl'
            utils.error.file_name_err(tempname)
            utils.pickle.write(tempname,data)
            utils.zipf.write(zipname,tempname)
            os.remove(tempname)
        def read(zipname,tempname=None):
            if tempname in [None,''] or isinstance(tempname,int):
                tempname = 'data.pkl'
            utils.error.file_name_err(tempname)
            utils.zipf.output(zipname,tempname)
            out = utils.pickle.read(tempname)
            os.remove(tempname)
            return out
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
def vtest():
    def argp():
        global parser
        parser = argparse.ArgumentParser()
        parser.add_argument('-o',type=str)
        parser.add_argument('-f',type=str)
        parser.add_argument('-t',type=str)
        parser.add_argument('-F',action='store_true')
    argp()
    args = {
        'f' : parser.parse_args().f,
        'o' : parser.parse_args().o,
        't' : parser.parse_args().t
    }
    if args['f'] != None:
        if args['t'] == None:
            args['t'] = 'DEMO'
        if parser.parse_args().F:
            oa = args['t']
            args['t'] = open(args['t']).read()
            time.sleep(1)
            open(oa,'w').write('')
        utils.pkz.write(args['t'],args['f'])
    if args['o'] != None:
        o = utils.pkz.read(args['o'])
        print(o)
if __name__ == '__main__':
    vtest()
