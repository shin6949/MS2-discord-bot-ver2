import os


# 다운로드한 프로필 사진, 길드 로고 삭제
def delete_png():
    path = "./"
    files = os.listdir(path)

    for file in files:
        tmp = "{}/{}".format(path, file)
        name, exten = os.path.splitext(tmp)

        if exten == ".png":
            if os.path.isfile(tmp):
                try:
                    os.remove(tmp)
                except Exception as e:
                    print(e)

