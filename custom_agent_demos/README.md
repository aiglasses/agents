# 智能体接入闪极拍拍镜Demo

## 介绍
本仓库是执行第三方智能体平台如Coze的智能体以及自定义智能体服务接入闪极拍拍镜的流程demo

功能：
- Coze上创建智能体，并接入闪极拍拍镜中
- 自定义智能体服务，接入闪极拍拍镜中

## 依赖
```shell
pip install -r requirements.txt
```

## 样例
| 智能体来源    | 鉴权方式      | demo地址                                                                                                       |
|----------|-----------|--------------------------------------------------------------------------------------------------------------|
| Coze     | PAT       | [examples/pat_agent/README_zh.md](examples/pat_agent/README_zh.md)                                 |
| Coze     | OAUTH JWT(开发者） | [examples/personal_oauth_jwt/README_zh.md](examples/personal_oauth_jwt/README_zh.md) |
| Coze     | OAUTH JWT(渠道） | [examples/channel_oauth_jwt/README_zh.md](examples/channel_oauth_jwt/README_zh.md)     |
| 自定义智能体服务 | 待更新       | [examples/custom_agent/README_zh.md](examples/custom_agent/README_zh.md)                           |


### 接入方式说明
coze是新一代AI应用开发平台，如果开发者没有太多编程基础，希望借助零代码或低代码的方式，快速搭建AI应用。建议选择coze等智能体平台作为接入方式。如果用户希望自定义自己的智能体服务，并提供更多定制化的功能，建议选择自定义智能体服务的方式进行接入，下面是不同鉴权方式的简要概述。
- COZE
  - PAT(更多信息，请参考：[PAT鉴权](https://www.coze.cn/docs/developer_guides/pat))<br>
  PAT(Personal Access Token),简称PAT。扣子平台中生成的个人访问令牌。PAT生成与使用便捷，适用于测试环境调试等场景。个人访问令牌有效期为1～30天，生成后不支持修改过期时间，过期后应重新申请<br>
  - OAUTH JWT(开发者)(更多信息，请参考：[OAUTH JWT(开发者)](https://www.coze.cn/docs/developer_guides/oauth_jwt))<br>
  OAuth Access Token，通过 OAuth 2.0 鉴权方式生成的 OAuth 访问令牌。该鉴权方式通常用于应用程序的身份验证和授权，和 PAT 鉴权方式相比，令牌有效期短，安全性更高，适用于线上生产环境。<br>
  - OAUTH JWT(渠道)(更多信息，请参考：[OAUTH JWT(渠道)](https://www.coze.cn/docs/developer_guides/oauth_jwt_channel))<br>
  OAuth Access Token, 通过 OAuth 2.0 鉴权方式生成的 OAuth 访问令牌。对于普通开发者来说，采用这种鉴权方式不用自己生成OAuth访问令牌，只需要申请加入闪极智能体团队，详情参考：[渠道鉴权](./examples/channel_oauth_jwt/README_zh.md)
- 自定义智能体服务
  - OAUTH JWT（根据自己的服务选择不同方式进行鉴权，闪极仅需要对应的API KEY来进行接入）

## 参考文档
- [COZE官方文档](https://www.coze.cn/docs/guides/welcome)
