import os
import shutil

# static/predicted_old_names - Annoted images
# static/prediction_original_images - Original images
# static/prediction_original_labels

original_path = 'static/prediction_original_images/'
predicted_path = 'static/prediction_old_names/'
labels_path =  'static/prediction_original_labels/'

final_image_path = 'static/prediction'
final_labels_path = 'static/csvs'

def clean_directory():
    #Clean existing files from prediction
    final_image_files = os.listdir(final_image_path)
    shutil.rmtree(final_image_path)
    os.makedirs(final_image_path)

    if len(final_image_files) != 0:
        for file in final_image_files:
            if '.png' in file or '.tif' in file or '.jpeg' in file or '.jpg' in file:
                try:
                    os.remove(final_image_path+file)
                except FileNotFoundError:
                    print("file not found")

def transfer_files():
#Transfer from prediction_original to prediction 
    if os.path.exists(original_path):
        original_files = os.listdir(original_path)
        for file in original_files:
            if '.png' in file or '.tif' in file or '.jpeg' in file or '.jpg' in file:
                shutil.move(src=original_path+file, dst=final_image_path)
    else: 
        print("Input path does not exists")

    #Transfer predicted files
    if os.path.exists(predicted_path):
        pred_files = os.listdir(predicted_path)
        for file in pred_files:
            try:
                if '.png' in file:
                    file = file.replace(".png", "_Y.png")
                    os.rename(src=predicted_path+file, dst=final_image_path)
                elif '.tif' in file:
                    file = file.replace(".tif", "_Y.tif")
                    os.rename(src=predicted_path+file, dst=final_image_path)
                elif '.jpeg' in file:
                    file = file.replace(".jpeg", "_Y.jpeg")
                    os.rename(src=predicted_path+file, dst=final_image_path)
                elif '.jpg' in file:
                    file = file.replace(".jpg", "_Y.jpg")
                    os.rename(src=predicted_path+file, dst=final_image_path)
            except:
                pass

    if os.path.exists(labels_path):
        labels_files = os.listdir(labels_path)
        for file in labels_files:
            if '.csv' in file:
                os.rename(src=labels_path+file, dst=final_labels_path)
    shutil.rmtree(original_path)
    # os.remove(predicted_path)
    # os.remove(labels_path)
    return [os.listdir(final_image_path),os.listdir(final_labels_path)]

    




        


        

