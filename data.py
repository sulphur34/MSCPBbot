import datetime
import json
import os


class RequestData:

    def __init__(self):
        self.contract_requests_list = dict()
        self.explanation_request_list = dict()
        self.filepath = os.path.join(os.getcwd(), 'contract_request.json')

    def get_request_list(self):
        with open(self.filepath, 'r') as jsonfile:
            data = json.load(jsonfile)
            return data
            print(data, type(data))


    def write_param(self, update, param_name):
        request_id = f'ch{update.effective_chat.id}us{update.effective_user.id}msg{update.callback_query.message.id}'
        if request_id in self.contract_requests_list:
            self.contract_requests_list[request_id][param_name] = update.callback_query.data
        else:
            self.contract_requests_list = dict()
            self.contract_requests_list[request_id] = {}
            self.contract_requests_list[request_id]['Datetime'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            self.contract_requests_list[request_id][param_name] = update.callback_query.data

    def get_requested_contract(self, request_id):
        with open(self.filepath, 'r') as jsonfile:
            data = json.load(jsonfile)

    def save_request(self):
        if self.contract_requests_list is None:
            return
        with open(self.filepath, 'w') as jsonfile:
            # columns = ['request_id', 'contract_type', 'contract_subject', 'counterpart_type', 'payment_system',
            #            'edo_presence', 'contract_link']
            # jdata = json.dumps(self.contract_requests_list)
            if os.path.getsize(self.filepath) > 0:
                data = self.get_request_list()
                if type(data) is dict:
                    data.update(self.contract_requests_list)
                    json.dump(data, jsonfile)
            else:
                json.dump(dict(self.contract_requests_list), jsonfile)


# class ContractRequest:
#
#     def __init__(self, request_id):
#         self.request_id = request_id
#         self.contract_type = None
#         self.contract_subject = None
#         self.counterpart_type = None
#         self.payment_system = None
#         self.edo_presence = None
#         self.contract_link = None
#
#     def write_param(self, param_type, param_value):
#
#     def get_request(self, source_file_path, request_id):
#         with open(source_file_path, 'r', newline=' ') as csvfile:
#
#     def add_request_to_file(self, source_file_path):
#         with open(source_file_path, 'a', newline=' ') as csvfile:
#             columns = ['request_id', 'contract_type', 'contract_subject', 'counterpart_type', 'payment_system',
#                        'edo_presence', 'contract_link']
#             writer = csv.DictWriter(csvfile, fieldnames=columns)

# doc_code = {
#     'supply': False,
#     'subcontract': False,
#     'services': False,
#     'profit': False,
#     'expenses': False,
#     'NDS': False,
#     'nonNDS': False,
#     'individual': False,
#     'unknown': False,
#     'prepay': False,
#     'postpay': False,
#     'EDOpresent': False,
#     'EDOabsent': False
# }
