from djitellopy import Tello
import logging
import time

logger = logging.getLogger(__name__)

class DJIDroneAdapter:
    def __init__(self):
        self.tello = Tello()
        self.is_connected = False

    def connect(self):
        """连接无人机"""
        try:
            self.tello.connect()
            self.is_connected = True
            logger.info("成功连接大疆无人机")
            # 启动状态监控
            self.tello.streamon()
        except Exception as e:
            logger.error(f"连接失败: {str(e)}")
            raise

    def takeoff(self, height: float = 1.0):
        """起飞到指定高度（米）"""
        if not 1 <= height <= 10:
            raise ValueError("高度超出有效范围 (1-10 米)")
        
        self.tello.takeoff()
        time.sleep(1)  # 等待起飞完成
        self.tello.move_up(int(height * 100))  # 转换为厘米

    def land(self):
        """降落"""
        self.tello.land()
        logger.info("正在降落...")

    def emergency_stop(self):
        """紧急停止"""
        self.tello.emergency()
        logger.warning("已触发紧急停止")

    def get_battery_status(self):
        """获取电池状态"""
        return self.tello.get_battery()

    def disconnect(self):
        """断开连接"""
        if self.is_connected:
            self.land()
            self.tello.streamoff()
            self.tello.end()
            self.is_connected = False
            logger.info("已断开无人机连接")