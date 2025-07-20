import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import os

IMG_PATH = "result/exp/room.jpg"
LABEL_PATH = "result/exp/labels/room.txt"

def load_labels(label_path, img_width, img_height):
    boxes = []
    if not os.path.exists(label_path):
        return boxes
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5:
                # YOLO format: class x_center y_center width height (normalized)
                _, x, y, w, h = map(float, parts[:5])
                # 좌표 변환 (normalized → 실제 픽셀)
                x1 = int((x - w/2) * img_width)
                y1 = int((y - h/2) * img_height)
                x2 = int((x + w/2) * img_width)
                y2 = int((y + h/2) * img_height)
                boxes.append((x1, y1, x2, y2))
    return boxes

def main():
    if "page" not in st.session_state:
        st.session_state.page = "main"

    if st.session_state.page == "main":
        st.title("객체 클릭 데모")
        image = Image.open(IMG_PATH)
        img_width, img_height = image.size
        boxes = load_labels(LABEL_PATH, img_width, img_height)

        # Draw rectangles for visualization
        draw = ImageDraw.Draw(image)
        for box in boxes:
            draw.rectangle(box, outline="red", width=3)

        st.image(image, caption="room.jpg", use_column_width=True)

        # 클릭 좌표 받기
        click = st.image(image, caption="객체를 클릭하세요", use_column_width=True, output_format="PNG")
        coords = st.query_params.get("coords", None)  # 변경됨

        # Streamlit의 native 이미지 클릭 이벤트가 없으므로, st.image 위에 투명 버튼을 박스마다 올려서 클릭 감지
        for idx, (x1, y1, x2, y2) in enumerate(boxes):
            # 버튼 위치 계산 (Streamlit은 절대좌표 지원X, workaround: 버튼 여러개)
            if st.button(f"Box {idx+1} 클릭", key=f"box_{idx}"):
                st.session_state.page = "next"
                st.rerun()  # 변경됨

        st.write("※ 실제 클릭 이벤트는 Streamlit에서 이미지 좌표로 직접 받기 어렵기 때문에, 위 버튼을 대신 사용합니다.")

    elif st.session_state.page == "next":
        st.title("다음페이지")
        st.write("다음페이지")

if __name__ == "__main__":
    main()