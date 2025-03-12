from django.shortcuts import get_object_or_404, render,  redirect
from django.template.loader import render_to_string
import base64, io, uuid, json, os
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.base import ContentFile
from mysite import settings
import cv2 as cv
from .jujubeform import JujubeForm
from django.contrib import messages
from .models import DetectionResult, JujubeImage
from django.core.files import File
from .print_boxes import detect_and_measure_diameter
from.load_model import load_yolo_model
import qrcode
from io import BytesIO
from django.http import HttpResponse
import requests
mymodel = load_yolo_model('mymodel')

    
def feature_1(request):
    show_video=False
    if request.method=='POST':
        print("request.POST:", request.POST)
        if request.FILES.get('image'):
            image = request.FILES['image']
            print('image',image)
            new_jujubeimage_inst = JujubeImage(jujube_image=image)
            new_jujubeimage_inst.save()
            ascending_current_uploaded_images = JujubeImage.objects.all().order_by('-upload_date')
            last_uploaded_image = ascending_current_uploaded_images[0]
            last_uploaded_image_path = last_uploaded_image.jujube_image.name
            image_path = os.path.join(settings.MEDIA_ROOT, last_uploaded_image_path).replace("\\", "/")
            global_counter = 1
            last_upload_date = last_uploaded_image.upload_date

            image, empty_df, fruit_counter = detect_and_measure_diameter(
                mymodel, image_path, global_counter, last_upload_date
            )
            ret, buf = cv.imencode('.png', image)
            content = ContentFile(buf.tobytes())
            last_uploaded_image.detected_image.save("output.jpg", content)

            # Add a success message
            messages.success(request, "Image processed successfully!")
            print("ascending_current_uploaded_images", ascending_current_uploaded_images)
            last_uploaded_image = ascending_current_uploaded_images[0]
            detectionresult_list = DetectionResult.objects.all().filter( jujubeimage_id = last_uploaded_image.upload_date)
            return redirect('/prediction_results')
        if 'back' in request.POST:
            request.session.flush()
            print("///")
            return redirect('/')
        if  "mycamera" in request.POST:
            show_video=True 
            print("show_video",show_video)
            return render(request,"predictions/index.html",{"show_video": show_video})
        if 'takemycamera' in request.POST:
            canvasData= request.POST.get('takemycamera', '')
            format, imgstr = canvasData.split(';base64,')  # แยก header และ base64
            ext = format.split('/')[-1]  # หานามสกุลไฟล์ (เช่น png, jpg)
            file_name = f"{uuid.uuid4()}.{ext}"  # สร้างชื่อไฟล์แบบสุ่ม
            print('file_name:',file_name)
            # สร้างไฟล์จาก Base64
            image_data = ContentFile(base64.b64decode(imgstr))
       
            new_jujubeimage = JujubeImage()
            

            decoded_data = base64.b64decode(imgstr)

            # 2. Write to a buffer (io.BytesIO)
            buf = io.BytesIO()
            buf.write(decoded_data)
            buf.seek(0)  # Rewind the buffer to the beginning

            # 3. Convert the buffer to ContentFile
            new_image_data = ContentFile(buf.getvalue())



            # กำหนด image ให้กับ field jujube_image
            new_jujubeimage.jujube_image.save('new_tj.jpg', new_image_data)

            # บันทึกข้อมูล
            new_jujubeimage.save()
            ascending_current_uploaded_images = JujubeImage.objects.all().order_by('-upload_date')
            last_uploaded_image = ascending_current_uploaded_images[0]
            last_uploaded_image_path = last_uploaded_image.jujube_image.name
            image_path = os.path.join(settings.MEDIA_ROOT, last_uploaded_image_path).replace("\\", "/")
            global_counter = 1
            last_upload_date = last_uploaded_image.upload_date

            image, empty_df, fruit_counter = detect_and_measure_diameter(
                mymodel, image_path, global_counter, last_upload_date
            )
            ret, buf = cv.imencode('.png', image)
            content = ContentFile(buf.tobytes())
            last_uploaded_image.detected_image.save("output.jpg", content)

            # Add a success message
            messages.success(request, "Image processed successfully!")
            return redirect('/prediction_results') 

    ascending_current_uploaded_images = JujubeImage.objects.all().order_by('-upload_date')
    if  len(ascending_current_uploaded_images)==0:
        return render(request, "predictions/index.html")
    return render(request, "predictions/index.html",{"show_video": show_video})


