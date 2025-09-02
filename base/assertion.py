from .logger import logger


class Assertion:
    @staticmethod
    def assert_equal(actual, expected, message="值不相等"):
        """断言两个值相等"""
        try:
            assert actual == expected, f"{message} - 实际值: {actual}, 期望值: {expected}"
            logger.info(f"断言成功: {actual} == {expected}")
            return True
        except AssertionError as e:
            logger.error(f"断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_not_equal(actual, expected, message="值相等"):
        """断言两个值不相等"""
        try:
            assert actual != expected, f"{message} - 实际值: {actual}, 期望值: {expected}"
            logger.info(f"断言成功: {actual} != {expected}")
            return True
        except AssertionError as e:
            logger.error(f"断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_in(actual, expected, message="实际值不在期望值中"):
        """断言实际值在期望值中"""
        try:
            assert actual in expected, f"{message} - 实际值: {actual}, 期望值: {expected}"
            logger.info(f"断言成功: {actual} 在 {expected} 中")
            return True
        except AssertionError as e:
            logger.error(f"断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_not_in(actual, expected, message="实际值在期望值中"):
        """断言实际值不在期望值中"""
        try:
            assert actual not in expected, f"{message} - 实际值: {actual}, 期望值: {expected}"
            logger.info(f"断言成功: {actual} 不在 {expected} 中")
            return True
        except AssertionError as e:
            logger.error(f"断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_status_code(response, expected_code, message="状态码不匹配"):
        """断言响应状态码"""
        try:
            assert response.status_code == expected_code, \
                f"{message} - 实际状态码: {response.status_code}, 期望状态码: {expected_code}"
            logger.info(f"状态码断言成功: {response.status_code} == {expected_code}")
            return True
        except AssertionError as e:
            logger.error(f"状态码断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_json_key_exists(response_json, key, message="JSON中不存在指定键"):
        """断言JSON响应中存在指定键"""
        try:
            assert key in response_json, f"{message} - 键: {key}"
            logger.info(f"JSON键存在断言成功: {key} 在响应中存在")
            return True
        except AssertionError as e:
            logger.error(f"JSON键存在断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_json_value(response_json, key, expected_value, message="JSON值不匹配"):
        """断言JSON响应中指定键的值"""
        try:
            # 如果期望值为空字典，则只检查键是否存在
            if expected_value == {}:
                Assertion.assert_json_key_exists(response_json, key)
                return True

            Assertion.assert_json_key_exists(response_json, key)
            actual_value = response_json[key]

            # 如果期望值是字典类型，则递归检查
            if isinstance(expected_value, dict) and isinstance(actual_value, dict):
                for k, v in expected_value.items():
                    if k in actual_value:
                        Assertion.assert_equal(actual_value[k], v, f"{message} - 键 {k}")
                    else:
                        raise AssertionError(f"{message} - 键 {k} 不存在于响应中")
            else:
                Assertion.assert_equal(actual_value, expected_value, message)
            return True
        except AssertionError as e:
            logger.error(f"JSON值断言失败: {str(e)}")
            raise
