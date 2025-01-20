# 本文档介绍添加coze agent的不同接入方式

## 目录
- [接入方式总览](#接入方式总览)
- [1. PAT](#1-PAT)
  - [1.1 COZE PAT鉴权](#11-COZE-PAT鉴权更多信息请参考添加个人访问令牌)
  - [1.2 COZE创建智能体](#12-COZE创建智能体)
    - [1.2.1 手动创建](#121-手动创建更多信息请参考搭建一个AI智能体)
    - [1.2.2 API创建](#122-API创建更多信息可参考文档创建智能体API)
  - [1.3 COZE发布智能体](#13-COZE发布智能体)
    - [1.3.1 手动发布](#131-手动发布更多信息请参考智能体发布概述)
    - [1.3.2 API发布](#132-API发布更多信息请参考发布智能体API)
  - [1.4 闪极拍拍镜中添加智能体](#14-闪极拍拍镜中添加智能体)
    - [1.4.1 手动添加](#141-手动添加) 
- [2. OAUTH JWT(开发者)](#2-OAUTH-JWT开发者)
  - [2.1 COZE Oauth JWT(开发者)鉴权](#21-COZE-Oauth-JWT开发者鉴权更多信息请参考OAuth-JWT授权开发者)
  - [2.2 COZE创建智能体](#22-COZE创建智能体)
    - [2.2.1 手动创建](#221-手动创建更多信息请参考搭建一个AI智能体)
    - [2.2.2 API创建](#222-API创建更多信息可参考文档创建智能体API)
  - [2.3 COZE发布智能体](#23-COZE发布智能体)
    - [2.3.1 手动发布](#231-手动发布更多信息请参考智能体发布概述)
    - [2.3.2 API发布](#232-API发布更多信息请参考发布智能体API)
  - [2.4 闪极拍拍镜中添加智能体](#24-闪极拍拍镜中添加智能体)
    - [2.4.1 手动添加](#241-手动添加)
- [3. OAUTH JWT(渠道)](#3-OAUTH-JWT渠道)
  - [3.1 COZE创建智能体](#31-COZE创建智能体)
    - [3.1.1 手动创建](#311-手动创建更多信息请参考搭建一个AI智能体)
    - [3.1.2 API构建](#312-API创建更多信息可参考文档创建智能体API)
  - [3.2 COZE发布智能体](#32-COZE发布智能体)
    - [3.2.1 手动发布](#321-手动发布更多信息请参考智能体发布概述)
    - [3.2.2 API发布](#322-API发布更多信息请参考发布智能体API)
  - [3.3 闪极拍拍镜中添加智能体](#33-闪极拍拍镜中添加智能体)
    - [3.3.1 手动添加](#331-手动添加)

## 接入方式总览
- [PAT](#1-PAT)

  PAT(Personal Access Token),简称PAT。扣子平台中生成的个人访问令牌。PAT生成与使用便捷，适用于测试环境调试等场景。个人访问令牌有效期为1～30天，生成后不支持修改过期时间，过期后应重新申请
- [OAUTH JWT(开发者)](#2-OAUTH-JWT开发者)

    OAuth Access Token，通过 OAuth 2.0 鉴权方式生成的 OAuth 访问令牌。该鉴权方式通常用于应用程序的身份验证和授权，和 PAT 鉴权方式相比，令牌有效期短，安全性更高，适用于线上生产环境。
- [OAUTH JWT(渠道)](#3-OAUTH-JWT渠道)

    OAuth Access Token, 通过 OAuth 2.0 鉴权方式生成的 OAuth 访问令牌。对于普通开发者来说，采用这种鉴权方式不用自己生成OAuth访问令牌，只需要申请加入**ShargeAI**团队

### 1. PAT

> [!NOTE] 
> 如果已熟悉 COZE 智能体的创建及发布流程，可直接跳到步骤 [1.4 闪极拍拍镜中添加智能体](#14-闪极拍拍镜中添加智能体)。

#### 1.1 COZE PAT鉴权（更多信息请参考：[添加个人访问令牌](https://www.coze.cn/docs/developer_guides/pat)）

1. 登录 [**Coze平台**](https://www.coze.cn/home)。
2. 在左侧菜单栏下方，单击**API图标**。

   <img src="../../imgs/coze_api.png" width="300" height="150" alt="api图标">

3. 进入 **授权 -> 个人访问令牌** 页面。

   <img src="../../imgs/personal_access_token.png" width="300" height="150" alt="个人访问令牌">

4. 单击 **添加新令牌**。
5. 在弹出的页面完成以下配置，然后单击确定：

   | 配置项       | 说明          |
   |--------------|----------------|
   | 名称         | 个人访问令牌的名称  
   | 过期时间     | 个人访问令牌的有效期时长。令牌过期后将会失效，无法继续用它来调用扣子 API。生成令牌后，无法修改过期时间。                                      
   | 权限         | 个人访问令牌的权限。调用 API 时，个人访问令牌应具备对应的 API 权限，否则会抛出异常 4101。                                                
   | 访问团队空间 | 可以使用该令牌的空间。<br>**说明：**<br>如果选择所有空间，则此个人访问令牌可用于你目前和将来拥有的所有团队空间，不包括你加入的、隶属于其他人的团队空间。

   <img src="../../imgs/add_pat.png" width="300" height="400" alt="添加个人pat令牌">

6. **复制并妥善保存个人访问令牌。**  
   生成的令牌仅在此时展示一次，请即刻复制并保存。

#### 1.2 COZE创建智能体

##### 1.2.1 手动创建（更多信息请参考：[搭建一个AI智能体](https://www.coze.cn/docs/guides/agent_quick_start)）

1. 创建一个智能体：
   - 登录 [扣子平台](https://www.coze.cn/home)。
   - 在页面左上角单击 ⊕，然后点击 **创建智能体**。

     <img src="../../imgs/add_agent2.png" width="300" height="150" alt="创建智能体">

   - 输入智能体名称、功能介绍等信息，也可以切换到 AI 构建，通过自然语言描述你的智能体创建需求，扣子会根据描述自动创建一个专属智能体。详情请参考：[通过AI创建智能体](https://www.coze.cn/docs/guides/assistant_coze#d11d798b)。

     <img src="../../imgs/add_agent3.png" width="300" height="150" alt="智能体信息">

2. 单击确认。进入智能体编排页面后可以：
   - 在左侧 **人设与回复逻辑** 面板中描述智能体的身份和任务。
   - 在中间 **技能** 面板为智能体配置扩展能力。
   - 在右侧 **预览与调试** 面板实时调试智能体。

     <img src="../../imgs/debug_agent.png" width="300" height="150" alt="调试智能体">

##### 1.2.2 API创建（更多信息可参考文档：[创建智能体API](https://www.coze.cn/docs/developer_guides/create_bot)）

- **请求方式**：`POST`  
- **请求地址**：[https://api.coze.cn/v1/bot/create](https://api.coze.cn/v1/bot/create)  
- 更多接口参数和示例请参考原文档

#### 1.3 COZE发布智能体

##### 1.3.1 手动发布（更多信息请参考：[智能体发布概述](https://www.coze.cn/docs/guides/publish_agent)）

1. 创建智能体后，点击右上角 **发布**。

   <img src="../../imgs/release_agent.png" width="300" height="150" alt="发布智能体">

2. 填写发布记录，选择发布平台时务必选择 **API方式**。

   <img src="../../imgs/release_agent2.png" width="300" height="150" alt="选择发布平台">
   
##### 1.3.2 API发布（更多信息请参考：[发布智能体API](https://www.coze.cn/docs/developer_guides/publish_bot)）

- **请求方式**：`POST`  
- **请求地址**：[https://api.coze.cn/v1/bot/publish](https://api.coze.cn/v1/bot/publish)  
- 更多接口参数和示例请参考原文档

#### 1.4 闪极拍拍镜中添加智能体

##### 1.4.1 手动添加

1. 登录 **闪极APP**。
2. 在底部导航栏选择 **AI**，右上角点击 ➕，然后选择 **创建智能体**。

   <img src="../../imgs/create_agent_sharge.png" width="300" height="500" alt="创建智能体">

3. 勾选 **COZE**，填入对应配置信息，再点击 **创建智能体**。（APP待更新）

至此，你的智能体已成功接入。您可以在闪极拍拍镜中通过说：“找【智能体名称】”，唤醒对应的智能体并与它交互。

### 2. OAUTH JWT(开发者)

> [!NOTE]
> 如果已知晓COZE智能体创建及发布的流程，可直接跳到步骤4：[闪极拍拍镜中添加智能体](#24-闪极拍拍镜中添加智能体)

#### 2.1 COZE Oauth JWT（开发者）鉴权(更多信息请参考：[OAuth JWT授权（开发者）](https://www.coze.cn/docs/developer_guides/oauth_jwt))
- 在扣子平台创建OAuth应用
  - 登陆[**Coze平台**](https://www.coze.cn/home)
  - 在授权 -> [OAuth应用](https://www.coze.cn/open/oauth/apps)页面单击创建新应用
    
    <img src="../../imgs/jwt_client.png" width = "300" height = "150" alt="img">
    
  - 填写应用的基本信息
  
    | 配置项 | 说明 |
    |-----|----------------------------------------------------------------------------------|
    | 应用类型 | 应用的类型，此处应指定为**普通** 
    | 客户端类型 | 客户端类型，此处应设置为**服务类应用** 
    | 应用名称 | 应用的名称，在扣子平台中全局唯一 
    | 描述 | 应用的基本描述信息

    <img src="../../imgs/client_basic_info.png" width = "300" height = "150" alt="img">
    
  - 填写配置信息，然后点击确定，完成配置
  
    | 配置项 | 说明 |
    |-----|----------------------------------------------------------------------------------|
    | 权限 | 应用程序调用扣子API时需要的权限范围 
    | 重定向URL | 无需配置
    | 客户端ID和客户端密钥 | 无需配置 
    | 公钥和私钥 | 用于应用程序客户端身份认证的非对称密钥。<br>单击创建key，页面将自动创建一对公钥和私钥，公钥自动配置在扣子中，私钥以private_key.pem文件格式由网页自动下载到本地。支持创建最多三对公钥和私钥<br>•建议将private_key.pem文件安全地存储在只有您应用可以访问的位置

    <img src="../../imgs/jwt_create_key.png" width = "300" height = "150" alt="img">

- 在扣子平台完成OAuth应用授权
  - 登陆[**Coze平台**](https://www.coze.cn/home)
  - 在**授权**->**OAuth应用**页面找到对应的OAuth应用，点击编辑操作
    
    <img src="../../imgs/jwt_authorize.png" width = "300" height = "150" alt="img">

    <img src="../../imgs/jwt_authorize2.png" width = "300" height = "150" alt="img">

- 应用程序通过公钥和私钥签署JWT
  - **Python**

    ```python
    # -*- encoding: utf-8 -*-
    import string
    import secrets
    import time
    import jwt
    from jwt import PyJWTError

    def _generate_random_string(length: int = 33):
        chars = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(chars) for _ in range(length))
        return random_string


    private_key = 【你的OAuth应用的私钥】


    def generate_jwt(
            public_key: str,
            private_key: str,
            service_id: str,
            typ: str = "JWT",
            alg: str = "RS256",
            aud: str = "api.coze.cn",
            iat: int = int(time.time()),
            exp: int = int(time.time()) + 86400 * 3600,
            ):
        """
        生成JWT。
        """
        headers = {
            'alg': alg, # 签名使用的加密算法。固定为RS256，即非对称加密算法
            'typ': typ, # 固定为JWT
            'kid': public_key  # OAuth应用的公钥指纹，需要从扣子平台获取
        }

        payload = {
            'iss': service_id,
            'aud': aud,
            'iat': iat,
            'exp': exp,
            'jti': _generate_random_string(33)
        }

        # 使用私钥对Header和Payload进行签名
        try:
            token = jwt.encode(payload, private_key, algorithm=headers["alg"], headers=headers)
        except PyJWTError as e:
            print(f"Error generating JWT: {e}")
            return None
        return token


    if __name__ == "__main__":
        jwt_str = generate_jwt(
            service_id=【你的OAuth应用的id】，
            public_key= 【你的OAuth应用的公钥指纹】,
            private_key=private_key,
            alg="RS256",
            typ="JWT",
            aud="api.coze.cn",
            iat=int(time.time()),
            exp=int(time.time()) + 86400 * 3600,
        )
        print(jwt_str)
        ```

- 应用程序通过JWT获取Oauth Access Token API，获取访问令牌
  - **Python**

    ```python
    # -*- encoding: utf-8 -*-
    import requests


    def get_oauth_access_token(
            jwt_token: str,
            token_url: str = 'https://api.coze.cn/api/permission/oauth2/token',
            duration_seconds: int = 86400,
            ):
        """
        使用JWT获取OAuth Access Token。

        :param jwt_token: 完整的JWT字符串
        :return: Access Token和过期时间
        """
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f'Bearer {jwt_token}'
        }
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'duration_seconds': duration_seconds  # Token的有效期
        }

        response = requests.post(token_url, headers=headers, json=data)

        if response.status_code == 200:
            access_token_response = response.json()
            return access_token_response.get('access_token')
        else:
            print(f"Failed to get access token: {response.text}")
            return None, None


    if __name__ == "__main__":
        access_token = get_oauth_access_token(
            jwt_token=【上一步生成的JWT】,
        )
        print(access_token)
    ```

  - **Curl**

    ```bash
    curl --location --request POST 'https://api.coze.cn/api/permission/oauth2/token' \ 
    --header 'Content-Type: application/json' \ 
    --header 'Authorization: Bearer 【上一步生成的JWT】 \ 
    --data '{ 
        "duration_seconds": 86400, 
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer" 
    }' 
    ```

#### 2.2 COZE创建智能体
##### 2.2.1 手动创建（更多信息请参考：[搭建一个AI智能体](https://www.coze.cn/docs/guides/agent_quick_start))
同 [PAT手动创建](#121-手动创建更多信息请参考搭建一个AI智能体)
          
##### 2.2.2 API创建（更多信息可参考文档：[创建智能体API](https://www.coze.cn/docs/developer_guides/create_bot))
同 [PAT API创建](#122-API创建更多信息可参考文档创建智能体API)

#### 2.3 COZE发布智能体
  
##### 2.3.1 手动发布（更多信息请参考：[智能体发布概述](https://www.coze.cn/docs/guides/publish_agent)）
同 [PAT手动发布](#131-手动发布更多信息请参考智能体发布概述)
   
##### 2.3.2 API发布(更多信息请参考：[发布智能体API](https://www.coze.cn/docs/developer_guides/publish_bot))
同 [PAT API发布](#132-API发布更多信息请参考发布智能体API)
    
#### 2.4 闪极拍拍镜中添加智能体
  
##### 2.4.1 手动添加
同[PAT 闪极拍拍镜添加智能体](#141-手动添加)

### 3. OAUTH JWT(渠道)

> [!NOTE]
> **确保自己的COZE账号具备发布智能体到闪极科技智能体团队的权限**<br>
目前闪极智能体平台尚未成为COZE公共平台（正在申请中），在申请通过之前，只有受邀请的成员才能申请发布自有智能体到闪极智能体平台，您可通过以下方式查看自己是否具备对应的发布权限。
>  - 登陆[**Coze平台**](https://www.coze.cn/home)
>  - 点击页面左侧的工作空间，然后点击**个人空间**查看自己是否在**shargeAI**的团队下

>  <img src="../../imgs/check_team.png" width = "300" height = "150" alt="img">
    
>  - 如果您的团队不包含**shargeAI**，您需要向shargeAI团队管理员 (邮箱：zenggangxin@shargetech.com)申请成为团队成员
>  - 如果您的团队中包含**shargeAI**，则您具备对应的发布权限

> [!NOTE]
> 如果已知晓COZE智能体创建及发布的流程，可直接跳到步骤3：[闪极拍拍镜中添加智能体](#33-闪极拍拍镜中添加智能体)

#### 3.1 COZE创建智能体

##### 3.1.1 手动创建（更多信息请参考：[搭建一个AI智能体](https://www.coze.cn/docs/guides/agent_quick_start))
>[!NOTE]<br>需要在**ShargeAI**团队下创建智能体,否则智能体发布不到**闪极智能体**平台
创建方式同[PAT 手动创建](#121-手动创建更多信息请参考搭建一个AI智能体)
      
##### 3.1.2 API创建（更多信息可参考文档：[创建智能体API](https://www.coze.cn/docs/developer_guides/create_bot))
###### 鉴权
- COZE PAT鉴权(参考：[pat鉴权](#11-COZE-PAT鉴权更多信息请参考添加个人访问令牌))
- COZE Oauth JWT（开发者）鉴权(参考：[personal oauth jwt](#21-COZE-Oauth-JWT开发者鉴权更多信息请参考OAuth-JWT授权开发者))

###### 接口信息
同[PAT API创建](#122-API创建更多信息可参考文档创建智能体API)

#### 3.2 COZE发布智能体
  
##### 3.2.1 手动发布（更多信息请参考：[智能体发布概述](https://www.coze.cn/docs/guides/publish_agent)）
- 创建智能体后，点击右上角发布
  
    <img src="../../imgs/release_agent.png" width = "300" height = "150" alt="img">
  
- 填写发布记录，选择发布平台时务必选择**闪极智能体**。
  
    <img src="../../imgs/release_agent3.png" width = "300" height = "150" alt="img">
   
##### 3.2.2 API发布(更多信息请参考：[发布智能体API](https://www.coze.cn/docs/developer_guides/publish_bot))
###### 鉴权：
- 方式同[鉴权](#鉴权)

###### 接口信息
同[PAT API发布](#132-API发布更多信息请参考发布智能体API)
    
#### 3.3 闪极拍拍镜中添加智能体
  
##### 3.3.1 手动添加
       
- 登陆**闪极APP**
- 在底部导航栏选择**AI**，右上角点击➕号，然后选择**创建智能体**
    
    <img src="../../imgs/create_agent_sharge.png" width = "300" height = "500" alt="img">
- 勾选**COZE**，填入对应配置信息，再点击**创建智能体**。<br> 至此，你的智能体已经成功接入，可在闪极拍拍镜中通过说：“找【智能体名称】”，可以唤醒对应的智能体并与它交互。
