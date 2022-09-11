# Краткое описание функционала:
# 1. Создание картинок дипломов на основании шаблонов и параметров
# 2. Выгрузка полученных файлов в IPFS
# 3. Передача всей необходимой информации в смарт-контракт
# 4. Отправка писем на почту студентам с дипломами

from web3 import Web3
import json
from PIL import Image, ImageDraw, ImageFont
import ipfsApi
import smtplib
import textwrap

from config import API_KEY_ALCHEMY
from config import PRIVATE_KEY_WALLET
from config import PASSWORD_MAIL

api_key_alchemy = API_KEY_ALCHEMY
private_key_wallet = PRIVATE_KEY_WALLET
password_mail = PASSWORD_MAIL

# 1. Создаем файл диплома на основании шаблона и параметров
# - Определение параметров, которые могут передаваться в фронтэнда или из любого другого источника.
#   для примера используем список словарей с двумя элементами
MyList = [
    {
        'DirTemplate': "D:\Hackathon\Template.jpg",
        'Heaader': "ДИПЛОМ",
        'Student': "Сальников Данил Сергеевич",
        'Number': 51,
        'course': "Blockchain Developer: разработка смарт-контрактов на Solidity",
        'Date': "2022",
        'mail': "cashriver@rambler.ru",
    },
    {
        'DirTemplate': "D:\Hackathon\Template.jpg",
        'Heaader': "ДИПЛОМ",
        'Student': "Малхосян Игорь Андреевич",
        'Number': 52,
        'course': "Blockchain Developer: разработка смарт-контрактов на Solidity",
        'Date': "2022",
        'mail': "keepcalmcryptotrader@gmail.com",
    }
]

# определение параметров смарт-контракта
contract_address = '0xE3Af4f8C59c9bdC2B39522dee81f638964cCe841'
owner = '0x900292f80220e438623FB964422808Bc3091430E'
# ABI от смарт контракта с etherscan.io
ABI = json.loads('''[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"indexed":false,"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"TransferBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"TransferSingle","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"value","type":"string"},{"indexed":true,"internalType":"uint256","name":"id","type":"uint256"}],"name":"URI","type":"event"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"accounts","type":"address[]"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"}],"name":"balanceOfBatch","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_ids","type":"uint256[]"},{"internalType":"uint256[]","name":"_amounts","type":"uint256[]"}],"name":"burnBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint256[]","name":"_burnIds","type":"uint256[]"},{"internalType":"uint256[]","name":"_burnAmounts","type":"uint256[]"},{"internalType":"uint256[]","name":"_mintIds","type":"uint256[]"},{"internalType":"uint256[]","name":"_mintAmounts","type":"uint256[]"}],"name":"burnForMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"string","name":"_uri","type":"string"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256[]","name":"_ids","type":"uint256[]"},{"internalType":"uint256[]","name":"_amounts","type":"uint256[]"}],"name":"mintBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeBatchTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"},{"internalType":"string","name":"_uri","type":"string"}],"name":"setURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_id","type":"uint256"}],"name":"uri","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]''')
# инициализация контракта
web3 = Web3(Web3.HTTPProvider(f"https://eth-goerli.g.alchemy.com/v2/{api_key_alchemy}"));
contract = web3.eth.contract(contract_address, abi=ABI)
nonce = web3.eth.getTransactionCount(owner)
# определение параметров и авторизация на почтовом клиенте
email_from = 'GenderParty0611@yandex.ru'
server_mail = smtplib.SMTP('smtp.yandex.ru', 587)
subject = 'Поздравляем с получением диплома!'
server_mail.starttls()
server_mail.login(email_from, password_mail)
index = 0
list = []
# Обходим список и по каждому формируем файл диплома
for x in MyList:

    DirTemplate = x.get("DirTemplate")
    image = Image.open(DirTemplate)

    drawer = ImageDraw.Draw(image)
    drawer.text((340, 550), x.get("Heaader"), font=ImageFont.truetype("lucon.ttf", 150), fill='white')

    # расчет центра области картинки
    W, H = 1240, 1754
    centr = ImageFont.truetype("lucon.ttf", 40).getbbox(x.get("Student"))[2]
    drawer.text(((W - centr) / 2, 775), x.get("Student"), font=ImageFont.truetype("lucon.ttf", 40), fill="white")

    # разбиение длинного текста на строки
    offset = 0
    text = x.get("course")
    for line in textwrap.wrap(text, width=32):
        drawer.text((350, 920 + offset), line, font=ImageFont.truetype("lucon.ttf", 25), fill="white")
        offset += 25

    drawer.text((290, 1100), x.get("Date"), font=ImageFont.truetype("lucon.ttf", 270), fill='white')

    # можно координаты расположения текстов, шрифты и их размеры так же получать из вне.
    # Например из фрондэнд графичиеского редактора, тогда и сами параметры проще обезличить и передавать их в JSON как:
    # [
    #     {
    #         'value': "Text",
    #         "position": {
    #                 "x": 100,
    #                 "y": 200
    #
    #             }
    #          "font": "arial.ttf"
    #          "size": 60
    # }],
    # но сейчас это не фокусная задача

    FileName = f'D:\Hackathon\diplom{x.get("Number")}.jpg'
    image.save(FileName)

    # 2. Выгружаем файл в IPFS и получаем ссылку, клиент IPFS должен быть запущен на сервере
    api = ipfsApi.Client(host='http://127.0.0.1', port=5001)
    CID = api.add(FileName)['Hash']
    ipfs_link = "https://ipfs.io/ipfs/" + CID
    print(ipfs_link)

    # 3. Передааем инфу в смарт контракт
    # Отправляем дипломы в блокчейн

    dict_transaction = {
        'chainId': web3.eth.chain_id,
        'from': owner,
        'value': 0,
        'gasPrice': round(web3.eth.gas_price*1.1),
        'nonce': nonce + index,
    }
    index = index + 1
    try:
        # Создаем
        transaction = contract.functions.mint(owner, x.get("Number"), 1, ipfs_link).buildTransaction(dict_transaction)
        # Подписываем
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key_wallet)
        # Отправляем
        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction).hex()
        link_transaction = f'https://goerli.etherscan.io/tx/{txn_hash}'
        print(link_transaction)

        # 4. Отправляем письмо на почту с дипломом. Так же легко можно добавить и одно общее письмо в конце с отчетом вледельцу
        to_email = x.get("mail")
        email_text = f'Поздравляем с успешным прохождением курса и получением диплома!\nСсылка на ваш диплом: {ipfs_link}\nСсылка на транзакцию в блокчейне: {link_transaction}'
        message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (email_from, to_email, subject, email_text)
        server_mail.sendmail(email_from, to_email, message.encode('utf-8'))

        list.append({'id_student':x.get("Number"), 'ipfs_link':ipfs_link, 'link_transaction':link_transaction})
    except Exception as err:
        print(err)
# Показываем последний сформированный диплом для теста
image.show()
# Закрываем соединение с почтой
server_mail.quit()

# 5. Возвращать ссылки и ИД вызывающей стороне
# Пока реализую через сохранение в JSON файл, но ни чего не мешает в дальнейшем переделать это на http-запрос для любого сервиса
response = json.dumps(list)
print(response)
