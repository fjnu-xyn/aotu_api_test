import yaml
import os
import re
from base.logger import logger
from utils.DataGenerator import DataGenerator


class YamlUtils:
    @staticmethod
    def read_yaml(file_path):
        """
        读取YAML文件内容并返回字典
        :param file_path: YAML文件的绝对路径
        :return: 解析后的字典数据
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"YAML文件不存在: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # 使用safe_load避免安全风险（不加载自定义对象）
                data = yaml.safe_load(f)
                return data
        except yaml.YAMLError as e:
            raise ValueError(f"YAML文件解析错误: {str(e)}")
        except Exception as e:
            raise Exception(f"读取YAML文件失败: {str(e)}")

    @staticmethod
    def process_dynamic_data(data):
        """
        处理动态数据生成（在每次调用时生成新的随机数据）
        :param data: 原始数据
        :return: 处理后的数据
        """
        if isinstance(data, dict):
            return {key: YamlUtils.process_dynamic_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [YamlUtils.process_dynamic_data(item) for item in data]
        elif isinstance(data, str):
            return YamlUtils._generate_dynamic_value(data)
        else:
            return data

    @staticmethod
    def _generate_dynamic_value(value):
        """
        根据占位符生成动态值
        :param value: 包含占位符的字符串
        :return: 生成的动态值或原始值
        """
        if not isinstance(value, str):
            return value

        # 匹配 {{function:param}} 或 {{function}} 格式的占位符
        pattern = r'\{\{([^}:]+)(?::([^}]+))?\}\}'
        match = re.search(pattern, value)

        if not match:
            return value

        func_name = match.group(1)
        param = match.group(2)

        # 根据函数名生成对应的数据
        try:
            if func_name == "generate_username":
                result = DataGenerator.generate_username(param or "user")
            elif func_name == "generate_email":
                result = DataGenerator.generate_email(param)
            elif func_name == "generate_phone":
                result = DataGenerator.generate_phone()
            elif func_name == "generate_password":
                result = DataGenerator.generate_password()
            elif func_name == "current_datetime":
                result = DataGenerator.generate_datetime()
            elif func_name == "generate_age":
                age = int(param) if param else 25
                result = DataGenerator.generate_age(age, age)
            else:
                result = value

            # 如果整个字符串就是一个占位符，则直接返回生成的值
            if match.group(0) == value:
                return result
            else:
                # 如果字符串中包含占位符，则替换占位符
                return value.replace(match.group(0), str(result))
        except Exception as e:
            logger.warning(f"动态数据生成失败: {value}, 错误: {str(e)}")
            return value

    @staticmethod
    def write_yaml(file_path, data):
        """写入数据到YAML文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
        except Exception as e:
            logger.error(f"写入YAML文件失败: {str(e)}")
            raise
