import cv2
def get_filtered_image(image,action):
    img=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    if action=='NO FILTER':
        filtered=img
    return filtered    