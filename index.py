import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import os

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
model = load_model("finalModel_31.h5")

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

    # Mengambil gambar dari webcam
    picture = st.camera_input("Nyalakan kamera untuk memulai klasifikasi.")

    if picture:
        # Membaca gambar
        img = Image.open(picture)
        st.image(img, caption='Gambar dari Kamera', use_column_width=True)

        # Konversi gambar ke array numpy
        img_array = np.array(img)

        # Melakukan prediksi pada gambar yang diambil
        predictions = predict_image(img_array, model)
        class_label = get_class_label(predictions)[0]

        st.write(f"Prediction: {class_label}")
    
        # Menyimpan gambar ke dalam folder saved_images
        save_image_with_metadata(img, st.session_state.get("username"), 'frame.jpg')

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
