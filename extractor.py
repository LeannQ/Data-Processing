import re


'''
    Extract information by regular expression.
'''


# Information needed
KEYS = [
    '姓名',
    '身份证号',
    '联系地址',
    '邮编',
    '开户银行（填写到支行）',
    '银行账号',
    '联系电话（手机）',
    '联系电话（座机）',
    '邮箱或QQ',
]


def clean(text):
    chars = [' ', '　', '    ']
    for i in chars:
        text = text.replace(i, '')
    return text


def deep_clean(text):
    text = clean(text)
    chars = ['\n', '\r\n']
    for i in chars:
        text = text.replace(i, '')
    return text


def match_or_null(pat, text):
    res = re.search(pat, text)
    if res:
        return res.group()
    return ''


def priority_match(pats, text):
    assert isinstance(pats, list)
    for pat in pats:
        res = match_or_null(pat, text)
        if res:
            return res
    return ''


def get_signature(text):
    pat = re.compile(r'本人签名[：；:]?(.*?)签订时间', re.S)
    finds = re.findall(pat, text)
    if len(finds):
        signature = finds[0]
        signature = signature.strip(' ')
        if signature and signature[0] in ['：', '；', ':', ';']:
            signature = signature[1:]
        return signature
    else:
        return ''


def get_id_num(text):
    pat = re.compile(r'身份证号[：；:]?\d{14,18}[a-zA-Z]?', re.S)
    res = match_or_null(pat, text)
    if res:
        id_num = res[5:23]
        return id_num
    else:
        return ''


def get_postal_num(text):
    pat = re.compile(r'邮编[：；:]?(\d{4,8})', re.S)
    finds = re.findall(pat, text)
    if len(finds):
        postal_num = finds[0]
        return postal_num
    else:
        return ''


def get_addr(text):
    pat = re.compile(r'联系地址[：；:]?(.*?)(邮编|开户银行)', re.S)
    finds = re.findall(pat, text)
    if len(finds):
        addr = finds[0][0]
        addr = addr.strip(' ')
        if addr[-1] == '（' or addr[-1] == '(':
            addr = addr[:-1]
            
        return addr
    else:
        return ''


def get_bank_id(text):
    pat = re.compile(r'银行账号[：；:]?(\d{6,30})', re.S)
    finds = re.findall(pat, text)
    if len(finds):
        bank_id = finds[0]
        return bank_id
    else:
        return ''


def get_bank_name(text):
    pat1 = re.compile('开户银行（填写到支行）[：；:]?(.*?)银行账号', re.S)
    pat2 = re.compile('开户银行[：；:]?(.*?)银行账号', re.S)
    pats = [pat1, pat2]
    find = priority_match(pats, text)
    if find:
        pat3 = re.compile('[：；:](.*?)银行账号', re.S)
        res = re.findall(pat3, find)
        if len(res):
            return res[0]
    return ''


def get_phone_num(text):
    cellphone = ''
    telephone = ''
    pat1 = re.compile(r'联系电话.*?邮箱', re.S)
    pat2 = re.compile(r'联系电话.*?座机', re.S)
    pat3 = re.compile(r'联系电话.*?手机', re.S)
    pats = [pat1, pat2, pat3]
    res = priority_match(pats, text)
    if res:
        pat = re.compile(r'[\d-]{7,20}', re.S)
        finds = re.findall(pat, deep_clean(res))
        if len(finds):
            cellphone = finds[0]
            if len(finds) > 1:
                telephone = finds[1]
    return cellphone, telephone


def get_email(text):
    pat = re.compile(r'[a-zA-Z0-9._-]{0,30}@[a-zA-Z0-9._-]+?\.[a-zA-Z0-9._-]+', re.S)
    text = deep_clean(text)
    return match_or_null(pat, text)


def get_meta(text):
    vs = [''] * len(KEYS)
    meta = dict(zip(KEYS, vs))
    text_clean = clean(text)

    # signature
    signature = get_signature(text_clean)
    meta['姓名'] = signature

    # id number
    id_num = get_id_num(text_clean)
    meta['身份证号'] = id_num

    # postal number
    postal_num = get_postal_num(text_clean)
    meta['邮编'] = postal_num

    # addr
    addr = get_addr(text_clean)
    addr = addr.strip(' ')
    meta['联系地址'] = addr

    # bank id
    bank_id = get_bank_id(text_clean)
    meta['银行账号'] = bank_id

    # bank name
    bank_name = get_bank_name(text_clean)
    meta['开户银行（填写到支行）'] = bank_name

    # phone num
    cellphone, telephone = get_phone_num(text_clean)
    meta['联系电话（手机）'] = cellphone
    meta['联系电话（座机）'] = telephone

    # email
    email = get_email(text_clean)
    meta['邮箱或QQ'] = email

    return meta


def count_not_null(dct):
    count = 0
    for i in list(dct.values()):
        if i:
            count += 1
    return count


def get_meta_best_match(obj):
    if isinstance(obj, str):
        return get_meta(obj)
    elif isinstance(obj, list):
        text_li = obj
        metas = [get_meta(i) for i in text_li]
        counts = [count_not_null(i) for i in metas]
        return metas[counts.index(max(counts))]


if __name__ == '__main__':
    pass
