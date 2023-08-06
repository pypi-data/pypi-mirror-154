#import paddleclas
#model = paddleclas.PaddleClas(model_name="person_exists", batch_size=2)
#results = model.predict(input_data="./docs/images/PULC/docs/")
#for r in results:
#    print(r)
#
#from paddleclas import PaddleClas
#clas = PaddleClas(model_name='ResNet50')
#infer_imgs = 'docs/images/inference_deployment/whl_demo.jpg'
#result=clas.predict(infer_imgs)
#print(next(result))
#
#from paddleclas import PaddleClas
#clas = PaddleClas(inference_model_dir='./inference/')
#infer_imgs = 'docs/images/inference_deployment/whl_demo.jpg'
#result=clas.predict(infer_imgs)
#print(next(result))
#
#from paddleclas import PaddleClas
#clas = PaddleClas(model_name='ResNet50', batch_size=2)
#infer_imgs = 'docs/images/'
#result=clas.predict(infer_imgs)
#for r in result:
#    print(r)

from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50')
infer_imgs = 'http://10.181.196.20:8000/GitHub/PaddleClas/docs/images/inference_deployment/whl_demo.jpg'
result=clas.predict(infer_imgs)
print(next(result))

import cv2
from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50')
infer_imgs = cv2.imread("docs/images/inference_deployment/whl_demo.jpg")[:, :, ::-1]
result=clas.predict(infer_imgs)
print(next(result))

from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50', save_dir='./output_pre_label/')
infer_imgs = 'docs/images/' # it can be infer_imgs folder path which contains all of images you want to predict.
results=clas.predict(infer_imgs)
for r in results:
    print(r)

from paddleclas import PaddleClas
clas = PaddleClas(model_name='ResNet50', class_id_map_file='./ppcls/utils/imagenet1k_label_list.txt')
infer_imgs = 'docs/images/inference_deployment/whl_demo.jpg'
result=clas.predict(infer_imgs)
print(next(result))

