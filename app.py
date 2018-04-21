#!/usr/bin/env python3

import uuid

from flask import Flask, request
from flask_restful import Api, Resource, abort

app = Flask(__name__)
api = Api(app)

class CandidateAccount:

    def __init__(self, type_, name):
        self.type_ = type_
        self.name = name

    def as_dict(self):
        return {
            'type': self.type_,
            'name': self.name,
        }

class Account:

    def __init__(self, type_, **kwargs):
        self.uuid = uuid.uuid1()
        self.type_ = type_
        self.kwargs = kwargs

    def as_dict(self):
        d = {'uuid': str(self.uuid), 'type': self.type_}
        d.update(self.kwargs)

        if 'huabei' in self.kwargs:
            huabei = self.kwargs['huabei']
            d['huabei'] = {'type': huabei.type_}
            d['huabei'].update(huabei.kwargs)

        return d

account_list = [
    Account(type_='CASH', remark='钱包A', balance='976.00'),
    Account(type_='CREDIT_CARD', remark='', bankCardNumber='4237', creditLimit='2000', billDate=1, paymentDate=10, arrears='1234'),
    Account(type_='DEBIT_CARD', remark='', bankCardNumber='669395', balance='6134.77'),
    Account(type_='ALIPAY', remark='', balance='16431.91', yuebao=None, 
        huabei=Account(type_='HUABEI', creditLimit='2000', billDate=1, paymentDate=9, arrears='413.43')),
]
accounts = { str(a.uuid) : a for a in account_list }

print(accounts)

candidate_accounts = [
    CandidateAccount(type_='CASH', name='现金钱包'),
    CandidateAccount(type_='CREDIT_CARD', name='信用卡'),
    CandidateAccount(type_='DEBIT_CARD', name='借记卡'),
    CandidateAccount(type_='ALIPAY', name='支付宝'),
    CandidateAccount(type_='WEIXIN', name='微信钱包'),
    CandidateAccount(type_='CAMPUS_CARD', name='校园卡'),
    CandidateAccount(type_='BUS_CARD', name='公交卡'),
    CandidateAccount(type_='INVESTMENT', name='投资账户'),
]

investmentProjects = {}

class AccountList(Resource):

    def get(self):
        return [a.as_dict() for a in accounts.values()]

    def post(self):
        json_data = request.get_json()
        # TODO validate json data
        type_ = json_data['type']
        del json_data['type']
        account = Account(type_, **json_data)
        accounts[account.uuid] = account
        return account.as_dict(), 201

class Account(Resource):

    def delete(self, id_):
        if not id_ in accounts:
            abort(404, message='Account {} does not exist'.format(id_))
        
        del accounts[id_]
        # XXX workaround: if return 204, the client won't go
        return '', 201

class CandidateAccountList(Resource):

    def get(self):
        return [c.as_dict() for c in candidate_accounts]

class InvestmentProjectList(Resource):

    def get(self):
        return investmentProjects

api.add_resource(AccountList, '/accounts')
api.add_resource(Account, '/accounts/<id_>')
api.add_resource(CandidateAccountList, '/candidate_accounts')
api.add_resource(InvestmentProjectList, '/investment_projects')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
