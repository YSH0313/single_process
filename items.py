# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    cpyz = scrapy.Field()  # 裁判要旨
    doc_id = scrapy.Field()  # 详情id
    province = scrapy.Field()  # 省份',
    sdate = scrapy.Field()  # 审结时间
    procedure = scrapy.Field()  # 审理程序
    status = scrapy.Field()  # 案件状态
    causename = scrapy.Field()  # 案由
    judgeresult = scrapy.Field()  # 判决结果
    yiju = scrapy.Field()  # 依据
    caf = scrapy.Field()  # 案件受理费
    cafperson = scrapy.Field()  # 案件受理费承担人
    updated = scrapy.Field()  # 修改日期
    wslx = scrapy.Field()  # 文书类型
    postTime = scrapy.Field()  # 发布时间
    court = scrapy.Field()  # 法院
    judge = scrapy.Field()  # 审判人员
    pname = scrapy.Field()  # 被告
    b_lawname = scrapy.Field()  # 被告代理人
    lawyer = scrapy.Field()  # 案件相关律师事务所
    pnametext = scrapy.Field()  # 被告描述
    plaintiff = scrapy.Field()  # 原告
    y_lawname = scrapy.Field()  # 原告代理人
    plaintifftext = scrapy.Field()  # 原告描述
    thirdparty = scrapy.Field()  # 第三人
    courtclaims = scrapy.Field()  # 法院主张
    evidence = scrapy.Field()  # 证据
    sortTime = scrapy.Field()  # 裁判日期
    caseType = scrapy.Field()  # 案件类型
    caseNo = scrapy.Field()  # 案号
    caseNo_r = scrapy.Field()  # 关联案号
    title = scrapy.Field()  # 标题
    mydoc_id = scrapy.Field()  # doc_id
    body = scrapy.Field()  # 正文
    detailUrl = scrapy.Field()  # 详情url
    crawlTime = scrapy.Field()  # 采集时间
    MD5 = scrapy.Field()  # md5码
    source = scrapy.Field()  # 来源

class CaipanClosedItem(scrapy.Item):
    title = scrapy.Field()  # '标题
    wslx = scrapy.Field()  # 文书类型
    caseNo = scrapy.Field()  # 案号
    sortTime = scrapy.Field()  # 案号
    posttime = scrapy.Field()  # 发布时间
    court = scrapy.Field()  # 法院
    caseType = scrapy.Field()  # 案件类型
    body = scrapy.Field()  # 正文
    detailUrl = scrapy.Field()  # 详情链接
    crawlTime = scrapy.Field()  # 采集时间
    province = scrapy.Field()  # 省份
    MD5 = scrapy.Field()  # MD5唯一标识
    source = scrapy.Field()  # 来源连接

class AllurlITem(scrapy.Item):
    detailUrl = scrapy.Field()
    title = scrapy.Field()

class KaiTingItem(scrapy.Item):
    source = scrapy.Field()  # 网站来源
    url = scrapy.Field()  # 详情链接
    body = scrapy.Field()  # 正文
    title = scrapy.Field()  # 标题
    court = scrapy.Field()  # 法院
    posttime = scrapy.Field()  # 发布时间
    sorttime = scrapy.Field()  # 开庭时间
    pname = scrapy.Field()  # 被告
    plaintiff = scrapy.Field()  # 原告
    party = scrapy.Field()  # 原告被告文本
    courtNum = scrapy.Field()  # 法庭
    anyou = scrapy.Field()  # 案由
    caseNo = scrapy.Field()  # 案号
    province = scrapy.Field()  # 省份
    organizer = scrapy.Field()  #
    judge = scrapy.Field()  # 审判员
    description = scrapy.Field()  # 描述
    md5 = scrapy.Field()  # body唯一性
    sign = scrapy.Field()
    load_time = scrapy.Field()

class TingShenItem(scrapy.Item):
    kid = scrapy.Field()
    pname = scrapy.Field()
    plaintiff = scrapy.Field()
    party = scrapy.Field()
    anyou = scrapy.Field()

class BaoGuangItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    sortTime = scrapy.Field()  # 立案日期
    posttime = scrapy.Field()  # 发布时间
    bdate = scrapy.Field()  # 曝光日期
    caseNo = scrapy.Field()  # 案号
    body = scrapy.Field()  # 源码
    pname = scrapy.Field()  # 被执行人

    age = scrapy.Field()  # 年龄
    sex = scrapy.Field()  # 性别
    partyType = scrapy.Field()  # 被执行人类型
    CERNO = scrapy.Field()  # 证件号（身份证号/组织机构代码）
    CERTYPE = scrapy.Field()  # 证件类型
    faren = scrapy.Field()  # 法定代表人
    address = scrapy.Field()  # 地址
    proposer = scrapy.Field()  # 申请人
    cause = scrapy.Field()  # 案由
    casecause = scrapy.Field()  # 曝光原因
    yjdw = scrapy.Field()  # 做出执行依据单位
    court = scrapy.Field()  # 法院
    yiju = scrapy.Field()  # 依据
    status = scrapy.Field()  # 执行状态
    exemoney = scrapy.Field()  # 标的金额
    unexemoney = scrapy.Field()  # 未执行金额
    url = scrapy.Field()  # 原始链接
    source = scrapy.Field()  # 来源连接
    gettime = scrapy.Field()  # 采集时间
    MD5 = scrapy.Field()  # md5唯一标识


