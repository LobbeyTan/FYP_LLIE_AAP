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


def getTargetImage(folder: str, target: ImageType, size=256):
    for _, _, files in os.walk(folder):
        for file in files:
            if getImageType(file) == target:
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

                df['x'] = df['x'].apply(lambda x: "%03d" % (float(x) * 256))
                df['y'] = df['y'].apply(lambda x: "%03d" % (float(x) * 256))
                df['w'] = df['w'].apply(lambda x: "%03d" % (float(x) * 256))
                df['h'] = df['h'].apply(lambda x: "%03d" % (float(x) * 256))

                df['Conf (%)'] = df['Conf (%)'].apply(
                    lambda x: "%2.2f" % (float(x) * 100)
                )

                return df


def saveImage(file):
    transform = transforms.Compose(
        [
            transforms.Resize(286, InterpolationMode.BICUBIC),
            transforms.CenterCrop(size=256),
        ]
    )

    img = transform(Image.open(file))

    path = os.getcwd() + r'/temp/output'

    shutil.rmtree(path, ignore_errors=True)

    os.mkdir(path)

    img.save(path + "/%s_O.png" % (datetime.now().strftime("%Y%m%d")))

    return path


def createTempZipFile(folder):
    return shutil.make_archive('./temp/result', "zip", folder)


# Load models
enhancer = LowLightImageEnhancer()

st.set_page_config(layout="wide", page_title="Low Light Image Enhancement")

st.header("Enhance And Detect Object in Low Light Image")

st.sidebar.write("## Upload or Select :gear:")

my_upload = st.sidebar.file_uploader(
    "Upload an image", type=["png", "jpg", "jpeg"],
)

folders = [root for root, _, files in os.walk(
    os.path.join(os.getcwd(), 'pictures')) if len(files) != 0]


col1, col2, col3 = st.columns(3)

with st.sidebar:
    idx = image_select(
        label="Select a low light image",
        use_container_width=False,
        return_value="index",
        images=[getTargetImage(folder, ImageType.ORIGINAL)
                for folder in folders],
    )

target_folder = folders[idx] if my_upload is None else saveImage(my_upload)

original_img = getTargetImage(target_folder, ImageType.ORIGINAL)

col1.image(original_img, caption="Original Image", use_column_width=True,)

if 'temp' in target_folder:
    enhanced_img = enhancer.process(original_img)

# col1.image(getTargetImage(
#     target_folder, ImageType.DETECT_ORIGINAL), caption="Detection Image", use_column_width=True)

col2.image(getTargetImage(
    target_folder, ImageType.ENHANCED), caption="Enhanced Image", use_column_width=True)

# col2.image(getTargetImage(
#     target_folder, ImageType.DETECT_ENHANCED), caption="Detection and Enhanced Image", use_column_width=True)

# result_path = createTempZipFile(target_folder)

# with open(result_path, "rb") as file:
#     col3.download_button("Download Result", data=file,
#                          mime="application/zip", file_name='result.zip',
#                          )

# col3.table(getAnnotationDF(target_folder))
