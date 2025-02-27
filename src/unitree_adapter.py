from unitree_sdk2_python.core.channel import ChannelSubscriber, ChannelPublisher, ChannelFactortyInitialize
from unitree_sdk2_python.idl.default import unitree_go_msg_dds__LowState_, unitree_go_msg_dds__LowCmd_
import time
import logging

logger = logging.getLogger(__name__)

class UnitreeRobotAdapter:
    def __init__(self):
        ChannelFactortyInitialize()
        self.subscriber = ChannelSubscriber("rt/lowstate", unitree_go_msg_dds__LowState_)
        self.publisher = ChannelPublisher("rt/lowcmd", unitree_go_msg_dds__LowCmd_)
        self.subscriber.Init()
        self.publisher.Init()
        self.is_connected = False
        self.last_state = None

    def connect(self):
        """连接机器人"""
        try:
            self._wait_for_connection()
            self.is_connected = True
            logger.info("成功连接宇树机器人")
        except Exception as e:
            logger.error(f"连接失败: {str(e)}")
            raise

    def _wait_for_connection(self, timeout=10):
        """等待机器人连接"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.subscriber.HasData():
                self.last_state = self.subscriber.Read()
                return
            time.sleep(0.1)
        raise TimeoutError("连接机器人超时")

    def move(self, velocity: float, duration: float = 1.0):
        """
        控制机器人运动
        :param velocity: 运动速度 (0-3 m/s)
        :param duration: 运动持续时间(秒)
        """
        if not 0 <= velocity <= 3:
            raise ValueError("速度超出有效范围 (0-3 m/s)")
            
        cmd = unitree_go_msg_dds__LowCmd_()
        cmd.motor_cmd[0].mode = 10  # 运动模式
        cmd.motor_cmd[0].q = velocity
        
        start_time = time.time()
        while time.time() - start_time < duration:
            self.publisher.Write(cmd)
            time.sleep(0.1)

    def get_status(self):
        """获取当前状态"""
        if self.subscriber.HasData():
            self.last_state = self.subscriber.Read()
        return self.last_state

    def emergency_stop(self):
        """紧急停止"""
        cmd = unitree_go_msg_dds__LowCmd_()
        cmd.motor_cmd[0].mode = 0  # 停止模式
        self.publisher.Write(cmd)
        logger.warning("已触发紧急停止")

    def disconnect(self):
        """断开连接"""
        self.emergency_stop()
        self.is_connected = False
        logger.info("已断开机器人连接")