TomatVision App ver 1.0 
********************************
How to Launch
1. Import database 'dbtomat.sql'
   - Open db.py, adjust your database username and password
Open terminal :
2. Install bcrypt            -> pip install bcrypt streamlit
3. Install mysql connector   -> pip install mysql-connector-python
4. Install tensorFlow        -> pip install streamlit tensorflow pillow
5. Install opencv            -> pip install streamlit opencv-python tensorflow pillow
6. Run your xampp/wampp/lampp/db 
7. Start the app             -> streamlit run main.py
===========================================================================================

How to Use
1. Log in using your username and password. If you don't have an account, sign up first
2. Input the captcha
3. After entering the homepage, you can scan the camera or upload image of tomatoes directly to the navigation select 'Camera scan'
4. Checklist the 'Nyalakan kamera untuk scan' / Click 'upload files'
5. Wait until the prediction result is displayed
6. You can view scan and upload history by select "Gallery & Photo Details" from navigation sidebar
7. Click 'detail gambar' to see the image prediction details
8. Click 'hapus gambar' to delete the image
