import json
from flask import Flask

class SimpleObject(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return {key:value for key, value in obj.__dict__.items() if not key.startswith("_")}
        return super().default(obj)    
        
# app = Flask(__name__)

# blockchain = b

# @app.route('/chain', methods=['GET'])
# def get_chain():
#     chain_data = []
#     for block in blockchain.chain:
#         chain_data.append(block.__dict__)
#     return json.dumps({"length": len(chain_data),
#                        "chain": chain_data}, cls = SimpleObject, indent=4)

# app.run(debug=True, port=5000)