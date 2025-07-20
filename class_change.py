import os

def change_class_to_new(input_dir, output_dir, new_class):
    # 출력 폴더가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            with open(input_path, "r") as file:
                lines = file.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 5 and parts[0] == '0':
                    parts[0] = new_class
                new_lines.append(" ".join(parts) + "\n")

            with open(output_path, "w") as file:
                file.writelines(new_lines)

    print(f"✅ class 0 → {new_class}로 변경된 파일이 '{output_dir}/'에 저장되었습니다.")

if __name__ == "__main__":
    input_folder = input_folder = './unprocessed_data/powerstrip.yolov5pytorch/valid/labels'
    new_class_id = input("변경할 클래스 ID를 입력하세요 (예: 1, 2, ...): ").strip()
    
    if not new_class_id.isdigit():
        print("❌ 숫자만 입력하세요.")
    else:
        output_folder = f"./class{new_class_id}_data"
        change_class_to_new(input_folder, output_folder, new_class_id)
