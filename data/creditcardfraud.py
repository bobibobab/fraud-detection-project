import kagglehub
import shutil
import os

path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")

print("Path to dataset files:", path)

# 현재 파일 위치(data/)로 csv 복사
dest_dir = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(path, "creditcard.csv")
dest = os.path.join(dest_dir, "creditcard.csv")

shutil.copy(src, dest)
print(f"Copied to: {dest}")
