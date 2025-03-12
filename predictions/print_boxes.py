import cv2 as cv
import pandas as pd 
from .models import DetectionResult, PredictionResult
from joblib import load
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
model = load('./saved_model/model.joblib')
scaler = load('./saved_model/scaler.joblib')

def calculate_iou(box1, box2):
    x1_max = max(box1[0], box2[0])
    y1_max = max(box1[1], box2[1])
    x2_min = min(box1[2], box2[2])
    y2_min = min(box1[3], box2[3])

    # คำนวณพื้นที่ของการซ้อนทับ (intersection area)
    overlap_area = max(0, x2_min - x1_max + 1) * max(0, y2_min - y1_max + 1)

    # คำนวณพื้นที่ของ box1 และ box2
    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    # คำนวณพื้นที่รวมของ box1 และ box2 (union area)
    total_area = box1_area + box2_area - overlap_area

    # คำนวณค่า IoU
    iou = overlap_area / total_area if total_area > 0 else 0
    rounded_iou = round(iou, 2)
    return rounded_iou

def filter_duplicate_boxes(boxes):
    filtered_boxes = []

    # ตรวจสอบแต่ละคู่ของกรอบ
    for i in range(len(boxes)):
        box1 = boxes[i]
        x1, y1, x2, y2 = map(int, box1.xyxy[0].tolist())
        keep = True  # Flag เพื่อเก็บกรอบที่ไม่ซ้ำ

        for j in range(i):

            box2 = boxes[j]
            p, q, r, s = map(int, box2.xyxy[0].tolist())

            iou = calculate_iou([x1, y1, x2, y2], [p, q, r, s])

            if 1> iou >= 0.5:
                keep = False  # หาก IoU เกินเกณฑ์ ไม่เก็บกรอบนั้น
                break

        if keep:
            filtered_boxes.append(box1)  # เก็บกรอบที่ไม่ซ้ำลงใน list

    return filtered_boxes
def class_label(class_name):
    """
    แปลงชื่อคลาสเป็นค่าตัวเลข
    :param class_name: ชื่อคลาส ('good' หรือ 'excellent')
    :return: 0 ถ้า class_name=='good', 1 ถ้า class_name=='excellent'
    """
    if class_name == 'good':
        return 0
    elif class_name == 'excellent':
        return 1
    else:
        raise ValueError("Invalid class_name. Expected 'good' or 'excellent'.")


def findRefBox(results):
    coin_diameter_mm = 26
    for result in results:
        boxes = result.boxes
        filtered_boxes = filter_duplicate_boxes(boxes)
        for box in filtered_boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            
            # ดึงชื่อคลาสตาม ID
            class_name = result.names[class_id]
            if class_name == 'ref':

                global ref_width_px
                global ref_height_px
                global ref_diameter_px

                ref_width_px = x2 - x1
                ref_height_px = y2 - y1
                ref_diameter_px = max(ref_width_px,  ref_height_px)
                pixel_per_mm = ref_width_px / coin_diameter_mm
                return x1, y1, x2, y2, pixel_per_mm 

def findNotRefBox(results, pixel_per_mm, image, global_counter, last_upload_date):
    
    fruit_counter =  global_counter
    for result in results:
        boxes = result.boxes
        empty_df = pd.DataFrame({
                        'ID': [],
                        'width_cm': [],
                        'height_cm': [],
                        'width_px': [],
                        'height_px': [],
                        'ref_width_px': [],
                        'ref_height_px': [],
                        'x1': [],
                        'y1': [],
                        'x2': [],
                        'y2': [],
                        'dummy_class_name': []
                    })
        
        filtered_boxes = filter_duplicate_boxes(boxes)
        for box in filtered_boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = result.names[class_id]
            print(class_name)
            print("x1 y1 x2 y2",(x1, y1, x2, y2))
            if class_name == 'excellent'or class_name=='good':
                if pixel_per_mm is not None:
                    width_px = x2 - x1 
                    height_px = y2 - y1
                    width_mm = width_px / pixel_per_mm 
                    width_cm = width_mm / 10
                    height_mm = height_px / pixel_per_mm 
                    height_cm = height_mm / 10
                    dummy_class_name = class_label(class_name)
                    new_row = {
                        'ID': fruit_counter,
                        'width_cm': width_cm,
                        'height_cm': height_cm,
                        'width_px': width_px,
                        'height_px': height_px,
                        'ref_width_px': ref_width_px,
                        'ref_height_px': ref_height_px,
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2,
                        'dummy_class_name': class_label(class_name)
                    }

                    detectionresult_inst = DetectionResult(jujubeimage_id= last_upload_date )
                    detectionresult_inst.counter = fruit_counter
                    detectionresult_inst.width_cm = width_cm
                    detectionresult_inst.height_cm = height_cm 
                    detectionresult_inst.width_pixel = width_px
                    detectionresult_inst.height_pixel = height_px
                    detectionresult_inst.ref_width_pixel = ref_width_px
                    detectionresult_inst.ref_height_pixel = ref_height_px
                    detectionresult_inst.x1=x1
                    detectionresult_inst.y1=y1
                    detectionresult_inst.x2=x2
                    detectionresult_inst.y2=y2
                    detectionresult_inst.dummy_class_name = dummy_class_name
                    print("detectionresult_inst",detectionresult_inst.width_cm)
                    detectionresult_inst.save()
                    
                    x_train = np.array([[width_cm ,height_cm, width_px,height_px, ref_width_px, ref_height_px, dummy_class_name ]])
                    scaled_x_train = scaler.transform(x_train)
                    y_pred = model.predict(scaled_x_train )
                    first_ypred_arr = y_pred.reshape(1,)
                    first_ypred = first_ypred_arr[0]
                    print('first_ypred_shape:',first_ypred.shape)
                    print('first_ypred:',first_ypred)
                    rouneded_first_ypred = round(first_ypred,2)
                    p = PredictionResult.objects.create(weight_gram=rouneded_first_ypred ,detectionresult=detectionresult_inst)
                    print('p',p)
                    empty_df.loc[len(empty_df)] = new_row

                    if  first_ypred>20:    
                        b, g, r = 0, 100, 54
                    elif  20>=first_ypred>=16:
                        b, g, r = 309, 77, 53
                    elif  16>first_ypred:
                        b, g, r = 309, 77, 53
                    image = cv.rectangle(image, (x1, y1), (x2, y2), (b, g, r), 3)
                    image = cv.putText(image, f'ID: {fruit_counter}', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.95, (0, 0, 0), 2) 
                    print("rec_tangle_worked")
                fruit_counter += 1
    return  image, empty_df, fruit_counter


def detect_and_measure_diameter(mymodel, image_path, global_counter, last_upload_date):
    image = cv.imread(image_path)
    # ปรับขนาดภาพ
    image = cv.resize(image, (640, 640))
    results = mymodel.predict(source=image)
    pixel_per_mm = None
    print("results:" ,results)
    print("findRefBox",findRefBox(results))
    x1, y1, x2, y2, pixel_per_mm = findRefBox(results)

    # วาด bounding box ของเหรียญในภาพ
    image = cv.rectangle(image, (x1, y1), (x2, y2), (61, 81, 93), 3)
    image = cv.putText(image, f'Reference (10 Baht coin)', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.95, (0, 0, 0), 2)

    image, empty_df, fruit_counter = findNotRefBox(results, pixel_per_mm, image, global_counter, last_upload_date)
    
    return image, empty_df, fruit_counter
