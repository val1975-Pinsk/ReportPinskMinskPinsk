class Report:
	def __init__(self, reportData):
		self.body = reportData

	def convertDate(self, date):
		month = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
		subDate = date.split("-")
		return subDate[2] + " " + month[int(subDate[1]) - 1] + " " + subDate[0]
	
	def createHeader(self, string):
		if "Пинск" in string.string:
			headerPice = string.spliting(", ")
			print("Дата отчёта: " + self.convertDate(headerPice[0]))
			print("Время отправления: " + headerPice[1])
			print("Направление: " + headerPice[2])
		if "свободно" in string.string:
			headerPice = string.spliting(", ")
			occupied = headerPice[0].split(" ")[0]
			freely = headerPice[1].split(" ")[0]
			print("Автомобиль: " + headerPice[2])
			print("----------------------------------------")
			print("Занято: " + occupied)
			print("Свободно: " + freely)
			print("========================================")
			
			
	def create(self):
		fullyPrice = 0
		discounted = 0
		halfTheCost = 0
		print("ОТЧЁТ" + "\n" + "========================================")
		i = 0
		while(i < len(self.body)):
			if isinstance (self.body[i], ReportStr):
				if self.body[i].header:
					fullyPrice = 0
					discounted = 0
					halfTheCost = 0
					self.createHeader(self.body[i])
				
			if isinstance (self.body[i], ReportCount):
				if self.body[i].status:
					
			i += 1

class ReportStr:
	def __init__(self, string, header = False):
		self.string = string.strip()
		self.header = header
	
	def spliting(self, delimeter):
		return self.string.split(delimeter)
		
	def getDataFromString(self):
		self.string = self.string[16:len(self.string)-5]
		
	def getStringValue(self):
		return self.string
	
class ReportCount:
	def __init__(self, string):
		self.count = string.strip()
		self.status = False	
		
	def getStringValue(self):
		return self.count
		
	def getDataFromString(self):	
		self.count = self.count[17:len(self.count)-5]


def getReportData():
	myFile = "/home/valentin/Report/Водители.txt"
	with open(myFile, encoding = "utf8") as file:
		text = file.readlines()
	i = 0
	data = []
	count = ""
	while(i < len(text)):
		if "Пинск" in text[i]:
			data.append(ReportStr(text[i], True))
			data[len(data) - 1].getDataFromString()
		elif "свободно" in text[i]:
			data.append(ReportStr(text[i], True))
			data[len(data) - 1].getDataFromString()
		elif "width=\"25px\"" in text[i]:
			data.append(ReportCount(text[i]))
			data[len(data) - 1].getDataFromString()
		elif "selected=\"\">Поехал" in text[i]:
			data[len(data) - 1].status = True
		elif "td colspan=\"5\"" in text[i]:
			if not "</tr>" in text[i]:
				data.append(ReportStr(text[i], True))
				data[len(data) - 1].getDataFromString()
		i += 1
	return data
'''
	25.04.24
    Изменения.
    Начало блока.
'''
def match(template):
	words = ["17р", "дк", "Д.К.", "Д к ", "Дк", "свободно", "Пинск"]
	for word in words:
        	if word in template:
        		return True
	return False

'''
    Функция формирует заголовок отчёта по направлениям, доблавляет в отчёт и
    возвращет уже обновлённый отчёт.
'''
def createHeader(report, headLines):
	subStr_0 = headLines[0].split(", ")
	subStr_1 = headLines[1].split(", ")
	subStr_1_0 = subStr_1[0].split(" ")
	subStr_1_1 = subStr_1[1].split(" ")	
	occupied = subStr_1_0[0]		#Занято
	freely = subStr_1_1[0]			#Свободно
	report.append("")
	report.append("Дата отчёта: " + convertDate(subStr_0[0]))
	report.append("Время отправления: " + subStr_0[1])
	report.append("Направление: " + subStr_0[2])
	report.append("Автомобиль: " + subStr_1[2])
	report.append("----------------------------------------")
	report.append("Занято: " + occupied)
	report.append("Свободно: " + freely)
	report.append("========================================")
	return report

