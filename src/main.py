from modelcontextprotocol import Server, StdioServerTransport
from modelcontextprotocol.sdk.types import *
import logging
from unitree_adapter import UnitreeRobotAdapter
from dji_adapter import DJIDroneAdapter
import asyncio

# 初始化日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RobotMCPServer:
    def __init__(self):
        self.unitree = UnitreeRobotAdapter()
        self.dji = DJIDroneAdapter()
        self.server = Server(
            name="robot-mcp-server",
            version="0.1.0",
            capabilities={
                "tools": self._register_tools(),
                "resources": {}
            }
        )
        self._setup_exception_handling()

    def _register_tools(self):
        return {
            "unitree_connect": {
                "description": "连接宇树机器人",
                "input_schema": {"type": "object"}
            },
            "unitree_move": {
                "description": "控制宇树机器人运动",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "velocity": {"type": "number", "minimum": 0, "maximum": 3},
                        "duration": {"type": "number", "minimum": 0.1, "default": 1.0}
                    },
                    "required": ["velocity"]
                }
            },
            "unitree_stop": {
                "description": "紧急停止宇树机器人",
                "input_schema": {"type": "object"}
            },
            "dji_connect": {
                "description": "连接大疆无人机",
                "input_schema": {"type": "object"}
            },
            "dji_takeoff": {
                "description": "大疆无人机起飞",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "height": {"type": "number", "minimum": 1, "maximum": 10, "default": 1.0}
                    }
                }
            },
            "dji_land": {
                "description": "大疆无人机降落",
                "input_schema": {"type": "object"}
            }
        }

    def _setup_exception_handling(self):
        async def error_handler(ctx, error):
            logger.error(f"工具调用错误: {str(error)}")
            return {"error": str(error)}

        self.server.on_tool_error = error_handler

    async def _execute_tool(self, name, arguments):
        try:
            logger.info(f"执行工具 {name}，参数: {arguments}")
            if name == "unitree_connect":
                self.unitree.connect()
                return {"status": "connected"}
            elif name == "unitree_move":
                velocity = arguments.get("velocity")
                duration = arguments.get("duration", 1.0)
                self.unitree.move(velocity, duration)
                return {"velocity": velocity, "duration": duration}
            elif name == "unitree_stop":
                self.unitree.emergency_stop()
                return {"status": "stopped"}
            elif name == "dji_connect":
                self.dji.connect()
                return {"status": "connected"}
            elif name == "dji_takeoff":
                height = arguments.get("height", 1.0)
                self.dji.takeoff(height)
                return {"height": height}
            elif name == "dji_land":
                self.dji.land()
                return {"status": "landing"}
            else:
                raise ValueError(f"未知工具: {name}")
        except Exception as e:
            logger.error(f"工具执行失败: {str(e)}")
            raise

    async def run(self):
        transport = StdioServerTransport()
        await self.server.connect(transport)
        self.server.register_tool_handler(self._execute_tool)
        logger.info("机器人MCP服务已启动")
        await asyncio.Future()  # 保持服务运行

if __name__ == "__main__":
    server = RobotMCPServer()
    asyncio.run(server.run())