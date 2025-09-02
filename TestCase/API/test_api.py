import pytest
import os

from config.settings import BASE_URL, DATA_DIR
from utils.yaml_utils import YamlUtils

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

    # 断言HTTP状态码
    assert_handler.assert_status_code(response, case['expected_http_code'])

    # 解析响应数据
    response_json = assert_handler.handle_json_parsing(response, case['expected_http_code'])
    if response_json is None:
        return

    # 断言响应体中的业务状态码
    if 'expected_res_code' in case:
        assert_handler.assert_response_code(response_json, case['expected_res_code'])

    # 断言响应内容
    # 遍历期望的响应内容进行断言
    if 'expected_response' in case and case['expected_response']:
        # 只有当期望响应不是空字典时才进行断言
        if case['expected_response'] != {}:
            assert_handler.assert_response_content(response_json, case['expected_response'], assert_handler)

    print(f"测试用例 {case['case_id']} 执行成功")
