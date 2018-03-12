#!/usr/bin/env python3

from flask import Flask
from flask.ext.restful import Api, Resource

app = Flask(__name__)
api = Api(app)

accounts = {}

investmentProjects = {}

class AccountList(Resource):

    def get(self):
        return accounts

class InvestmentProjectList(Resource):

    def get(self):
        return investmentProjects

api.add_resource(AccountList, '/accounts')
api.add_resource(InvestmentProjectList, '/investment_projects')



if __name__ == '__main__':
    app.run(host='0.0.0.0')
