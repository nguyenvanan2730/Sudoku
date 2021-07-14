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
        ret, frame = capture.read()
        if ret == False:
            print('カメラから画像を取得できませんでした。')
            break
        
        #グレイスケール
        #gray = cv2.cvt＃olor(frame, cv2.COLOR_BGR2GRAY)
        
        #起動平滑化
        #dst = cv2.equalizeHist(gray)

        #get the board (canny 処理)
        #dst = cv2.Canny(frame, 40.0, 200.0)
        #dst = cv2.bitwise_not(dst)

        #affin_trans = cv2.getRotationMatrix2D(center, degree, 1.0)
        #dst = cv2.warpAffine(frame, affin_trans, (width, height))
        #degree += 1.0

        #cv2.imshow('Camera',dst)

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