def feature_2(request):
    show_video = False
    if request.method=='POST':
        if request.FILES.get('image'):
            print("request.POST:", request.POST)
            image = request.FILES['image']
            print('image',image)
            new_jujubeimage_inst = JujubeImage(jujube_image=image)
            new_jujubeimage_inst.save()
            ascending_current_uploaded_images = JujubeImage.objects.all().order_by('-upload_date')
            last_uploaded_image = ascending_current_uploaded_images[0]
            last_uploaded_image_path = last_uploaded_image.jujube_image.name
            image_path = os.path.join(settings.MEDIA_ROOT, last_uploaded_image_path).replace("\\", "/")
            global_counter = 1
            last_upload_date = last_uploaded_image.upload_date

            image, empty_df, fruit_counter = detect_and_measure_diameter(
                mymodel, image_path, global_counter, last_upload_date
            )
            ret, buf = cv.imencode('.png', image)
            content = ContentFile(buf.tobytes())
            last_uploaded_image.detected_image.save("output.jpg", content)

            # Add a success message
            messages.success(request, "Image processed successfully!")
            print("ascending_current_uploaded_images", ascending_current_uploaded_images)
            last_uploaded_image = ascending_current_uploaded_images[0]
            detectionresult_list = DetectionResult.objects.all().filter( jujubeimage_id = last_uploaded_image.upload_date)
            return redirect('/prediction_results')
        if 'back' in request.POST:
            request.session.flush()
            return redirect('/')
        if  "mycamera" in request.POST:
            show_video=True 
            print("show_video",show_video)
            return render(request,"predictions/index.html",{"show_video": show_video})
    # if request.method=='GET':
    #     if 'back' in request.GET:
    #         return redirect('/')



    ascending_current_uploaded_images = JujubeImage.objects.all().order_by('-upload_date')
    last_uploaded_image = ascending_current_uploaded_images[0]
    detectionresult_list = DetectionResult.objects.all().filter( jujubeimage_id = last_uploaded_image.upload_date)
    # Compute summation and mean
    total_weight = sum(result.predictionresult.weight_gram for result in detectionresult_list)
    mean_weight = total_weight / len(detectionresult_list) if detectionresult_list else 0
    
    return render(request, "predictions/index.html",{'last_uploaded_image': last_uploaded_image,'detectionresult_list': detectionresult_list,'total_weight': total_weight,'mean_weight': mean_weight,'show_video': show_video})

def generate_qr(request):
    # Get the ngrok URL dynamically (or manually set it)
    ngrok_url = "https://76b0-202-28-118-100.ngrok-free.app"  # Replace with your ngrok URL

    # Generate the QR Code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(ngrok_url)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # Convert image to BytesIO and serve as HTTP response
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")











# def feature(request):
#     if request.method == 'POST':
#         if 'reset' in request.POST:  # ตรวจสอบว่าผู้ใช้กดปุ่มรีเซ็ต
#             # ลบภาพและข้อมูลที่เกี่ยวข้องจาก JujubeImage
#             JujubeImage.objects.all().delete()
#             return render(request, "predictions/index.html", {'form': JujubeForm()})
        
#         form = JujubeForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             form.save()
           
         
            
#             mymodel = load_yolo_model('mymodel')
#             ascending_current_uploaded_images  = JujubeImage.objects.all().order_by('-upload_date')
#             last_uploaded_image = ascending_current_uploaded_images[0]
#             print('last_upload_image: ', last_uploaded_image)
#             # print("last_uploaded_image['jujube_image']", last_uploaded_image.jujube_image.name)
#             last_uploaded_image_path = last_uploaded_image.jujube_image.name
#             image_path = os.path.join(settings.MEDIA_ROOT, last_uploaded_image_path ).replace("\\", "/")
#             global_counter = 1
#             print("last_uploaded_image.update_date",last_uploaded_image.upload_date)
#             last_upload_date= last_uploaded_image.upload_date
#             print("image_path: ",image_path)
#             image, empty_df, fruit_counter = detect_and_measure_diameter(mymodel, image_path, global_counter,  last_upload_date)
           
#             ret, buf = cv.imencode('.png', image)

#             print('empty_df',empty_df)


#             content = ContentFile(buf.tobytes())

            

#             last_uploaded_image.detected_image.save("output.jpg", content)
            
#             # ดึงข้อมูลจาก PredictionResult และ DetectionResult
#             prediction_results = PredictionResult.objects.all().values('detectionresult_id', 'weight_gram')
#             detection_results = DetectionResult.objects.all().values('id', 'counter')
#             print("prediction_results :",prediction_results)
#             print("detection_results :",detection_results)

#              # Add a success message
#             messages.success(request, "Form submitted successfully!")
#             # return render(request, "predictions/index.html", {
#             #     'form': form,
#             #     'last_uploaded_image': last_uploaded_image
#             # })
#             # Add a success message
#             messages.success(request, "Image processed successfully!")
#             return render(request, "predictions/index.html",{
#                 'last_uploaded_image': last_uploaded_image
#             })
#         elif not form.is_valid() :
#             print(form.errors)
#     else:
#         form = JujubeForm()

#     return render(request,"predictions/index.html",{
#         'form': form
#     })
        
    

    


