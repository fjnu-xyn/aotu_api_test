import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 测试数据目录
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 测试报告目录
REPORT_DIR = os.path.join(BASE_DIR, 'reports')

# 日志目录
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 默认API基础URL
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8080')

# 测试用例YAML文件路径
TEST_CASES_FILE = os.path.join(DATA_DIR, 'test_cases.yaml')

# 确保所有目录存在
for dir_path in [DATA_DIR, REPORT_DIR, LOG_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
