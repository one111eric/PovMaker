import scenedetect as sd
import scenedetect.scene_manager as sm
from scenedetect import open_video, SceneManager, ContentDetector
import face_recognition
import os
import subprocess


class PovMaker:
    def __init__(self, sourceDir, scenesDir, screenshotDir, refDir, outputDir):
        self.srcDir = sourceDir
        self.scnDir = scenesDir
        self.ssDir = screenshotDir
        self.refDir = refDir
        self.dstDir = outputDir

    def split(self):
        sd.platform.init_logger(log_level=20, show_stdout=True,
                                log_file="./scenedetect.log")
        sourceVideos = sorted(os.listdir(path=self.srcDir))

        for sourceVideo in sourceVideos:
            video = open_video(os.path.join(self.srcDir, sourceVideo))
            # "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/test.mp4"
            sceneManager = SceneManager()
            sceneManager.add_detector(ContentDetector())
            sceneManager.detect_scenes(video, show_progress=True)

            scenes = sceneManager.get_scene_list()

        sm.save_images(scenes, video, num_images=5, frame_margin=1, image_extension='jpg',
                       encoder_param=90, output_dir=self.ssDir, show_progress=True)
        # print(*scenes, sep="\n")

        # scenesFolder = '/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/outputvideosS1E1/'
        # "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/test.mp4"
        sd.video_splitter.split_video_ffmpeg(os.path.join(self.srcDir, sourceVideo), scenes,
                                             output_file_template=self.scnDir+'/$VIDEO_NAME-Scene-$SCENE_NUMBER.mp4', show_progress=True)

    # split()

    def match(self):
        matchedSceneList = []

        referencePics = os.listdir(path=self.refDir)

        for reference in referencePics:

            referencePic = face_recognition.load_image_file(
                os.path.join(self.refDir, reference))
            referencePicEncoding = face_recognition.face_encodings(referencePic)[
                0]

        screenshots = sorted(os.listdir(path=self.ssDir))

        totalFound = 0

        for pic in screenshots:
            tempPic = face_recognition.load_image_file(
                os.path.join(self.ssDir, pic))
            tempPicEncoding = face_recognition.face_encodings(tempPic)
            print(pic)

            if len(tempPicEncoding) > 0:
                tempFace = tempPicEncoding[0]
                result = face_recognition.compare_faces(
                    [referencePicEncoding], tempFace)

                if result[0] == True:
                    print("found reference in "+pic)
                    if matchedSceneList.count(self.scnDir+"/" + pic.split("-")[0] + "-"+pic.split("-")[1]+"-"+pic.split("-")[2] + ".mp4") == 0:
                        matchedSceneList.append(
                            self.scnDir+"/" + pic.split("-")[0] + "-"+pic.split("-")[1]+"-"+pic.split("-")[2] + ".mp4")
                    totalFound += 1

        print(totalFound)
        print(matchedSceneList)

        f = open("merge.txt", "w")
        for str in matchedSceneList:
            f.write("file '" + str + "'\n")
        f.close()

    # match()

    def merge(self):
        cmd_str = "echo y | ffmpeg -f concat -safe 0 -i merge.txt -c:v copy " + \
            self.dstDir + "/merged.mp4;"
        subprocess.run(cmd_str, shell=True)

    # merge()


# Write some tests
def test_split():
    print("testing split function:")
    maker = PovMaker("/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/source2", '/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/scenes',
                     "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/screenshots", "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/reference", "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/output")
    maker.split()
    print("testing split function done")


# test_split()


def test_match():
    print("testing match function:")
    maker = PovMaker("/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/source2", '/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/scenes',
                     "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/screenshots", "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/reference", "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/output")
    maker.match()
    print("testing match function done")


#test_match()


def test_merge():
    print("testing merge function:")
    maker = PovMaker("/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/source2", '/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/scenes',
                     "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/screenshots", "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/reference", "/Users/mxiang816/Documents/go-workspace/src/code.comcast.com/mxiang816/labweek2023Spring/PovMaker/output")
    maker.merge()
    print("testing merge function done")

#test_split()
#test_match()
#test_merge()
