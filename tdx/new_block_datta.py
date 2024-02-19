import pymongo as mongo
import pandas as pd
import sys

class MongoIo(object):
    """Redis操作类"""
    
    def __init__(self, host='127.0.0.1', port=27017, database='quantaxis'):
        # self.config = self.file2dict(conf)
        client = mongo.MongoClient(host, port)
        self.db = client[database]
        
    def get_day_select_tops(self, ins_day = '2024-02-06', min_nums = 10):
        tblName = 'day-select-ff'
        cursor = self.db[tblName].aggregate( #aggregate_sql)
        [
                { '$match':{                'date':{'$eq': ins_day}            }},
                {            '$group':{
                        '_id': "$code",
                        'funcs': {'$push': '$func'},
                        'sum_score': {'$sum': '$score'}
                }}
                ,{ '$match': { 'sum_score': { '$gte': min_nums }         }}
                ,{ '$sort':{'sum_score':-1} }
        ])
        res = pd.DataFrame([item for item in cursor])
        return res
        # codes2=[]
        # for x in cursor:
        # #     print(x['_id'])
        #     codes2.append(x['_id'])
        # # print(codes2)
        # codes = codes + codes2
        # codes = codes2
    
    def init_blk(self, res, blk):
        with open(r'D:/soft/new_tdx/T0002/blocknew/%s.blk' % blk, 'w') as f:
            f.write("\n")
            for idx,row in res.iterrows():
                flg = 0
                if row['_id'][:1] == '6':
                    flg = 1
                print('%d%s' % (flg, row['_id']))
                f.write('%d%s\n' % (flg, row['_id']))
    
if __name__ == '__main__':
    print('example python.exe .\tdx\new_block_datta.py 2024-02-05 12 ZW3')
    print('argv', sys.argv)
    mg = MongoIo()
    res = mg.get_day_select_tops(sys.argv[1], int(sys.argv[2]))
    # print(res)
    mg.init_blk(res, sys.argv[3])