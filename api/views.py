from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from OCR.settings import BASE_DIR
import cv2
import re
import pytesseract
import json;import os

''' Extract Key-value pairs from raw_text using patterns '''
def extract_key_value_pairs(raw_text, patterns):
    final_op=[]
    for item in patterns:
        for i in item:
            key_value_pairs = {}
            s=i+" (.+)"
            key_ = r"[^a-zA-Z0-9\s]+"
            key = re.sub(key_, "", i)
            key=key.rstrip('w');key=key.rstrip('ws')
            match = re.search(s, raw_text)
            if match:
                value = match.group(1)
                if key=="Amount":
                    value = re.sub(r"\D", "", value)
                key_value_pairs[key] = value
                final_op.append(key_value_pairs)
    return final_op

patterns=[
[r"Invoice No:  (\w+)",r"Invoice:  (\w+)",r"invoice No: (\w+)",r"Invoice No (\w+)"],
[r"Invoice Date: ([\w\s]+)",r"invoice date: ([\w\s]+)",r"lavoice Date",r"Inv Date:"],
[r"Country of Origin (\w+)"],[r"Country of Final"],
[r"GSTIN:",r"GSTIN : (\w+)"],
[r"Due Date:",r"Due Date"],
[r"Challan No (\w+)"],[r"Challan Date"],[r"Bank Account Number"],
[r"Transport Mode:",r"Transport Mode"],
[r"Place of Supply:",r"Place of Supply"],
[r"Date of Supply:",r"Date of Supply"],
[r"Bank Swift Code"],
[r"Ship Bill no: (\w+)"],[r"Ship Bill date"],[r"Ship Port code"],
[r"Amount:",r"Amount",r"Amount after Tax:",r"Amount before Tax"]
]

'''Create Json file for Output response'''
def output_json(data):
    file_path = str(BASE_DIR)+"/Output/result.json"
    with open(file_path, "w") as file:
        json.dump(data, file)


class OCR_Extraction(APIView):
    def post(self,request):
        try:
            for item in request.FILES.getlist('ImagePath'):
                FileName = item.name
                with open(str(BASE_DIR)+"/Input/"+FileName, 'wb+') as destination:
                        destination.write(item.read())
            image_path=str(BASE_DIR)+"/Input/"+FileName
            pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
            box_ = pytesseract.image_to_data(image_path, output_type=pytesseract.Output.DICT)
            raw_text_ = pytesseract.image_to_string(image_path)
            clean_pattern = r"[^a-zA-Z0-9\s:/-]+"
            raw_text = re.sub(clean_pattern, "", raw_text_)
            #print(raw_text, 'clean Text-------------')
            result= extract_key_value_pairs(raw_text, patterns)
            res={"Satus":True,"FileName":FileName,"Data":result}
            output_json(result)
            print('Output Json file Generated--')
            return Response(res, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            res={"Satus":False,"msg":"Internal server error"}
            return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)
