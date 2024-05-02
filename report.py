def getFilList():
	return

def reWriteTmpFile(content):
	tmpFile = "/home/valentin/Python/otchotTest/temp.txt"
	with open(tmpFile, "w") as file:
		file.write("")
	with open(tmpFile, "a") as file:
		for string in content:
			file.writelines(string + "\n")

def reWriteOtchot(report):
	rFile = "/home/valentin/Python/Report/report.txt"
	with open(rFile, "w") as file:
		file.write("")
	with open(rFile, "a") as file:
		for string in report:
			file.writelines(string + "\n")
			
def getFileContent():
	myFile = "/home/valentin/Documents/Водители.txt"
	with open(myFile, encoding = "utf8") as file:
		text = file.readlines()
		return text
		
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
    Здесь выбираются строки для формирования отчёта.
'''        
def get_html(f_c):
	lst = []
	getString = False
	for string in f_c:
		if "<body>" in string:
			getString = True
		if "</body>" in string:
			getString = False
		if "BDB9BD" in string:
			getString = True
		if "ffcccc" in string:
			getString = False
		if "bgcolor=\"white\"" in string:
			getString = True
		if "adebeb" in string:
			getString = False
		if getString:
			string = string.strip()
			if match(string):
				string = string[16:]
				string = string[:len(string) - 5]
				lst.append(string)
			if "<td width=\"25px\">" in string:
			#Здесь выбираются строки где обозначено количество мест.
				string = string.replace("<td width=\"25px\">", "Мест ")
				lst.append(string[:len(string) - 5])
	return lst
'''
    Конец блока.
'''
'''
	Версия функции до 25.04.24
'''
'''
def getHTMLContent(fileContent):
	lst = []
	start = False
	for string in fileContent:
		if "<body>" in string:
			start = True
		if "</body>" in string:
			start = False
		if start:
			string = string.strip()
			if "colspan=\"5\"" in string:
				string = string[16:]
				string = string[:len(string) - 5]
				lst.append(string)
	lst_ = []
	for string in lst:
		if "Пинск" in string:
			lst_.append(string)
		elif "свободно" in string:
			lst_.append(string)
		elif "+" in string:
			lst_.append(string)
	return lst_
'''
'''
	С 25.04.24 не используется.
	
def createReportData(fileC):
	i = 0
	report = ["Данные для формирования отчёта"]
	while i < len(fileC):
		if "Пинск" in fileC[i]:
			report.append("\nЗаголовок\n")
			report.append(fileC[i])
			i += 1
			report.append(fileC[i])
			report.append("\nТело\n")
		else: report.append(fileC[i])
		i += 1
	return report
'''

def convertDate(date):
	month = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
	subDate = date.split("-")
	return subDate[2] + " " + month[int(subDate[1]) - 1] + " " + subDate[0]

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
fileList = getFilList()		
fileContent = getFileContent()
fileContent = get_html(fileContent)
report = create(fileContent)
reWriteOtchot(report)
#reWriteTmpFile(fileContent)

