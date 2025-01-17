STEPS TO FOLLOW.

1. Download zip file and Extract in your system.

2. cd OCR/

3. Create the virtualenv
! pip install virtualenv
! virtualenv env_name
! env_name\Scripts\activate   # to activate virtualenv

4. Install all the required packages
! pip install -r requirements.txt

5. Start the python server using following command
!python manage.py runserver

6. Use postman collection to trigger the request and get the result.
http://localhost:8000/api/v1/OCRExtraction
! POST req and select file
