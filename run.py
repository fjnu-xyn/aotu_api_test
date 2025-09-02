import os
import pytest
from datetime import datetime
from config.settings import REPORT_DIR


def run_tests():
    """执行测试并生成报告"""
    # 生成报告文件名
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    report_file = os.path.join(REPORT_DIR, f'report_{now}.html')

    # 构建pytest命令
    pytest_args = [
        'TestCase/',
        '--html=' + report_file,
        '--self-contained-html',
        '-v'
    ]

    # 执行测试
    print(f"开始执行测试，报告将保存至: {report_file}")
    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        print(f"测试执行成功！报告已生成: {report_file}")
    else:
        print(f"测试执行完成，存在失败用例。报告已生成: {report_file}")

    return exit_code


if __name__ == "__main__":
    run_tests()
