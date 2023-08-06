import logging
import os

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.dnspod.v20210323 import dnspod_client, models

headers = {
    "X-TC-TraceId": "ffe0c072-8a5d-4e17-8887-a8a60252abca"
}

DOMAIN = "xoto.cc"
SECRET_ID = os.getenv('SECRET_ID', None)
SECRET_KEY = os.getenv('SECRET_KEY', None)


def run(method, ip_vpn):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        cred = credential.Credential(SECRET_ID, SECRET_KEY)

        # 实例化一个http选项，可选的，没有特殊需求可以跳过。
        httpProfile = HttpProfile()
        clientProfile = ClientProfile()
        set_client_profile(clientProfile, httpProfile)

        # 实例化要请求产品(以cvm为例)的client对象，clientProfile是可选的。
        client = dnspod_client.DnspodClient(cred, "ap-guangzhou", clientProfile)

        # 实例化一个cvm实例信息查询请求对象,每个接口都会对应一个request对象。
        req = models.DescribeRecordListRequest()
        req.Domain = DOMAIN
        # python sdk支持自定义header如 X-TC-TraceId、X-TC-Canary，可以按照如下方式指定，header必须是字典类型的
        req.headers = headers

        if method == "del":
            resp = client.DescribeRecordList(req)
            logging.debug(resp.to_json_string(indent=2))
            delete_record_about_vpn(client, resp)

        if method == "add":
            req_add = models.CreateRecordRequest()
            resp_add = add_record_about_vpn(ip_vpn, client, req_add)
            print("vpn add succeed, info:", resp_add.to_json_string(indent=2))

    except TencentCloudSDKException as err:
        print(err)


def add_record_about_vpn(ip, client, req_add):
    req_add.Domain = DOMAIN
    req_add.SubDomain = "vpn"
    req_add.Value = ip
    req_add.RecordLine = "默认"
    req_add.RecordType = "A"
    resp_add = client.CreateRecord(req_add)
    return resp_add


def delete_record_about_vpn(client, resp):
    for record in resp.RecordList:
        if record.Name == "vpn":
            req_del = models.DeleteRecordRequest()
            req_del.RecordId = record.RecordId
            req_del.Domain = DOMAIN
            resp_del = client.DeleteRecord(req_del)
            print("delete vpn record succeed, info:", resp_del.to_json_string(indent=2))


def set_client_profile(client_profile, http_profile):
    http_profile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
    http_profile.keepAlive = True  # 状态保持，默认是False
    http_profile.reqMethod = "GET"  # get请求(默认为post请求)
    http_profile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
    http_profile.endpoint = "dnspod.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)
    client_profile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
    client_profile.language = "en-US"  # 指定展示英文（默认为中文）
    client_profile.httpProfile = http_profile

# if __name__ == '__main__':
#     run('add',"xx")