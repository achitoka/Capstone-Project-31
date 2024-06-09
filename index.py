import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import os

# Fungsi untuk memuat model Keras (.h5)
@st.cache_resource
def load_keras_model(model_path):
    model = load_model(model_path)
    return model

# Fungsi untuk memproses dan memprediksi gambar
def predict_image(image, model):
    # Mengubah ukuran gambar sesuai kebutuhan model (misalnya 224x224)
    img = cv2.resize(image, (224, 224))
    # Mengubah gambar menjadi array numpy
    img_array = np.array(img)
    # Menambahkan dimensi batch
    img_array = np.expand_dims(img_array, axis=0)
    # Melakukan normalisasi jika diperlukan
    img_array = img_array / 255.0
    # Melakukan prediksi
    predictions = model.predict(img_array)
    return predictions

# Fungsi untuk memetakan prediksi ke label kelas asli
def get_class_label(predictions):
    class_labels = ['Ripe', 'Unripe', 'Damaged', 'Old']
    class_index = np.argmax(predictions, axis=1)
    return [class_labels[index] for index in class_index]

# Fungsi untuk memberikan deskripsi dari setiap kelas prediksi
def get_prediction_description(class_label):
    descriptions = {
        'Ripe': 'Tomat dalam kondisi matang dan siap untuk dikonsumsi.',
        'Unripe': 'Tomat masih mentah dan belum siap untuk dikonsumsi.',
        'Damaged': 'Tomat mengalami kerusakan dan tidak layak untuk dikonsumsi.',
        'Old': 'Tomat sudah tua dan mungkin tidak segar lagi.'
    }
    return descriptions.get(class_label, 'Deskripsi tidak tersedia.')

# Membuat folder saved_images jika belum ada
if not os.path.exists('saved_images'):
    os.makedirs('saved_images')

# Memuat model Keras (.h5)
model = load_keras_model("finalModel_31.h5")

# Definisi halaman
def homepage():
    st.header("Selamat Datang di TomatVision App")
    st.write("Solusi Real-time untuk memastikan kualitas tomat. Aplikasi ini dirancang untuk memindai dan mengklasifikasi tomat.")
    st.image("welcome.png", use_column_width=True)

# Fungsi untuk menyimpan gambar dengan metadata pemilik
def save_image_with_metadata(image, user_id, filename):
    img_save_path = f'saved_images/{user_id}_{filename}'
    image.save(img_save_path)

# Fungsi untuk memuat daftar gambar yang dimiliki oleh pengguna saat ini
def get_user_images(user_id):
    user_images = []
    image_files = os.listdir('saved_images')
    for img_file in image_files:
        if img_file.startswith(f"{user_id}_"):
            user_images.append(img_file)
    return user_images

# Halaman untuk melakukan pemindaian kamera
def camera_scan_page():
    st.header("Pemindaian Kamera")

    # Menjalankan kamera
    run = st.checkbox('Jalankan Kamera')

    # Placeholder untuk frame video
    stframe = st.empty()

    if run:
        cap = cv2.VideoCapture(0)
        previous_frame = None
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("Gagal mendapatkan frame dari kamera.")
                break

            # Deteksi perubahan dalam frame untuk menentukan kehadiran objek
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if previous_frame is not None:
                diff_frame = cv2.absdiff(previous_frame, gray_frame)
                _, thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)
                non_zero_count = np.count_nonzero(thresh_frame)

                if non_zero_count > 10000:  # Mengubah nilai ini sesuai kebutuhan
                    # Melakukan prediksi pada frame saat ini
                    predictions = predict_image(frame, model)
                    class_label = get_class_label(predictions)[0]

                    # Menggambar bingkai hijau jika prediksi adalah 'Ripe'
                    if class_label == 'Ripe':
                        # Menggambar bingkai hijau di sekitar gambar (margin 10 piksel)
                        start_point = (10, 10)
                        end_point = (frame.shape[1] - 10, frame.shape[0] - 10)
                        color = (0, 255, 0)  # Warna hijau dalam BGR
                        thickness = 3  # Ketebalan bingkai
                        frame = cv2.rectangle(frame, start_point, end_point, color, thickness)

                    # Menampilkan hasil prediksi pada frame
                    cv2.putText(frame, f"Prediction: {class_label}", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # Menyimpan frame saat ini sebagai previous_frame
            previous_frame = gray_frame

            # Menampilkan frame di Streamlit
            stframe.image(frame, channels="BGR")

            # Menyimpan frame ke dalam folder saved_images
            frame_filename = f'frame_{int(cap.get(cv2.CAP_PROP_POS_FRAMES))}.jpg'
            save_image_with_metadata(Image.fromarray(frame), st.session_state.get("username"), frame_filename)

        cap.release()
    else:
        st.write("Nyalakan kamera untuk memulai klasifikasi.")

    # Upload gambar
    uploaded_file = st.file_uploader("Unggah Gambar Tomat", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Gambar Tomat yang Diunggah', use_column_width=True)

        # Konversi gambar ke array numpy
        img_array = np.array(image)

        # Melakukan prediksi pada gambar yang diunggah
        predictions = predict_image(img_array, model)
        class_label = get_class_label(predictions)[0]

        st.write(f"Prediction: {class_label}")

        # Menyimpan gambar yang diunggah ke dalam folder saved_images
        save_image_with_metadata(image, st.session_state.get("username"), uploaded_file.name)

# Halaman untuk menampilkan galeri gambar
def gallery_and_details_page():
    st.header("Galeri Foto & Rincian")

    # Menampilkan gambar dalam grid
    image_files = get_user_images(st.session_state.get("username"))
    cols = st.columns(4)  # Menampilkan gambar dalam grid 4 kolom
    
    for i, img_file in enumerate(image_files):
        img_path = os.path.join('saved_images', img_file)
        
        with cols[i % 4]:
            with open(img_path, "rb") as file:
                image = Image.open(file)
                st.image(image, caption=img_file, width=200, use_column_width=True)
                
                if st.button(f"Detail gambar", key=img_file):
                    st.image(image, caption=img_file, width=150)
                    
                    # Konversi gambar ke array numpy
                    img_array = np.array(image)

                    # Melakukan prediksi pada gambar yang dipilih
                    predictions = predict_image(img_array, model)
                    class_label = get_class_label(predictions)[0]
                    description = get_prediction_description(class_label)

                    st.write(f"Prediction: {class_label}")
                    st.write(f"Deskripsi: {description}")
                    st.write(f"Nama File: {img_file}")

                    if st.button("Tutup Detail", key=f"tutup_detail_{img_file}"):
                        image.close()

            # Tombol untuk menghapus gambar
            if st.button(f"Hapus gambar", key=f"hapus_{img_file}"):
                os.remove(img_path)
                st.experimental_rerun()
