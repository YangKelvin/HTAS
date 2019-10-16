import datetime
import os

# 資料夾名稱（看板名稱）
BOARD = 'MobileComm'

# 資料夾路徑
ROOT = os.getcwd()                          # 根目錄
DATA_ROOT = ROOT + '/../HTAS/Data/'            # 存放資料的目錄
ML_DATA_LAYER = DATA_ROOT + 'DataForML/'    # 訓練資料的目錄
TEST_ML_DATA_LAYER = DATA_ROOT + 'TestML/'  # 訓練資料的目錄(測試用)
DATA_LAYER = DATA_ROOT + BOARD + '/'        # 看板資料目錄

# 詞向量畫面顯示的數量
DATA_VEC_LEN = 15