class ShinXinItem(scrapy.Item):
    sid = scrapy.Field()
    title = scrapy.Field()  # 标题
    pname = scrapy.Field()  # 被执行人姓名/名称
    caseNo = scrapy.Field()  # 案件编号
    age = scrapy.Field()  # 年龄
    sex = scrapy.Field()  # 性别
    cardNum = scrapy.Field()  # 身份证号码/组织机构代码
    court = scrapy.Field()  # 执行法院
    province = scrapy.Field()  # 省份
    caseNo_r = scrapy.Field()  # 执行依据文号
    sorttime = scrapy.Field()  # 立案时间
    reg = scrapy.Field()  # 做出执行依据单位
    duty = scrapy.Field()  # 生效法律文书确定义务
    performance = scrapy.Field()  # 履行情况
    fulfilled = scrapy.Field()  # 已履行
    fulfilled_no = scrapy.Field()  # 未履行
    disrupt = scrapy.Field()  # 失信被执行人行为具体情形
    ptime = scrapy.Field()  # 发布时间
    posttype = scrapy.Field()  # 被执行人公布类型
    lstatus = scrapy.Field()  # 诉讼地位
    personname = scrapy.Field()  # 法人姓名
    casestatus = scrapy.Field()  # 案件状态
    subject = scrapy.Field()  # 标的
    url = scrapy.Field()  # 原始链接
    source = scrapy.Field()  # 来源
    load_time = scrapy.Field()  # 落地时间
    md5 = scrapy.Field()  # md5唯一标识
    json = scrapy.Field()  # body
    remarks = scrapy.Field()  # body
    

class beizhixing(scrapy.Item):
    thirdParty = scrapy.Field()  # 第三人
    caseCause = scrapy.Field()  # 案由
    postTime = scrapy.Field()  # 信息发布时间
    representativeNo = scrapy.Field()  # 法定代表人身份证号
    legalRepresentativ = scrapy.Field()  # 法定代表人
    yjdw = scrapy.Field()  # 作出执行依据单位
    yjCode = scrapy.Field()  # 执行依据文号
    title = scrapy.Field()  # 案件标题
    sortTime = scrapy.Field()  # 立案时间
    end_time = scrapy.Field()  # 结案时间
    out_time = scrapy.Field()  # 移出时间
    proposer = scrapy.Field()  # 申请执行人
    pname = scrapy.Field()  # 被执行人姓名/名称
    sex = scrapy.Field()  # 性别
    partyType = scrapy.Field()  # 当事人/被执行人类型
    idcardNo = scrapy.Field()  # 身份证/组织机构代码
    focusNumbe = scrapy.Field()  # 关注次数
    district = scrapy.Field()  # 地区
    caseNo = scrapy.Field()  # 案号
    execMoney = scrapy.Field()  # 执行标的
    court = scrapy.Field()  # 执行法院
    caseState = scrapy.Field()  # 案件状态
    body = scrapy.Field()  # 源码/正文
    loadTime = scrapy.Field()  # 采集时间
    url = scrapy.Field()  # 详情url
    source = scrapy.Field()  # 网站链接

class zbaj(scrapy.Item):
    body = scrapy.Field()  # 正文
    pid = scrapy.Field()  # id规律
    title = scrapy.Field()  # 标题
    pname = scrapy.Field()  # 当事人
    sex = scrapy.Field()  # 性别
    address = scrapy.Field()  # 地址
    court = scrapy.Field()  # 执行法院
    caseNo = scrapy.Field()  # 案号
    postTime = scrapy.Field()  # 发布时间
    lianTime = scrapy.Field()  # 立案时间
    anyou = scrapy.Field()  # 案件案由
    anyouzb = scrapy.Field()  # 终本案由
    sortTime = scrapy.Field()  # 终本时间
    execMoney = scrapy.Field()  # 执行标的
    unnexeMoney = scrapy.Field()  # 未履行金额
    idcardNo = scrapy.Field()  # 身份证/组织机构代码
    url = scrapy.Field()  # 详情页
    source = scrapy.Field()  # 网站来源
    loadtime = scrapy.Field()  # 采集时间
    MD5 = scrapy.Field()  # md5唯一标识