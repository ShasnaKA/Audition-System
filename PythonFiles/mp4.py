
import subprocess,os

def convert(batpath,ifile,tar):
    cmd=f"ffmpeg -i {ifile} -vf fps=3 {tar}\\frame_%03d.jpg"
    cmdfile=batpath#"v.bat"
    obj=open(cmdfile,"w")
    obj.write(cmd)
    obj.close()
    rtcode=subprocess.call(cmd,shell=True)
    print(rtcode)

#convert('head-pose-face-detection-female.mp4','extrated_frames')


#def dire(path):
 #   with os.scandir(path) as dirs:
  #      for entry in dirs:
   #         print(entry.name)

#dire('pic')