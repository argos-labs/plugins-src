
import os
import sys
import csv

################################################################################
HEADER = 'index', 'depth', 'subfolder', 'num_subfolders', 'num_files'


################################################################################
def traverse_subfolder(rootfolder, maxdepth=0):
    c = csv.writer(sys.stdout, lineterminator='\n')
    c.writerow(HEADER)
    ndx = 0
    for root, dirs, files in os.walk(rootfolder):
        if root == rootfolder:
            continue

        subf = root[len(rootfolder)+1:]
        sepf = subf.split(os.path.sep)
        depth = len(sepf)
        if maxdepth == 0 or 0 < depth <= maxdepth:
            ndx += 1
            row = (ndx, len(sepf), subf, len(dirs), len(files))
            c.writerow(row)


################################################################################
if __name__ == '__main__':
    traverse_subfolder("subf")
    # traverse_subfolder(r"V:\Bots\SubFolder\올포홈", maxdepth=2)
