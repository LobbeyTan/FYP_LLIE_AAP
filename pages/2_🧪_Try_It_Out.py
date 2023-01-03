import os
import shutil
from datetime import datetime
from enum import Enum

import pandas as pd
import streamlit as st
import torchvision.transforms as transforms
from PIL import Image
from streamlit_image_select import image_select
from torchvision.transforms import InterpolationMode

from src.enhancer import LowLightImageEnhancer
from src.detector import ObjectDetector
from src.mapping import cls_to_label


class ImageType(Enum):
    ORIGINAL = 1
    ENHANCED = 2
    DETECT_ORIGINAL = 3
    DETECT_ENHANCED = 4
    NONE = -1


def getImageType(filename: str):
    t = ImageType.NONE

    if ('O' in filename):
        t = ImageType.ORIGINAL

    if ('E' in filename):
        t = ImageType.ENHANCED

    if ('DO' in filename):
        t = ImageType.DETECT_ORIGINAL

    if ('DE' in filename):
        t = ImageType.DETECT_ENHANCED

    return t


def getTargetImage(folder: str, target: ImageType, size=256, path_only=False):
    for _, _, files in os.walk(folder):
        for file in files:
            if getImageType(file) == target:
                if path_only:
                    return os.path.join(folder, file)
                return Image.open(os.path.join(folder, file)).resize((size, size))


def getAnnotationDF(folder: str):
    for _, _, files in os.walk(folder):
        for file in files:
            if '.txt' in file:
                df = pd.read_csv(os.path.join(folder, file), delimiter=' ', skiprows=0, names=[
                                 'Label', 'x', 'y', 'w', 'h', 'Conf (%)'])

                df['Label'] = df['Label'].apply(
                    lambda x: "%32s" % cls_to_label[int(x)]
                )

                df['x'] = df['x'].apply(lambda x: "%03d" % (float(x)))
                df['y'] = df['y'].apply(lambda x: "%03d" % (float(x)))
                df['w'] = df['w'].apply(lambda x: "%03d" % (float(x)))
                df['h'] = df['h'].apply(lambda x: "%03d" % (float(x)))

                df['Conf (%)'] = df['Conf (%)'].apply(
                    lambda x: "%2.2f" % (float(x) * 100)
                )

                return df


def transformImage(file):
    transform = transforms.Compose(
        [
            transforms.Resize(286, InterpolationMode.BICUBIC),
            transforms.CenterCrop(size=256),
        ]
    )

    img = transform(Image.open(file))

    return img


def createTempZipFile(folder):
    return shutil.make_archive('./temp/result', "zip", folder)


@st.cache
def createTempFolder():
    path = os.getcwd() + '/temp'

    try:
        os.mkdir(path)
    except:
        pass


@st.cache(allow_output_mutation=True)
def loadModels():
    # Load models
    enhancer = LowLightImageEnhancer()
    detector = ObjectDetector()

    return enhancer, detector


def enhanceAndDetect(img: Image):
    path = os.getcwd() + '/temp/output'

    shutil.rmtree(path, ignore_errors=True)

    os.mkdir(path)

    original_img = img
    enhanced_img = enhancer.process(original_img)
    detected_original, detected_enhanced = detector.predict(original_img, enhanced_img)

    fname = datetime.now().strftime("%Y%m%d")

    original_img.save(path + "/%s_O.png" % fname)
    enhanced_img.save(path + "/%s_E.png" % fname)
    detected_original.save(path + "/%s_DO.png" % fname)
    detected_enhanced.save(path + "/%s_DE.png" % fname)

    return [original_img, enhanced_img, detected_original, detected_enhanced], path


st.set_page_config(layout="wide", page_title="Low Light Image Enhancement")

st.header("Enhance And Detect Object in Low Light Image")

with st.spinner(text="Loading models ..."):
    createTempFolder()
    enhancer, detector = loadModels()

st.sidebar.write("## Upload or Select :gear:")

my_upload = st.sidebar.file_uploader(
    "Upload an image", type=["png", "jpg", "jpeg"],
)

sampleImages = [[os.path.join(root, file) for file in files]
                for root, _, files in os.walk(os.getcwd() + '/pictures/sample') if len(files) != 0][0]

with st.sidebar:
    idx = image_select(
        label="Select a low light image",
        use_container_width=False,
        return_value="index",
        images=sampleImages,
    )

img = transformImage(sampleImages[idx] if my_upload is None else my_upload)

processed_imgs, tmp_path = enhanceAndDetect(img)

col1, col2, col3 = st.columns(3)


col1.image(processed_imgs[0], caption="Original Image", use_column_width=True,)

col2.image(processed_imgs[1], caption="Enhanced Image", use_column_width=True)

col1.image(processed_imgs[2], caption="Detection Image", use_column_width=True)

col2.image(processed_imgs[3], caption="Detection and Enhanced Image", use_column_width=True)

result_path = createTempZipFile(tmp_path)

with open(result_path, "rb") as file:
    col3.download_button("Download Result", data=file, mime="application/zip", file_name='result.zip')

col3.write("**Running time**: {:.2f}s".format(enhancer.running_time + detector.running_time))

col3.table(getAnnotationDF(tmp_path))
