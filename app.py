#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource

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

accounts = [
    {'a': 1},
    {'b': 2},
    {'c': 3},
]

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
        return accounts

class CandidateAccountList(Resource):

    def get(self):
        return [c.as_dict() for c in candidate_accounts]

class InvestmentProjectList(Resource):

    def get(self):
        return investmentProjects

api.add_resource(AccountList, '/accounts')
api.add_resource(CandidateAccountList, '/candidate_accounts')
api.add_resource(InvestmentProjectList, '/investment_projects')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
