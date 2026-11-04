import os
import sys
import cv2
import shutil
import numpy as np
from sklearn.cluster import HDBSCAN

from insightface.app import FaceAnalysis


def create_embeddings(folder_path):

    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, 'models')


    app = FaceAnalysis(name="buffalo_sc", root=model_dir, providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))


    embeddings = []
    file_labels = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        image_array = cv2.imread(filepath)
        if image_array is None:
            print(f"Warning: Could not read {filename}. Skipping.")
            continue
        faces = app.get(image_array)
        for face in faces:
            embeddings.append(face.embedding)
            file_labels.append(filepath)
    print(f'type of embeddings: {type(embeddings)}')
    print(f'type of embeddings elements: {type(embeddings[0])}')
    embeddings_matrix = np.array(embeddings, dtype=np.float32)
    return embeddings_matrix, file_labels
def classify(embeddings):
    hdb = HDBSCAN(min_cluster_size=3, n_jobs=-1, copy = True, metric='cosine')
    cluster_labels = hdb.fit_predict(embeddings)
    return cluster_labels
def move_files(labels, file_labels):
    for label, file_label in zip(labels, file_labels):
        front, tail = os.path.split(file_label)
        if label == -1:
            try:
                shutil.copy2(file_label, front + "/unknown/" )
            except FileNotFoundError:
                os.makedirs(front + '/unknown/',exist_ok=True)
                shutil.copy2(file_label, front + "/unknown/")
        else:
            new_path = front + f"/person_{label}/"
            try:
                shutil.copy2(file_label, new_path)
            except FileNotFoundError:
                os.makedirs(front + f'/person_{label}/', exist_ok=True)
                shutil.copy2(file_label, new_path)
embeddings, file_labels = create_embeddings("/home/tymoteusz/Desktop/test_zdjecia")
move_files(classify(embeddings), file_labels)