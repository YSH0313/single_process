# -*- coding: utf-8 -*-

# Define here the models for your scraped items


class SingleItem(object):
    log_info = None

    def dict(self):
        __dict = dict()
        for k, v in self.__dict__.items():
            if v:
                if isinstance(v, ApprovalInfo):
                    __dict[k] = v.app()
                else:
                    __dict[k] = v
        return __dict


class BiddingItem(SingleItem):
    def __init__(self):
        self.title = None  # 必填
        self.pub_time = None  # 必填
        self.url = None  # 必填
        self.show_url = None
        self.source = None  # 必填
        self.html = None  # 必填
        self.caller = None
        self.winner = None
        self.winner_amount = None
        self.caller_amount = None
        self.data = None
        self.notice_type = None  # 标书类型  预招标公告、更正公告、废标公告、中标公告、招标公告、非招投标
        self.url_not_filter = None  # True/False True:中间层用,不存储url的MD5，只进行html过滤


approval_list = []


class ApprovalInfo():
    def __init__(self):
        self.agency = None
        self.time = None
        self.result = None
        self.detail = None
        self.code = None

    def app(self):
        self.approval = {
            'agency': self.agency,
            'time': self.time,
            'result': self.result,
            'detail': self.detail,
            'code': self.code
        }
        approval_list.append(self.approval)
        return approval_list


class ProposedItem(SingleItem):
    def __init__(self, _obj=None):
        # ------- 拟建项目字段 - -------
        self.project_type = None  # 项目类型
        self.project_code = None  # 项目编号
        self.project_name = None  # 项目名称
        self.project_status = None  # 项目状态
        self.project_detail = None  # 项目描述
        self.pub_time = None  # 时间
        self.province = None  # 省
        self.city = None  # 市
        self.county = None  # 县
        self.caller = None  # 业主单位
        self.contact = None  # 联系人
        self.phone = None  # 联系人电话
        self.approval_info: list = []  # 审批信息
        # self.approval_info: list = [{
        #     'agency': None,  # 审批部门
        #     'time': None,  # 审批时间
        #     'result': None,  # 审批结果
        #     'detail': None,  # 审批事项
        #     'code': None  # 批复文号
        # }]  # 审批信息
        self.trade = None  # 行业
        self.money = None  # 项目总投资
        self.content = None  # 正文
        self.content_ext = None  # 解析正文
        self.url = None  # 原文链接
        self.show_url = None  # 原文链接
        self.file_url = None  # 文件链接
        self.source = None  # 来源
        if _obj:
            d = self.__dict__.copy()
            d.update(_obj)
            self.__dict__ = d
