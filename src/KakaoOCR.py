
import cv2
import requests
import numpy as np


LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40


def kakao_ocr_resize(image_path: str):
    """
    ocr detect/recognize api helper
    ocr api의 제약사항이 넘어서는 이미지는 요청 이전에 전처리가 필요.

    pixel 제약사항 초과: resize
    용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

    :param image_path: 이미지파일 경로
    :return:
    """
    
    #image = cv2.imread(image_path) #한글 경로 안됨 ㅡㅡ , 따라서 아래와 같이 처리
    img_arr = np.fromfile(image_path, np.uint8)
    image = cv2.imdecode(img_arr, cv2.IMREAD_UNCHANGED)

    height, width, _ = image.shape
    #print(height, width)

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None


def kakao_ocr(image_path: str, appkey: str):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    
    #image = cv2.imread(image_path)  #한글 경로 X, 따라서 아래와 같이 처리
    img_arr = np.fromfile(image_path, np.uint8)
    image = cv2.imdecode(img_arr, cv2.IMREAD_UNCHANGED)

    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"image": data})


# 반환 [닉네임, 직업, 레벨, 직위, 주간미션, 수로, 플래그 ]
def test(image_path):
    #image_path = "img/test2.png"
    appkey = '81cd7707feba4c741cdc6391f99801ff';

    resize_impath = kakao_ocr_resize(image_path)
    if resize_impath is not None:
        image_path = resize_impath
        print("원본 대신 리사이즈된 이미지를 사용합니다.")

    output = kakao_ocr(image_path, appkey).json()
    result = output['result'];
    #print(result);

    return json2arr(result)



def json2arr(json):
    arr = []
    y_p = -10
    row = []

    for i in json:
        y = i['boxes'][0][1]
        info = i['recognition_words'][0];
        if (abs(y - y_p) <= 3) or y_p==-10:
            row.append(info)
        else:
            arr.append(row)
            row = [info]
        y_p = y

    return arr

