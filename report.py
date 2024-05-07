class Payment:
	def __init__(self, value):
		self.value = value
		self.count = 0
		
	def getTotal(self):
		return self.value * self.count
		
	def reset(self):
		self.count = 0

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
			print("----------------------------------------")
			
	def createBody(self, discounted, halfTheCost, fullyPrice):
		print(f"По дисконту: {discounted.count} человек. На сумму: {discounted.getTotal()} руб.")
		print(f"За полстоимости: {halfTheCost.count} человек. На сумму: {halfTheCost.getTotal()} руб.")
		print(f"За полную стоимость: {fullyPrice.count} человек. На сумму: {fullyPrice.getTotal()} руб.")
		print("========================================")
		
	def create(self):
		fullyPrice = Payment(35)
		discounted = Payment(30)
		halfTheCost = Payment(17)
		count = 0
		print("ОТЧЁТ" + "\n" + "========================================")
		i = 0
		while(i < len(self.body)):
			if isinstance (self.body[i], ReportStr):
				if self.body[i].header:
					if fullyPrice.count + discounted.count + halfTheCost.count != 0:
						self.createBody(discounted, halfTheCost, fullyPrice)
						fullyPrice.reset()
						discounted.reset()
						halfTheCost.reset()
					self.createHeader(self.body[i])
				else:
					if self.body[i].isDiscount() and not self.body[i].isCashless():
						discounted.count += count
					elif self.body[i].isHalfTheCost() and not self.body[i].isCashless():
						halfTheCost.count += count
					else:
						if not self.body[i].isCashless():
							fullyPrice.count += count
			if isinstance (self.body[i], ReportCount):
				if self.body[i].status:
					count = self.body[i].strToInt()
				else: count = 0
			i += 1
		self.createBody(discounted, halfTheCost, fullyPrice)
			
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
	
	def isHalfTheCost(self):
		'''words = ["17р"]
		for word in words:'''
		if "17р" in self.string:
			return True
		return False
	
	def isDiscount(self):
		words = ["дк", "Д.К.", "Д к ", "Дк"]
		for word in words:
			if word in self.string:
				return True
		return False
		
	def isCashless(self):
		words = ["безнал", "б/н"]
		for word in words:
			if word in self.string:
				return True
		return False
		
class ReportCount:
	def __init__(self, string):
		self.count = string.strip()
		self.status = False	
		
	def getStringValue(self):
		return self.count
		
	def getDataFromString(self):	
		self.count = self.count[17:len(self.count)-5]

	def strToInt(self):
		return int(self.count)

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
				data.append(ReportStr(text[i]))
				data[len(data) - 1].getDataFromString()
		i += 1
	return data

fileList = []
reportData = getReportData()
report = Report(reportData)
report.create()
