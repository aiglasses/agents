# Coze智能体接入闪极拍拍镜-Oauth JWT(渠道）鉴权

## 流程

> [!NOTE]
> **确保自己的COZE账号具备发布智能体到闪极科技智能体团队的权限**<br>
目前闪极智能体平台尚未成为COZE公共平台（正在申请中），在申请通过之前，只有受邀请的成员才能申请发布自有智能体到闪极智能体平台，您可通过以下方式查看自己是否具备对应的发布权限。
>  - 登陆[**Coze平台**](https://www.coze.cn/home)
>  - 点击页面左侧的工作空间，然后点击个人空间查看自己是否在**shargeAI**的团队下

>  <img src="../../imgs/check_team.png" width = "300" height = "150" alt="img">
    
>  - 如果您的团队不包含**shargeAI**，您需要向shargeAI团队管理员 (邮箱：zenggangxin@shargetech.com)申请成为团队成员
>  - 如果您的团队中包含**shargeAI**，则您具备对应的发布权限

> [!NOTE]
> 如果已知晓COZE智能体创建及发布的流程，可直接跳到步骤3：[接入闪极拍拍镜](#add agent3)

### 1. COZE创建智能体
   - **手动创建（更多信息请参考：[搭建一个AI智能体](https://www.coze.cn/docs/guides/agent_quick_start))**
     - 创建一个智能体
       - 登陆[扣子平台](https://www.coze.cn/home)
       - 在页面左上角单击⊕，然后点击创建智能体
         
         <img src="../../imgs/add_agent2.png" width = "300" height = "150" alt="img">
         
       - 输入智能体名称、功能介绍等信息，也可以切换到AI构建，通过自然语言描述你的智能体创建需求，扣子会根据描述自动创建一个专属于你的智能体（需要注意的是，**工作空间**需要选择**ShargeAI**，详情请参考文档：[通过AI创建智能体](https://www.coze.cn/docs/guides/assistant_coze#d11d798b)）
       
         <img src="../../imgs/add_agent3.png" width = "300" height = "400" alt="img">
         
       - 单击确认。创建智能体后，你会直接进入智能体编排页面。你可以:
         - 在左侧**人设与回复逻辑**面板中描述智能体的身份和任务
         - 在中间**技能**面板为智能体配置各种扩展能力
         - 在右侧**预览与调试**面板中，实时调试智能体

            <img src="../../imgs/debug_agent.png" width = "300" height = "150" alt="img">
        
      - 编写提示词
        - 配置智能体的第一步就是编写提示词，也就是智能体的人设与回复逻辑。智能体的人设与回复逻辑定义了智能体的基本人设，此人设会持续影响智能体在所有回话中的回复效果。建议在人设与回复逻辑中指定模型的角色、设计回复的语言风格、限制模型的回答范围，让对话更符合用户预期。你可以单击优化，让大语言模型优化为结构化内容。更多详细信息，参考[编写提示词](https://www.coze.cn/docs/guides/prompt)
      
          <img src="../../imgs/edit_prompt.png" width = "300" height = "150" alt="img">
         
      - （可选）为智能体添加技能。<br> 如果模型能力可以基本覆盖智能体的功能，则只需要为智能体编写提示词即可。但是如果你为智能体设计的功能无法仅通过模型能力完成，则需要为智能体添加技能，拓展它的能力边界。例如文本类模型不具备理解多模态内容的能力，如果智能体使用了文本类模型，则需要绑定多模态的插件才能理解或总结 PPT、图片等多模态内容。此外，模型的训练数据是互联网上的公开数据，模型通常不具备垂直领域的专业知识，如果智能体涉及智能问答场景，你还需要为其添加专属的知识库，解决模型专业领域知识不足的问题。详情请查看：[为智能体添加技能](https://www.coze.cn/docs/guides/agent_plugin)
      - 调试智能体<br>配置好智能体后，就可以在**预览与调试**区域中测试智能体是否符合预期。
        
        <img src="../../imgs/preview_agent.png" width = "300" height = "150" alt="img">
          
  - **API创建（更多信息可参考文档：[创建智能体API](https://www.coze.cn/docs/developer_guides/create_bot)）**
    - 鉴权 <a id="鉴权"></a>
      - COZE PAT鉴权(参考：[pat鉴权](../pat_agent/README_zh.md),更多信息请参考：[添加个人访问令牌](https://www.coze.cn/docs/developer_guides/pat))
      - COZE Oauth JWT（开发者）鉴权(参考：[personal oauth jwt](../personal_oauth_jwt/README_zh.md),更多信息请参考：[OAuth JWT授权（开发者）](https://www.coze.cn/docs/developer_guides/oauth_jwt))
    
    - **基础信息**
   
         | 参数 | 参数详情 |
         | --- | --- |
         | **请求方式** | POST 
         | **请求地址** | https://api.coze.cn/v1/bot/create 
         | **权限** | **createBot**<br>确保调用这个接口使用的个人令牌 (access token) 开通了createBot权限，详细信息参考：[鉴权方式](https://www.coze.cn/docs/developer_guides/authentication) 
         | **接口说明** | 调用接口创建一个新的智能体 

    - **Header**

         | 参数 | 取值 | 说明 |
         | --- | --- | --- |
         | Authorization | Bearer $Access_Token |用于验证客户端身份的访问令牌, 其中Access_Token为**步骤1** [鉴权](#鉴权)中生成的token
         | Content-Type | application/json | 解释请求正文的方式

    - **Body**

         | 参数 | 类型 | 是否必选 | 说明 |
         | --- | --- | --- | --- |
         | space_id | String |是| Bot所在的空间的Space ID
         | name | String |是| 智能体名称。1～20个字符
         | description | String |否| 智能体的描述信息。0～500个字符，默认为空
         | icon_file_id | String |否| 作为智能体头像的文件ID
         | prompt_info | Object |否| 智能体的人设与回复逻辑
         | onboarding_info | Object |否| 智能体的开场白相关设置

    - **Prompt_Info object**

         | 参数 | 类型 | 是否必选 | 说明 |
         | --- | --- | --- | --- |
         | prompt | String |否| 智能体人设与回复逻辑，0～20000个字符，默认为空

    - **Onboarding_info object**

         | 参数 | 类型 | 是否必选 | 说明 |
         | --- | --- | --- | --- |
         | prologue | String |否| 智能体的开场白。长度为 0~ 300 个字符。默认无开场白。 <br> 开场白中如果设置了用户名称变量{{user_name}}，API 场景中需要业务方自行处理，例如展示开场白时将此变量替换为业务侧的用户名称。
         | suggested_questions | Array of String |否| 智能体的开场白预置问题。每个问题长度为 0~ 50 个字符，问题数量无限制。默认无开场白预置问题。

    - **返回结果**

         | 参数 | 类型 | 说明 |
         | --- | --- | --- |
         | code | Integer |调用状态码，0表示调用成功，其他值表示调用失败。可通过msg字段判断详细的错误原因
         | msg | String | 状态信息。API调用失败时可通过此字段查看详细错误信息
         | data| Object|接口响应的业务信息
         | data.bot_id| String | 创建的智能体ID

    - **Curl样例**

        ```bash
        curl --location --request POST 'https://api.coze.cn/v1/bot/create' \ 
        --header 'Authorization: Bearer pat_OYDacMzM3WyOWV3Dtj2bHRMymzxP****' \ 
        --header 'Content-Type: application/json' \ 
        --data-raw '{ 
            "space_id": "736142423532160****", 
            "name": "每日学一菜", 
            "description": "每天教你一道菜的做法，暑假之后你将成为中餐大厨～", 
            "icon_file_id": "73694959811****", 
            "prompt_info": { 
                "prompt": "你是一位经验丰富的中餐大厨，能够熟练传授各类中餐的烹饪技巧，每日为大学生厨师小白教学一道经典中餐的制作方法。" 
            }, 
            "onboarding_info": { 
                "prologue": "欢迎你，学徒，今天想学一道什么样的菜？", 
                "suggested_questions": [ 
                    "川菜，我想吃辣的", 
                    "广东菜，来点鲜的", 
                    "随机教我一道菜" 
                ] 
            } 
        }'
        ```

    - **Python样例**

        ```python
        # -*— encoding: utf-8 -*-
        import requests
    
        url = 'https://api.coze.cn/v1/bot/create'
        headers = {
            'Authorization': 'Bearer pat_OYDacMzM3WyOWV3Dtj2bHRMymzxP****',
            'Content-Type': 'application/json'
        }
        data = {
            "space_id": "736142423532160****",
            "name": "每日学一菜",
            "description": "每天教你一道菜的做法，暑假之后你将成为中餐大厨～",
            "icon_file_id": "73694959811****",
            "prompt_info": {
                "prompt": "你是一位经验丰富的中餐大厨，能够熟练传授各类中餐的烹饪技巧，每日为大学生厨师小白教学一道经典中餐的制作方法。"
            },
            "onboarding_info": {
                "prologue": "欢迎你，学徒，今天想学一道什么样的菜？",
                "suggested_questions": [
                    "川菜，我想吃辣的",
                    "广东菜，来点鲜的",
                    "随机教我一道菜"
                ]
            }
        }
    
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("请求成功，响应内容：", response.json())
        else:
            print("请求失败，状态码：", response.status_code, "，错误信息：", response.text)
        ```

### 2. COZE发布智能体
  
  - **手动发布（更多信息请参考：[智能体发布概述](https://www.coze.cn/docs/guides/publish_agent)）**
    - 创建智能体后，点击右上角发布
      
      <img src="../../imgs/release_agent.png" width = "300" height = "150" alt="img">
      
    - 填写发布记录，选择发布平台时务必选择**API方式**。
      
      <img src="../../imgs/release_agent2.png" width = "300" height = "150" alt="img">
   
  - **API发布(更多信息请参考：[发布智能体API](https://www.coze.cn/docs/developer_guides/publish_bot))**
    - 鉴权方式同[智能体创建](#鉴权)
    
    - **基础信息**
   
         | 参数 | 参数详情 |
         | --- | --- |
         | **请求方式** | POST |
         | **请求地址** | [https://api.coze.cn/v1/bot/publish](https://api.coze.cn/v1/bot/publish) |
         | **权限** | **publish**<br>确保调用这个接口使用的个人令牌 (access token) 开通了publish权限，详细信息参考：[鉴权方式](https://www.coze.cn/docs/developer_guides/authentication) |
         | **接口说明** | 调用接口将指定智能体发布到API、WebSDK或者自定义渠道 |

    - **Header**

         | 参数 | 取值 | 说明 |
         | --- | --- | --- |
         | Authorization | Bearer $Access_Token |用于验证客户端身份的访问令牌, 其中Access_Token为**步骤1** [鉴权](#鉴权)中生成的token
         | Content-Type | application/json | 解释请求正文的方式

    - **Body**

         | 参数        | 类型              | 是否必选 | 示例         | 说明                                                                            |
         |------------|------------------|---------|-------------|----|
         | bot_id      | String            | 是       | 7328668***  | 要发布的智能体ID。<br>进入智能体的开发页面，开发页面URL中bot参数后的数字就是智能体ID。例如https://www.coze.com/space/341****/bot/7328668****，bot_id为7328668****。 |
         | connector_id| Array of String   | 是       | ["1024"]     | 智能体的发布渠道ID列表。目前支持通过此API将智能体发布为Agent as API、WebSDK以及自定义渠道。<br> • Agent as API: 1024<br>• WebSDK: 999<br>• 自定义渠道: 自定义渠道ID，获取方式可以参考渠道入驻概述。需要保证使用自定义渠道的创建者的访问令牌来进行访问。 |

    - **PublishDraftBotData**

         | 参数 | 类型 | 示例 | 说明 |
         | --- | --- | --- | --- |
         | bot_id | String |7328668***| 智能体ID
         | version | String |1724150564914| 智能体版本号

    - **返回参数**

        | 返回参数 | 类型 | 示例 | 说明 |
        | ---- | ---- | ---- | ---- |
        | code | Integer | 0 | 调用状态码。<br>• 0表示调用成功。<br>• 其他值表示调用失败。你可以通过msg字段判断详细的错误原因。 |
        | msg | String | | 状态信息。API调用失败时可通过此字段查看详细错误信息 |
        | data | Object of PublishDraftBot Data | {"bot_id": "743961547827****", "version": "1732190531****"} | 接口响应的业务信息。 |

    - **Curl样例**

        ```bash
        curl --location --request POST 'https://api.coze.cn/v1/bot/publish' \ 
        --header 'Authorization: Bearer $AccessToken' \ 
        --header 'Content-Type: application/json' \ 
        --data-raw '{ 
            "bot_id": "7439615478273*****", 
            "connector_ids": [ 
                "1024" 
            ]  
        }'
        ```

    - **Python样例**

        ```python
        # -*- encoding: utf-8 -*-
        import requests
    
        url = 'https://api.coze.cn/v1/bot/publish'
        access_token = '$AccessToken'  # 请将此处替换为实际的访问令牌
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            "bot_id": "7439615478273*****",
            "connector_ids": [
                "1024"
            ]
        }
    
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("请求成功，响应内容：", response.json())
        else:
            print("请求失败，状态码：", response.status_code, "，错误信息：", response.text)
        ```
    
### 3.闪极拍拍镜中添加智能体 <a id="add agent3"></a>
  
- **手动添加**
       
  - 登陆**闪极APP**
  - 在底部导航栏选择**AI**，右上角点击➕号，然后选择**创建智能体**
    
    <img src="../../imgs/create_agent_sharge.png" width = "300" height = "500" alt="img">
  - 勾选**COZE**，填入对应配置信息，再点击**创建智能体**。<br> 至此，你的智能体已经成功接入，可在闪极拍拍镜中通过说：“找【智能体名称】”，可以唤醒对应的智能体并与它交互。
