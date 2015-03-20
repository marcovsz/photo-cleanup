#! /usr/bin/python
# coding=utf-8
#  marksz@foxmail.com

import string, os, sys, filecmp, shutil, re, stat, time, EXIF

if __name__ == "__main__":    
    if len(sys.argv) != 3:
        print "Usage: photosync.py src_folder dst_folder"
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    
    file_filter = ['.jpg', '.mov', '.mp4', '.3gp'];
    
    
    count = 0;
    for root, dirs, files in os.walk(src):
        sum = len(files)
        print "total %d files" %sum
        for f in files:
            count = count + 1
            matched = False
            lower_f = string.lower(f)
            for surfix in file_filter:
                if (lower_f.endswith(surfix)):
                    matched = True;
                    break
            if matched == False:
                files.remove(f)
                continue      
            
            # extract date info, first from file name, if failed, try file's properties
            match = re.search("[a-zA-Z]+_\d+_\d+\.", lower_f)
            if match:
                year  = int(match.group()[match.group().find('_')+1:match.group().find('_')+5])
                month = int(match.group()[match.group().find('_')+5:match.group().find('_')+7])
                #print  u'%d年%d月' %(year, month)
            else:
                t = time.localtime(os.stat(os.path.join(root, f))[stat.ST_MTIME])
                year  = t.tm_year
                month = t.tm_mon
                #print os.stat(os.path.join(root, f)).st_mtime
                #print  "%d年%d月" %(t.tm_year, t.tm_mon)
            
            # read EXIF date of JPG file
            if lower_f.endswith('.jpg'):
                # Open image file for reading (binary mode)
                jpg = open(os.path.join(root, f), 'rb')
                tags = EXIF.process_file(jpg)
                keys = ['EXIF DateTime', 'EXIF DateTimeOriginal', 'EXIF DateTimeDigitized']
                if not tags:
                    print 'No EXIF information found'
                else:
                    for key in keys:
                        tmp_year = 0
                        tmp_month = 0
                        if key in tags.keys():
                            #print key + ":" + tags[key].printable
                            exif_year = int(tags[key].printable[0:4])
                            exif_month = int(tags[key].printable[5:7])
                            if tmp_year <= exif_year:
                                tmp_year  = exif_year
                                tmp_month = exif_month
                            #print  u'%d年%d月' %(exif_year, exif_month)
            #  fix date if needed
            if tmp_year != 0:
                year  = tmp_year
                month = tmp_month 
            
            #  find destination folder 
            #  create folder if not exists
            if (os.path.exists(os.path.join(dst.decode('gbk'), u'%d年' %(year)))) == False :
                print (os.path.join(dst.decode('gbk'), u'%d年' %(year)))
                os.makedirs(os.path.join(dst.decode('gbk'), u'%d年' %(year)))
            if (os.path.exists(os.path.join(dst.decode('gbk'), u'%d年/%d年%d月' %(year, year, month)))) == False :
                os.makedirs(os.path.join(dst.decode('gbk'), u'%d年/%d年%d月' %(year, year, month)))
            if (os.path.exists(os.path.join(dst.decode('gbk'), u'%d年/%d年%d月/%s' %(year, year, month, f.decode('gbk'))))) == False :
                shutil.copy2(os.path.join(root, f), os.path.join(dst.decode('gbk'), u'%d年/%d年%d月/%s' %(year, year, month, f.decode('gbk'))))
                print u'Copy %s to %s Done' %(os.path.join(root.decode('gbk'), f.decode('gbk')), os.path.join(dst.decode('gbk'), u'%d年/%d年%d月/' %(year, year, month)))
            else:
                print "%s exists, skip copy" %(os.path.join(dst.decode('gbk'), u'%d年/%d年%d月/%s' %(year, year, month, f.decode('gbk')))) 
