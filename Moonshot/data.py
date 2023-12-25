import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os
import shutil
import cv2
from cv2 import dnn_superres


class Data_processing():
     def __init__(self,directory_images,directory_labels):
         self.directory_images = directory_images
         self.directory_labels = directory_labels
         self.images_names_with_directory = []
         self.images_names = []
         self.labels_names = []
         self.labels_names_csv = []
         self.labels_names_txt = []

     def image_upscaling(self,image):
         """

         :param image: image to be upscaled by a factor of 2
         :return: upscaled image by a factor of 2
         """
         sr = dnn_superres.DnnSuperResImpl_create()
         path = "LapSRN_x2.pb"
         sr.readModel(path)
         sr.setModel("lapsrn", 2)
         upscaled_image = sr.upsample(image)
         return upscaled_image

     def padding_image(self,image, windowSize):
         """

         :param image: image to be padded (numpy array)
         :param windowSize: the total size of the output with padding (tuple)
         :return: padded image as a numpy array and the coordinates of the top left corner of the image
         that was padded (float values)
         """
         mask = np.zeros((windowSize[0], windowSize[1], 3), dtype="uint8")
         ii = np.random.randint(0, windowSize[0] - image.shape[0])
         jj = np.random.randint(0, windowSize[1] - image.shape[1])
         mask[ii:ii + image.shape[0], jj:jj + image.shape[1], :] = image
         return mask, ii, jj

     def coordinate_transformation(self,label, scale, C_x, C_y, W, H):
         """

         :param label: center x, center y, box width, box height in the original image (int)
         :param scale: scale factor by which the image was shrunk (float)
         :param C_x: x of the top left corner of the image in the padded output(int)
         :param C_y: y of the top left corner of the image in the padded output (int)
         :param W: width of the padded image (int)
         :param H: height of the padded image(int)
         :return: label: center x, center y, box width, box height in the padded image
         """
         return (scale * label[:, 0] + C_y / W), (scale * label[:, 1] + C_x / H), \
                0.5*scale * label[:, 2], 0.5*scale * label[:,3]

     def image_label_augmentation(self,image, label):
         """

         :param image: original image (numpy array)
         :param label: orginal label (numpy array)
         :return: upscaled image, padded image (numpy array), label in the padded image (numpy array)
         """
         new_image = self.image_upscaling(image)
         padded_image, x, y = self.padding_image(image, (832, 832))
         new_label = self.coordinate_transformation(label, 0.5, x, y, 832, 832)
         return new_image, padded_image, new_label

     def create_lists(self,type, fill_images_list):
         """

         :param type: save labels as .csv or .txt format
         :param fill_images_list: whether or not to append image paths to the list
         :return: creates lists containing paths to each image.
         """
         for filename in os.listdir(self.directory_images):
             if filename == ".DS_Store":
                 pass
             else:
                 name = filename.split('.')[0]
                 label_name = [name, type]
                 label_name_ext = '.'.join(label_name)
                 if type == "csv":
                     foldered_labeled_name = [self.directory_labels, label_name_ext]
                     self.labels_names.append(name)
                 else:
                     foldered_labeled_name = ['text_labels', label_name_ext]
                 foldered_labeled_name_ext = '/'.join(foldered_labeled_name)
                 f = os.path.join(self.directory_images, filename)
                 if os.path.isfile(f):
                     if fill_images_list:
                         self.images_names_with_directory.append(f)
                         self.images_names.append(filename)
                     else:
                         pass
                     if type == "csv":
                         self.labels_names_csv.append(foldered_labeled_name_ext)
                     else:
                         self.labels_names_txt.append(foldered_labeled_name_ext)


     def convert_to_txt(self):
         """

         :return: converts labels from .csv to .txt
         """
         try:
             os.mkdir('../text_labels')
         except FileExistsError:
             shutil.rmtree('../text_labels')
             os.mkdir('../text_labels')
         root = '../text_labels'
         for index, label_name in enumerate(self.labels_names_csv):
             label = pd.read_csv(label_name, header=None)
             df = pd.DataFrame(np.zeros((label.shape[0], 1), dtype=int))
             output = pd.concat([df, label], axis=1)
             new_name = [self.labels_names[index], 'txt']
             filename = '.'.join(new_name)
             output.to_csv(root + '/' + filename, header=None, index=False, sep=' ')

     def creating_augmented_folders(self):
         """

         :return:creates folders containing augmented data
         """
         try:
             os.mkdir('../augmented_images')
         except FileExistsError:
             pass
         try:
             os.mkdir('../augmented_labels')
         except FileExistsError:
             pass
         for filename in os.listdir(self.directory_images):
             f = os.path.join(self.directory_images, filename)
             image = cv2.imread(f)
             name = filename.split('.')[0]
             label_name = [name,'csv']
             label_name_csv = '.'.join(label_name)
             label = pd.read_csv(os.path.join(self.directory_labels, label_name_csv), sep=',', header=None, index_col=None)
             label_array = label.to_numpy()
             new_image, padded_image, new_label = self.image_label_augmentation(image, label_array)
             new_label = np.transpose(new_label)
             new_label = pd.DataFrame(new_label)
             cv2.imwrite('../augmented_images'+'/'+ filename,new_image)
             label.to_csv('../augmented_labels'+ '/' + label_name_csv,header = None,index = False)
             cv2.imwrite('../augmented_images'+ '/'+ 'modified_' + filename,padded_image)
             new_label.to_csv('../augmented_labels'+ '/' + 'modified_'+ label_name_csv,header = None,index = False)
         self.directory_images = '../augmented_images'
         self.directory_labels = '../augmented_labels'




     def split(self,train, val):
         """

         :param train: training set size, float between 0 and 1
         :param val: validation size, between 0 and 1. train and val have to add up to less than 1
         :return: training, validation and test sets (numpy arrays)
         """
         train_images, remaining_images, train_labels, remaining_labels = train_test_split(self.images_names_with_directory,
                                                                                           self.labels_names_txt,
                                                                                           train_size=train,
                                                                                           shuffle=True)
         val_images, test_images, val_labels, test_labels = train_test_split(remaining_images, remaining_labels,
                                                                             train_size=val / (1 - train),
                                                                             shuffle=True)
         return train_images, train_labels, val_images, val_labels, test_images, test_labels

     def splits_folders(self,folder, set, list,labels):
         try:
             os.mkdir(folder)
         except FileExistsError:
             pass
         try:
             os.mkdir(folder + '/' + set)
             root = folder + '/' + set
             for item in list:
                 if not labels:
                    name = item.split('/')[2]
                    shutil.move(item, root + '/' + name)
                 else:
                     name = item.split('/')[1]
                     shutil.move('../' + item, root + '/' + name)
         except FileExistsError:
             pass

     def data_for_yolo(self,train, val,augmentation):
         """
            :param train: training set size, float between 0 and 1
            :param val: validation size, between 0 and 1. train and val have to add up to less than 1
            :return: training, validation and test sets (numpy arrays)
                  """
         if len(os.listdir(self.directory_images)) != 0 and len(os.listdir(self.directory_labels)) != 0:
             if augmentation:
                self.creating_augmented_folders()
             self.create_lists("csv", True)
             self.convert_to_txt()
             self.create_lists("txt", False)
             train_images, train_labels, val_images, val_labels, test_images, test_labels = self.split(train, val)
             self.splits_folders('../images', 'training', train_images,False)
             self.splits_folders('../images', 'validation', val_images,False)
             self.splits_folders('../images', 'test', test_images,False)
             self.splits_folders('../labels', 'training', train_labels,True)
             self.splits_folders('../labels', 'validation', val_labels,True)
             self.splits_folders('../labels', 'test', test_labels,True)
         else:
            pass











