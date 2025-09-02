import random
import string
from datetime import datetime


class DataGenerator:
    """
    数据生成工具类，用于生成各种测试数据
    """

    @staticmethod
    def generate_username(prefix="user", length=8):
        """
        生成随机用户名
        :param prefix: 用户名前缀
        :param length: 随机部分长度
        :return: 生成的用户名
        """
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        return f"{prefix}_{random_str}"

    @staticmethod
    def generate_email(username=None, domain="example.com"):
        """
        生成随机邮箱地址
        :param username: 用户名，如果为空则自动生成
        :param domain: 邮箱域名
        :return: 生成的邮箱地址
        """
        if not username:
            username = DataGenerator.generate_username(length=6)
        # 如果提供了username参数但不是固定值，则生成随机用户名
        elif username == "admin":
            username = DataGenerator.generate_username(prefix="admin", length=6)
        return f"{username}@{domain}"

    @staticmethod
    def generate_phone():
        """
        生成随机手机号码
        :return: 生成的手机号码
        """
        prefix = random.choice(['13', '15', '17', '18', '19'])
        suffix = ''.join(random.choices(string.digits, k=9))
        return f"{prefix}{suffix}"

    @staticmethod
    def generate_password(length=10):
        """
        生成随机密码
        :param length: 密码长度
        :return: 生成的密码
        """
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=length))

    @staticmethod
    def generate_datetime():
        """
        生成当前日期时间字符串
        :return: 格式化的日期时间字符串
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def generate_age(min_age=18, max_age=80):
        """
        生成随机年龄
        :param min_age: 最小年龄
        :param max_age: 最大年龄
        :return: 生成的年龄
        """
        return random.randint(min_age, max_age)


if __name__ == "__main__":
    # 演示如何调用generate_phone()方法
    print("生成的随机手机号码:", DataGenerator.generate_phone())

    # 演示其他方法的调用
    print("生成的随机用户名:", DataGenerator.generate_username())
    print("生成的随机邮箱:", DataGenerator.generate_email())
    print("生成的随机密码:", DataGenerator.generate_password())
    print("生成的当前时间:", DataGenerator.generate_datetime())
    print("生成的随机年龄:", DataGenerator.generate_age())