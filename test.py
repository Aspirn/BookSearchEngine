from aip import AipOcr
import os

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content(os.getcwd() + '/data/results/test1.png')


APP_ID = '10634722'
API_KEY = '9T9pkzckvioQ9pocGHLPnaBd'
SECRET_KEY = 'ULMstHiUUKRRheOGrBnZRi5DjGHtVNzx'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"


print client.basicGeneral(image, options)

