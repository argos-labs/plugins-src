"""
====================================
:mod:`argoslabs.shop.shop11st`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Rossum API module
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/11/22]
#     - IP주소 변경: https://openapi.11st.co.kr/openapi/OpenApiServiceRegister.tmall
#     - 개발가이드:  https://openapi.11st.co.kr/openapi/OpenApiGuide.tmall?categoryNo=110
#  * [2022/11/21]
#     - 독립 플러그인이 아닌 "Dynamic Python" 코드로 작성
#     - 결과의 목록 JSON을 다음의 입력으로 API 호출
#       - http://61.109.249.21:31000/swagger-ui.html#/platform-order-data-controller/saveUsingPOST
#  * [2022/11/03]
#     - starting

################################################################################
import os
import sys
import yaml
import json
import pprint
import pathlib
import requests
import traceback
import xmltodict
import logging
import logging.handlers


################################################################################
def get_logger(logfile,
                logsize=500*1024, logbackup_count=4,
                logger=None, loglevel=logging.DEBUG):
    loglevel = loglevel
    if logfile:
        pathlib.Path(logfile).parent.mkdir(parents=True, exist_ok=True)
        if logger is None:
            logger = logging.getLogger(os.path.basename(logfile))
        logger.setLevel(loglevel)
        if logger.handlers is not None and len(logger.handlers) >= 0:
            for handler in logger.handlers:
                logger.removeHandler(handler)
            logger.handlers = []
        loghandler = logging.handlers.RotatingFileHandler(
            logfile,
            maxBytes=logsize, backupCount=logbackup_count,
            encoding='utf8')
    else:
        if logger is None:
            logger = logging.getLogger()
        loghandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s-%(name)s-%(levelname)s-'
        '%(filename)s:%(lineno)s-[%(process)d] %(message)s')
    loghandler.setFormatter(formatter)
    logger.addHandler(loghandler)
    return logger


################################################################################
class Shop11stApi(object):
    # ==========================================================================
    API_ORDER_LIST = 'https://api.11st.co.kr/rest/ordservices/completed/{{start_time}}/{{end_time}}'
    API_ORDER_INFO = 'https://api.11st.co.kr/rest/ordservices/complete/{{ord_no}}'

    # ==========================================================================
    def __init__(self, yaml_f) -> None:
        if not os.path.exists(yaml_f):
            raise IOError(f'Cannot read YAML config file "{{yaml_f}}"')
        self.yaml_f = yaml_f
        with open(yaml_f) as ifp:
            self.conf = yaml.load(ifp, yaml.SafeLoader)
        self.logger = get_logger(self.conf['env']['logfile'])
        self.logger.info(f'Creating {{self.__class__.__name__}} ...')

    # ==========================================================================
    def __enter__(self):
        return self
        
    # ==========================================================================
    def __exit__(self, *args):
        ...

    # ==========================================================================
    def call_api(self, od, oid):
        try:
            self.logger.info('call_api: Trying to fill out api data')
            api_d = {{
                "mallCode": self.conf['const']['mallCode'], # 고정 정보
                "orderDeliveryList": [  # 현재 구조는 1개만 나옴 (목록에)
                {{
                    "deliveryAddress": oid['rcvrBaseAddr'] + ' ' + oid['rcvrDtlsAddr'],  # 배송지 : "rcvrBaseAddr" + "rcvrDtlsAddr" (사이에 공백이 없으면 추가)
                    "deliveryDate": None,   # 배송요청일 : 비움
                    "deliveryMessage": oid['ordDlvReqCont'],    # 배송메시지 : "ordDlvReqCont"
                    "deliveryPost": oid['rcvrMailNo'],        # 배송지우편번호 : "rcvrMailNo"
                    "deliveryRibbonLeft": None, # 비움
                    "deliveryRibbonRight": None,       # 비움
                    "deliveryTime": None,         # 비움
                    "orderDeliveryGoodsList": [
                        {{
                        "goodsName": oid['prdNm'],   # 상품명 : "prdNm"
                        "goodsPrice": int(oid['ordPayAmt']), # 상품금액 : 일단 "ordPayAmt" 로 하는데 상품이 여러개 있을 때 (목록) 체크 요
                        "goodsQuantity": int(oid['ordQty']),  # 수량 : "ordQty"
                        "orderDeliveryGoodsOptionList": [
                            {{
                            "optionName": None,  # 비움 (옵션이 여러개 선택되는 경우가 있는지 확인)
                            "optionPrice": None,       # 비움 (옵션이 여러개 선택되는 경우가 있는지 확인)
                            "optionQuantity": None         # 비움 (옵션이 여러개 선택되는 경우가 있는지 확인)
                            }}
                        ]
                        }}
                    ],
                    "receiverName": oid['rcvrNm'],   # 받는사람이름 : "rcvrNm"
                    "receiverPhone": oid['rcvrPrtblNo'], # 받는사람핸번 : "rcvrPrtblNo"
                    "receiverTel": oid['rcvrTlphn'],    # 받는사람전번 : "rcvrTlphn"
                }}
                ],
                "orderNumber": oid['ordNo'],    # 주문번호 : "ordNo"
                "orderTimeString": oid['ordDt'],   # 주문시각 : "ordDt"
                "ordererMallId": oid['memID'],     # 주문자ID : "memID"
                "ordererName": oid['ordNm'],    # 주문자이름 : "ordNm"
                "ordererPhone": oid['ordPrtblTel'], # 주문자핸번 : "ordPrtblTel"
                "ordererTel": oid['ordTlphnNo'],    # 주문자전번 : "ordTlphnNo"
                "optionsString": oid['slctPrdOptNm'],  # 옵션스트링 : "slctPrdOptNm"
                "paymentStateCode": self.conf['const']['paymentStateCode'], # 결제상태코드 : 고정
                "paymentTypeCode": self.conf['const']['paymentTypeCode'],  # 결제종류 : 고정
            }}
            self.logger.debug(f'call_api: api data = {{pprint.pformat(api_d)}}')
            # call API
            url = self.conf['api']['save_url']
            resp = requests.post(url, json=api_d)
            if resp.status_code // 10 != 20:
                raise RuntimeError(f"call_api: Invalid API response code {{resp.status_code}}, {{resp.text}}")
            rd = json.loads(resp.text)
            # print(resp.text)
            self.logger.info(f'call_api: successfully saved: result={{pprint.pformat(rd)}}')
        except:
            raise

    # ==========================================================================
    def get_order_info(self, ord_no):
        headers = {{
            'openapikey': self.conf['params']['accesskey'],
            'Content-Type': 'text/xml',
        }}
        url = self.API_ORDER_INFO.format(ord_no=ord_no)
        resp = requests.get(url, headers=headers)
        if resp.status_code // 10 != 20:
            raise LookupError(f"get_order_info: Invalid API response code {{resp.status_code}}, {{resp.text}}")
        rd = xmltodict.parse(resp.text)
        rd = rd['ns2:orders']
        rd = rd['ns2:order']
        return rd

    # ==========================================================================
    def get_order_list(self):
        headers = {{
            'openapikey': self.conf['params']['accesskey'],
            'Content-Type': 'text/xml',
        }}
        url = self.API_ORDER_LIST.format(
            start_time=self.conf['params']['start_time'], 
            end_time=self.conf['params']['end_time'])
        resp = requests.get(url, headers=headers)
        if resp.status_code // 10 != 20:
            raise LookupError(f"get_order_list: Invalid API response code {{resp.status_code}}, {{resp.text}}")

        rd = xmltodict.parse(resp.text)
        rd = rd['ns2:orders']
        rd = rd['ns2:order']

        done_cnt = ord_cnt = 0
        for _od in rd:
            ord_cnt += 1
            try:
                od = dict(_od)
                oid = self.get_order_info(od['ordNo'])
                self.call_api(od, oid)
                done_cnt += 1
            except Exception as err:
                self.logger.error(traceback.format_exc())
        self.logger.info(f'get_order_list: succeeded {{done_cnt}} out of total {{ord_cnt}}')
    # ==========================================================================
    def do(self):
        try:
            self.logger.info(f'Starting {{self.__class__.__name__}} ...')
            self.get_order_list()
        except Exception as err:
            self.logger.error(traceback.format_exc())
            raise err
        finally:
            self.logger.info(f'Ended {{self.__class__.__name__}} ...')



################################################################################
def test():
    #yaml_f = '11st.yml'
    yaml_f = '{yaml_f}'
    with Shop11stApi(yaml_f) as s11:
        s11.do()


################################################################################
# if __name__ == '__main__':
test()
