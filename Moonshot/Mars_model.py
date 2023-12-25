from ultralytics import YOLO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

model_mars = YOLO(str(Path(BASE_DIR,'best.pt')))
model_moon = YOLO(str(Path(BASE_DIR,'moon_model.pt')))
#model.predict(source = 'images',hide_labels = True,line_thickness = 2,save = True,save_txt = True)
