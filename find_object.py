import torch
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
img_path = 'my_image/1.png'
results = model(img_path)
df = results.pandas().xyxy[0]
microwaves = df[df['name'] == 'microwave']

img = cv2.imread(img_path)
for _, row in microwaves.iterrows():
    x1, y1, x2, y2 = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
    cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
    cv2.putText(img, 'microwave', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

cv2.imwrite('microwave_detected.jpg', img)
print('microwave_detected.png로 저장 완료!')