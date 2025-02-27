import time
from modelcontextprotocol import Client
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    client = Client.connect_stdio()
    
    try:
        # 控制宇树机器人
        print("连接宇树机器人...")
        client.call_tool("unitree_connect", {})
        
        print("向前移动 (速度 1.5m/s, 持续2秒)")
        client.call_tool("unitree_move", {"velocity": 1.5, "duration": 2})
        
        # 控制大疆无人机
        print("\n连接大疆无人机...")
        client.call_tool("dji_connect", {})
        
        print("起飞到2米高度")
        client.call_tool("dji_takeoff", {"height": 2.0})
        
        print("悬停5秒...")
        time.sleep(5)
        
        print("降落")
        client.call_tool("dji_land", {})
        
    except Exception as e:
        print(f"操作失败: {str(e)}")
        client.call_tool("unitree_stop", {})
        client.call_tool("dji_land", {})

if __name__ == "__main__":
    main()