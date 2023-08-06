'''
            Copyright (c) 2022 HOStudio123(ChenJinlin) ,
                      All Rights Reserved.
'''
from platform import python_version
from .hopter import Error_ptc
python_code = python_version().split('.')
if int(python_code[0]) < 3:
  print('E:Sorry, You python version is less than 3.8, and this program cannot be used.')
elif int(python_code[1]) < 8:
  print('E:Sorry, You python version is less than 3.8, and this procedure cannot be used.')
else:
  try:
    from .__main__ import *
  except Exception as e:
    Error_ptc('Sorry,The program has an error and cannot continue to run',str(e))