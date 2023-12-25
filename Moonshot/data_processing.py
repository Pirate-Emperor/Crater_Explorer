from data import Data_processing
#import moon_processing
import os
import shutil
import Mars_model
import pandas as pd
from data_finder import clean_directory,transfer_files
def main_processing(path, output_directory, model):
    try:
        shutil.copytree(path + '/images', os.getcwd()+'/images')
    except FileExistsError:
        shutil.rmtree(os.getcwd()+'/images')
        shutil.copytree(path + '/images', os.getcwd() + '/images')
    if os.path.exists('static/prediction_original_images'):
        shutil.rmtree('static/prediction_original_images')
    shutil.copytree(path + '/images', 'static/prediction_original_images')
    if 'labels' in os.listdir(path):
        try:
            shutil.copytree(path + '/labels', os.getcwd() + '/labels')
        except FileExistsError:
            shutil.rmtree(os.getcwd() + '/labels')
            shutil.copytree(path + '/labels', os.getcwd() + '/labels')
        processor = Data_processing('images','labels')
        processor.convert_to_txt()
    if os.path.exists('runs'):
        shutil.rmtree('runs')
    model.predict(source='images', hide_labels=True, line_thickness=2, save=True, save_txt=True)
    try:
        os.mkdir(output_directory + '/images')
    except FileExistsError:
        shutil.rmtree(output_directory + '/images')
        os.mkdir(output_directory + '/images')
    try:
        os.mkdir(output_directory + '/detections')
    except FileExistsError:
        shutil.rmtree(output_directory + '/detections')
        os.mkdir(output_directory + '/detections')
    for item in os.listdir('runs/detect/predict'):
        if item != 'labels':
            name = item.split('.')[0]
            label = [name,'txt']
            label_name = '.'.join(label)
            if label_name in os.listdir('runs/detect/predict/labels'):
                shutil.copy('runs/detect/predict/'+item, output_directory + '/images')
                shutil.copy('runs/detect/predict/'+item, 'static/prediction_old_names')
            for item in os.listdir('runs/detect/predict/'+ 'labels'):
                name = item.split('.')[0]
                label = [name, 'csv']
                label_name = '.'.join(label)
                read_file = pd.read_csv('runs/detect/predict/'+'labels'+'/'+item)
                read_file_2 = pd.read_csv('runs/detect/predict/'+'labels'+'/'+item)
                read_file.to_csv(output_directory+'/detections/'+label_name)
                read_file_2.to_csv('static/prediction_original_labels')
    clean_directory()
    return transfer_files()

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

main_processing(str(Path(BASE_DIR, 'test_folder')), str(Path(BASE_DIR, 'output_folder')), Mars_model.model_mars)







