# 自定义智能体服务接入闪极拍拍镜<br>
闪极拍拍镜支持开发者部署自己的http服务上架到**我的智能体**中，并在闪极拍拍镜中进行访问

## 流程

### 1. 创建智能体服务<br> <a id="chapter1"></a>
- 首先，你需要自己写一个智能体类，类中必须实现chat和stream_chat方法，分别表示非流式和流式输出。这两个方法返回的结果必须是个Dict对象，且必须包含content和finish_reason字段。<br>
你可以参考示例：[food_agent](./food_agent.py)来实现
- 实现好自己的类后，可以在[client_initializer](./client_initializer.py)中实例化这个类。例如：<br>
    ```python
    # -*- encoding: utf-8 -*-
    import os
    from food_agent import FoodAgent
    
    MODEL = "qwen-plus"
    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("BASE_URL")
    agent_client = FoodAgent(model="qwen-plus", api_key=API_KEY, base_url=BASE_URL)
    ```
- 然后，在server.py中导入client_initializer.py中实例化的类。<br>
    ```python
    from client_initializer import agent_client
    ```
- 最后，启动http服务。
    ```shell
    nohup python server.py &
    ```
    
### 2.闪极拍拍镜中添加智能体 <a id="chapter2"></a>
  
- **手动添加**
       
  - 登陆**闪极APP**
  - 在底部导航栏选择**AI**，右上角点击➕号，然后选择**创建智能体**
    
    <img src="../../imgs/create_agent_sharge.png" width = "300" height = "500" alt="img" align=center /><br>
  - 勾选**OPEN AI**，填入对应配置信息，再点击**创建智能体**。<br> 至此，你的智能体已经成功接入，可在闪极拍拍镜中通过说：“找【智能体名称】”，可以唤醒对应的智能体并与它交互。
  > [!Note]
  > URL：填入[第1步](#chapter1)中创建的智能体服务的chat方法的url，例如：<br>
  > ```http://12.34.56.78:30000/custom_agent/chat```<br>
  > API KEY（可选）：根据你的智能体服务中是否需要鉴权来输入对应的API KEY
