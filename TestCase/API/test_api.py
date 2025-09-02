import pytest
import os
import re

from config.settings import BASE_URL, DATA_DIR
from utils.yaml_utils import YamlUtils
from utils.DataGenerator import DataGenerator

# 读取YAML测试数据
test_data_raw = YamlUtils.read_yaml(os.path.join(DATA_DIR, "test_cases.yaml"))


@pytest.mark.api
@pytest.mark.parametrize("case_raw", test_data_raw)
def test_create_user(case_raw):
    """测试用户创建接口"""
    # 每次测试都处理动态数据
    case = YamlUtils.process_dynamic_data(case_raw)

    # 初始化请求处理器和断言处理器
    from base.request import RequestBase
    from base.assertion import Assertion

    req_handler = RequestBase()
    assert_handler = Assertion()

    # 拼接完整URL
    full_url = f"{BASE_URL}{case['url']}"

    # 打印测试用例信息
    print(f"\n执行测试用例 {case['case_id']}: {case['description']}")
    print(f"请求URL: {full_url}")
    print(f"请求数据: {case['request_data']}")

    # 发送请求
    response = req_handler._send_request(
        method=case['method'],
        url=full_url,
        headers=case['headers'],
        json=case['request_data']  # 使用json参数自动处理Content-Type
    )

    # 打印响应状态码和内容，便于调试
    print(f"响应状态码: {response.status_code}")
    try:
        response_json = response.json()
        print(f"响应内容: {response_json}")
    except Exception:
        print(f"响应内容(非JSON): {response.text}")

    # 断言状态码
    assert_handler.assert_status_code(response, case['expected_code'])

    # 解析响应数据
    try:
        response_json = response.json()
    except Exception as e:
        # 如果期望状态码不是2xx，且无法解析JSON，则可能是服务器错误
        if case['expected_code'] < 200 or case['expected_code'] >= 300:
            print(f"警告: 状态码 {response.status_code} 的响应不是有效的JSON格式")
            return
        else:
            pytest.fail(f"响应解析JSON失败: {str(e)}")

    # 断言响应内容
    # 遍历期望的响应内容进行断言
    if 'expected_response' in case and case['expected_response']:
        # 只有当期望响应不是空字典时才进行断言
        if case['expected_response'] != {}:
            _assert_response_content(response_json, case['expected_response'], case['request_data'], assert_handler)

    print(f"测试用例 {case['case_id']} 执行成功")


def _assert_response_content(response_json, expected_response, request_data, assert_handler):
    """
    递归断言响应内容
    :param response_json: 实际响应JSON
    :param expected_response: 期望响应内容
    :param request_data: 请求数据，用于匹配动态值
    :param assert_handler: 断言处理器
    """
    for key, expected_value in expected_response.items():
        # 处理嵌套字典的情况
        if isinstance(expected_value, dict):
            # 确保键存在且值是字典
            assert_handler.assert_json_key_exists(response_json, key)
            actual_value = response_json[key]
            if isinstance(actual_value, dict):
                # 递归处理嵌套字典
                _assert_response_content(actual_value, expected_value, request_data, assert_handler)
            else:
                pytest.fail(f"期望键 {key} 的值是字典，但实际值是 {type(actual_value)}: {actual_value}")
        else:
            # 处理普通键值对
            assert_handler.assert_json_value(response_json, key, expected_value)
