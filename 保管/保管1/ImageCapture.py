# import cv2
# import numpy as np
# from chainer import Chain, serializers
# import chainer.functions as F
# import chainer.links as L
import cv2

try:
    capture = cv2.VideoCapture(0) # 0 というのはノットのカーメラ
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    center = (width//2, height//2)
    degree = 0.0

    print("frame size = " + str(width) + "x" + str(height))
    
    while(True):
        ret, image = capture.read()
        if ret == False:
            print('カメラから画像を取得できませんでした。')
            break
        
        cv2.rectangle(image,(269,189),(371,291),(0,0,255),1)
        cv2.imshow("Capture",image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()




except:
    import sys
    print("Erro:", sys.exc_info()[0])
    print(sys.exc_info()[1])
    import traceback
    print(traceback.format_tb(sys.exc_info()[2]))