"""
Python file that helps deleting old directories to save storage on VMs.
Currently the logic is to delete any directory which has timestamp of more than 2 weeks.
"""
import os, shutil, re
from datetime import datetime
path = r"/abc/def/ghi/"
print("path from where directores will be deleted: ",path)
count =0
d = datetime.today()
print("\nToday is : ",d)
for f in (os.listdir(path)):
    try:
        print("\nDirectory under consideration for deletion: ",f)
        match=re.search(r'\d{8}\.',f)
        s = match.group(0)
        if s is None:
          print("Directory {} will not be deleted because it is not the targeted directory".format(f))
          continue
        sval = s[:-1]
        dt = datetime.strptime(sval, '%Y%m%d')
        dif = abs((d-dt).days)
        print("Directory {0} is created {1} days ago.".format(f,dif))
        if dif > 14:
            print(os.path.join(path,f))
            shutil.rmtree(os.path.join(path, f))
            print("Directory {} is deleted".format( f))
            count += 1
        else:
            print("Directory {} is not deleted because it is created less than 14 days ago".format(f))
            count = count
    except Exception as e:
        print("Directory {} will not be deleted because it is not the targeted directory".format(f))
        continue
print("\nTotal no. of directories deleted : ",count)