def createBody(report, fullyPrice,  discounted, halfTheCost):
	fullyPriceCash = fullyPrice[0] * fullyPrice[1]
	discountedCash = discounted[0] * discounted[1]
	halfTheCostCash = halfTheCost[0] * halfTheCost[1]
	report.append(f"Стоимость: {fullyPrice[0]}p. человек: {fullyPrice[1]} на сумму: {fullyPriceCash} рублей.")
	report.append(f"Стоимость: {discounted[0]}p. человек: {discounted[1]} на сумму: {discountedCash} рублей.")
	report.append(f"Стоимость: {halfTheCost[0]}p. человек: {halfTheCost[1]} на сумму: {halfTheCostCash} рублей.")
	totalCash = fullyPriceCash + discountedCash + halfTheCostCash
	report.append("----------------------------------------")
	report.append(f"Итого на сумму: {totalCash} рублей.")
	report.append("========================================")
	return report
	
'''
	Получение кода оплаты:
		0 - полная стоимось;
		1 - дисконт;
		2 - пол стоимости.
  с 25.04.24 не ипользуется.
'''
def getPrice(str_):
	#print("From getPayCode...")
	#print("str_: " + str_)
	i = 0
	while i < len(str_):
		if "дк" in str_ or "Дк" in str_:
	#		print("30p")
			return 30
		elif "17р" in str_:
	#		print("17р")
			return 17
		i += 1
	#print("35p")
	return 35
	
def create(data):
	i = 0
	#body = False Версия до 25.04.24
	report = ["ОТЧЁТ", "========================================"]
	discounted = [30, 0]
	fullyPrice = [35, 0]
	halfTheCost = [17, 0]
	while i < len(data):
		#if "Заголовок" in data[i]: Версия до 25.04.24
		if "Пинск" in data[i]:
			if halfTheCost[1] + discounted[1] + fullyPrice[1] != 0:
				report = createBody(report, fullyPrice,  discounted, halfTheCost)
			discounted[1] = 0
			fullyPrice[1] = 0
			halfTheCost[1] = 0
			#body = False Версия до 25.04.24
			headLines = [data[i], data[i+1]]
			#i += 1 Версия до 25.04.24
			'''
				25.04.24
			    Правка.
			Функция не возвращала результат.
			После правки возвращает. Так понятней действие функции.
			'''
			report = createHeader(report, headLines)
		'''
		Версия до 25.04.24
		
		if "Тело" in data[i]: 
			body = True
		if body == True and "Тело" not in data[i]:
			price = getPrice(data[i])
			if price == 35:
				fullyPrice[1] += 1
			elif price == 30:
				discounted[1] += 1
			else: halfTheCost[1] += 1'''
		if "Мест" in data[i]:
			if i == len(data)-1:
				q = int(data[i].split(" ")[1])
				fullyPrice[1] += 1
				report = createBody(report, fullyPrice,  discounted, halfTheCost)
				return report
			if "дк" in data[i+1]:
				#    Для наглядности...
				# data[i] = "Мест 1"
				# data[i+1] = "+дк 2731*"
				q = int(data[i].split(" ")[1])
				discounted[1] += q
			if "Дк" in data[i+1]:
				q = int(data[i].split(" ")[1])
				discounted[1] += q
			if "Д.К." in data[i+1]:
				q = int(data[i].split(" ")[1])
				discounted[1] += q
			if "Д к" in data[i+1]:
				q = int(data[i].split(" ")[1])
				discounted[1] += q
			if "17р" in data[i+1]:
				q = int(data[i].split(" ")[1])
				halfTheCost[1] += q
			if "Мест" in data[i+1]:
				q = int(data[i].split(" ")[1])
				fullyPrice[1] += q
			if "Пинск" in data[i+1]:
				q = int(data[i].split(" ")[1])
				fullyPrice[1] += q
		i += 1
	createBody(report, fullyPrice,  discounted, halfTheCost) #Версия до 25.04.24
	return report
fileList = []
reportData = getReportData()
for string in reportData:
	print(string.getStringValue())
report = Report(reportData)
report.create()
