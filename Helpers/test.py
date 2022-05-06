from blockchain import Blockchain


Users = Blockchain()

Users.createNewBlock()
Users.addTransactionToPendingTransaction(
    {"name": "Waris", "email": "waris@gmail.com"})
Users.addTransactionToPendingTransaction(
    {"name": "PARITOSH", "email": "Fairy@gmail.com"})
Users.createNewBlock()

print(Users.chain)

# previousBlockHash = "wSGR#$@DNDN"
# currentBlockData = [{"name": "waris sharma"}]

# print(Users.hashBlock(previousBlockHash, currentBlockData,
#       Users.proofOfWork(previousBlockHash, currentBlockData)))

# print(Users.hashBlock("000087985248cb89c29e93af0bd55ebb7b659bcea8f96ace46060b27fdc95330",[
#                 {
#                     "name": "Paritosh Chauhan",
#                     "email": "paritosh@gmail.com",
#                     "transactionId": "f71133ec7ad5498ab7d63795472d297a",
#                 },
#             ],11))
# bc1 = {
#     "chain": [
#         {
#             "index": 1,
#             "timestamp": 1640712588644,
#             "transactions": [],
#             "nonce": 80440,
#             "hash": "00009d00c7c92542eee659cd485b2059f2545bb6a7b1fa161303c40828317f2c",
#             "previousBlockHash":
#             "000087985248cb89c29e93af0bd55ebb7b659bcea8f96ace46060b27fdc95330",
#         },
#         {
#             "index": 2,
#             "timestamp": 1640712649614,
#             "transactions": [
#                 {
#                     "name": "Paritosh Chauhan",
#                     "email": "paritosh@gmail.com",
#                     "transactionId": "f71133ec7ad5498ab7d63795472d297a",
#                 },
#             ],
#             "nonce": 28479,
#             "hash": "00009edec6a09cc90f3d62427a2d3d7aefa79c83420e7f7dc8052fb0c53fc348",
#             "previousBlockHash":
#             "00009d00c7c92542eee659cd485b2059f2545bb6a7b1fa161303c40828317f2c",
#         },
#         {
#             "index": 3,
#             "timestamp": 1640712739591,
#             "transactions": [
#                 {
#                     "amount": 12.5,
#                     "sendAddr": "00",
#                     "recAddr": "9a3437074b634dbdb8f61a65bba0b6af",
#                     "transactionId": "b9eb1f5f1dc4417a9e5f00ba1fbf654e",
#                 },
#                 {
#                     "name": "Waris Sharma",
#                     "email": "waris@gmail.com",
#                     "transactionId": "b28756bf290144f3b51190069fb25d65",
#                 },
#                 {
#                     "name": "Anirudh Kaushal",
#                     "email": "anirudh@gmail.com",
#                     "transactionId": "691576cd27fa4b8aa4b452aa2eefc504",
#                 },
#                 {
#                     "name": "Rounak Aggarwal",
#                     "email": "rounak@gmail.com",
#                     "transactionId": "0eb79d3d663b4e93b6063beb0e8740ed",
#                 },
#             ],
#             "nonce": 6062,
#             "hash": "0000aff9334ab205a91a6262eccf602692aebfc209fd19e83738f0fd781cfa3f",
#             "previousBlockHash":
#             "00009edec6a09cc90f3d62427a2d3d7aefa79c83420e7f7dc8052fb0c53fc348",
#         },
#         {
#             "index": 4,
#             "timestamp": 1640712779953,
#             "transactions": [
#                 {
#                     "amount": 12.5,
#                     "sendAddr": "00",
#                     "recAddr": "9a3437074b634dbdb8f61a65bba0b6af",
#                     "transactionId": "fe9859a755b449c99d53a0b5e6fe4b15",
#                 },
#                 {
#                     "name": "Chiru",
#                     "email": "chiru@gmail.com",
#                     "transactionId": "d7b08172af2646b2a5bdfb25fd09bb7e",
#                 },
#                 {
#                     "name": "Aakash",
#                     "email": "aakash@gmail.com",
#                     "transactionId": "9572e123280441bc899cee67a10e4ad0",
#                 },
#             ],
#             "nonce": 72772,
#             "hash": "0000949160853eae79af1fd31bc98f0a074a4b22655dbf4afa83ff4c13d71453",
#             "previousBlockHash":
#             "0000aff9334ab205a91a6262eccf602692aebfc209fd19e83738f0fd781cfa3f",
#         },
#         {
#             "index": 5,
#             "timestamp": 1640712860545,
#             "transactions": [
#                 {
#                     "amount": 12.5,
#                     "sendAddr": "00",
#                     "recAddr": "9a3437074b634dbdb8f61a65bba0b6af",
#                     "transactionId": "8f6a530f75aa4794a287c0406774603b",
#                 },
#             ],
#             "nonce": 55774,
#             "hash": "0000b4394d7f9707bd156a2087c8bd7e45939b7d6dcf94fd9e19b95e765ff1ff",
#             "previousBlockHash":
#             "0000949160853eae79af1fd31bc98f0a074a4b22655dbf4afa83ff4c13d71453",
#         },
#         {
#             "index": 6,
#             "timestamp": 1640712864323,
#             "transactions": [
#                 {
#                     "amount": 12.5,
#                     "sendAddr": "00",
#                     "recAddr": "9a3437074b634dbdb8f61a65bba0b6af",
#                     "transactionId": "d6de2a8989624e36b460866dd75c069e",
#                 },
#             ],
#             "nonce": 200090,
#             "hash": "0000503f9d8504794c60ff47798d9a7c291994478f33b680cf3e4742a5ab7c50",
#             "previousBlockHash":
#             "0000b4394d7f9707bd156a2087c8bd7e45939b7d6dcf94fd9e19b95e765ff1ff",
#         },
#     ],
#     "pendingTransactions": [
#         {
#             "amount": 12.5,
#             "sendAddr": "00",
#             "recAddr": "9a3437074b634dbdb8f61a65bba0b6af",
#             "transactionId": "ef54181e64a8426797bb6463fef0daf7",
#         },
#     ],
#     "currentNodeURL": "http://localhost:3001",
#     "networkNodes": [],
# }

print("Valid : ", Users.chainIsValid(Users.chain))
