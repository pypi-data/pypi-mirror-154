#  Copyright (c) 2021 Richard Smith and others
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0.
#
#  This Source Code may also be made available under the following Secondary
#  licenses when the conditions for such availability set forth in the Eclipse
#  Public License, v. 2.0 are satisfied: GNU General Public License, version 2
#  with the GNU Classpath Exception which is
#  available at https://www.gnu.org/software/classpath/license.html.
#
#  SPDX-License-Identifier: EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0

from raylib import rl, ffi

from inspect import ismethod,getmembers,isbuiltin
import inflection

current_module = __import__(__name__)



def pointer(self, struct):
    return ffi.addressof(struct)

LIGHTGRAY  =( 200, 200, 200, 255 )
GRAY       =( 130, 130, 130, 255 )
DARKGRAY   =( 80, 80, 80, 255 )
YELLOW     =( 253, 249, 0, 255 )
GOLD       =( 255, 203, 0, 255 )
ORANGE     =( 255, 161, 0, 255 )
PINK       =( 255, 109, 194, 255 )
RED        =( 230, 41, 55, 255 )
MAROON     =( 190, 33, 55, 255 )
GREEN      =( 0, 228, 48, 255 )
LIME       =( 0, 158, 47, 255 )
DARKGREEN  =( 0, 117, 44, 255 )
SKYBLUE    =( 102, 191, 255, 255 )
BLUE       =( 0, 121, 241, 255 )
DARKBLUE   =( 0, 82, 172, 255 )
PURPLE     =( 200, 122, 255, 255 )
VIOLET     =( 135, 60, 190, 255 )
DARKPURPLE =( 112, 31, 126, 255 )
BEIGE      =( 211, 176, 131, 255 )
BROWN      =( 127, 106, 79, 255 )
DARKBROWN  =( 76, 63, 47, 255 )
WHITE      =( 255, 255, 255, 255 )
BLACK      =( 0, 0, 0, 255 )
BLANK      =( 0, 0, 0, 0 )
MAGENTA    =( 255, 0, 255, 255 )
RAYWHITE   =( 245, 245, 245, 255 )


# I'm concerned that we are doing a lot of string comparisons on every function call to detect types.
# Quickest way would probably be isinstance(result, ffi._backend._CDataBase) but that class name varies
# depending on if binding is static/dynamic
# (and possibly also different on pypy implementations?).
# which makes me reluctant to rely on it.
# Another possibility is ffi.typeof() but that will throw an exception if you give it a type that isn't a ctype
# Another way to improve performance might be to special-case simple types before doing the string comparisons

def makefunc(a):
    #print("makefunc ",a, ffi.typeof(a).args)
    def func(*args):
        modified_args = []
        for (c_arg, arg) in zip(ffi.typeof(a).args, args):
            #print("arg:",str(arg), "c_arg.kind:", c_arg.kind, "c_arg:", c_arg, "type(arg):",str(type(arg)))
            if c_arg.kind == 'pointer':
                if type(arg) == str:
                    arg = arg.encode('utf-8')
                elif type(arg) is bool:
                    arg = ffi.new("bool *", arg)
                elif type(arg) is int:
                    arg = ffi.new("int *", arg)
                elif type(arg) is float:
                    arg = ffi.new("float *", arg)
                elif str(type(arg)) == "<class '_cffi_backend.__CDataOwn'>" and "*" not in str(arg): #CPython
                    arg = ffi.addressof(arg)
                elif str(type(arg)) == "<class '_cffi_backend._CDataBase'>" and "*" not in str(arg): #Pypy
                    arg = ffi.addressof(arg)
            modified_args.append(arg)
        result = a(*modified_args)
        if result is None:
            return
        if str(type(result)) == "<class '_cffi_backend._CDataBase'>" and str(result).startswith("<cdata 'char *'"):
            if str(result) == "<cdata 'char *' NULL>":
                result = ""
            else:
                result = ffi.string(result).decode('utf-8')
        return result
    return func

def makeStructHelper(struct):
    def func(*args):
        return ffi.new(f"struct {struct} *", args)[0]
    return func


for name, attr in getmembers(rl):
    #print(name, attr)
    uname = inflection.underscore(name).replace('3_d','_3d').replace('2_d','_2d')
    if isbuiltin(attr) or str(type(attr)) == "<class '_cffi_backend.__FFIFunctionWrapper'>" or str(type(attr)) == "<class '_cffi_backend._CDataBase'>":
        #print(attr.__call__)
        #print(attr.__doc__)
        #print(attr.__text_signature__)
        #print(dir(attr))
        #print(dir(attr.__repr__))
        f = makefunc(attr)
        setattr(current_module, uname, f)
        #def wrap(*args):
        #    print("call to ",attr)
        #setattr(PyRay, uname, lambda *args: print("call to ",attr))
    else:
        setattr(current_module, name, attr)

for struct in ffi.list_types()[0]:
    f = makeStructHelper(struct)
    setattr(current_module, struct, f)

# overwrite ffi enums with our own
from raylib.enums import *
