from flask import Flask, request
from flask_restful import Resource, Api
from getData import getData

app = Flask(__name__)
api = Api(app)

# TODO: write some tests for my api
class LeaderBoardData(Resource):
    def get(self,comp,year):
        # TODO: set up correct defaults
        event_num = request.args.get('eventNum') if request.args.get('eventNum') else 0
        division = request.args.get('division') if request.args.get('division') else 1
        pages = request.args.get('pages') if request.args.get('pages') else 2
        return {'data': getData(comp,year,division,event_num,pages)}

api.add_resource(LeaderBoardData, '/<string:comp>/<int:year>/')

if __name__ == '__main__':
    app.run(debug=True)