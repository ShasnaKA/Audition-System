import os
import shutil
import cv2
import string
import random # define the random module

def get_random_str():
	S = 10  # number of characters in the string.
	# call random.choices() string module to find the string in Uppercase + numeric data.
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
	print("The randomly generated string is : " + str(ran)) # print the random data
	return ran


def initDir(file_path):
    shutil.rmtree(file_path, ignore_errors=True)
    os.mkdir(file_path);

def extract_face(infile,outdir,pos):

    imagePath = infile

    #sys.argv[1]

    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
        )

    print("[INFO] Found {0} Faces.".format(len(faces)))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w]
        print("[INFO] Object found. Saving locally.")
        cv2.imwrite(f'{outdir}/{pos}_faces.jpg', roi_color)

    #status = cv2.imwrite(f'{outdir}/faces_detected.jpg', image)
    #print("[INFO] Image faces_detected.jpg written to filesystem: ", status)


def save_face_pics(pic_dir,face_dir):
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(pic_dir):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    print('Total File :',len(listOfFiles))
    cnt=0
    r_file_name = get_random_str()
    for file in listOfFiles:
        extract_face(file,face_dir,f'{r_file_name}_{cnt}')
        cnt += 1
initDir('C:/Users/HP/PycharmProjects/AuditionCastPlay/project/pics_cropped/new')
save_face_pics('C:/Users/HP/PycharmProjects/AuditionCastPlay/project/pics_to_crop/new','C:/Users/HP/PycharmProjects/AuditionCastPlay/project/pics_cropped/new')

