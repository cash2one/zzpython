class RandomChar():
	@staticmethod
	def Unicode():
		val = random.randint(0x4E00, 0x9FBF)
		return unichr(val)	

	@staticmethod
	def GB2312():
		head = random.randint(0xB0, 0xCF)
		body = random.randint(0xA, 0xF)
		tail = random.randint(0, 0xF)
		val = ( head << 8 ) | (body << 4) | tail
		str = "%x" % val
		return str.decode('hex').decode('GB18030','ignore')

class ImageChar():
	def __init__(self, fontColor = (0, 0, 0),
										 size = (70, 25),
										 fontPath = '/var/pythoncode/mobileweb/simhei.ttf',
										 bgColor = (255, 255, 255),
										 fontSize = 20):
		self.size = size
		self.fontPath = fontPath
		self.bgColor = bgColor
		self.fontSize = fontSize
		self.fontColor = fontColor
		self.font = ImageFont.truetype(self.fontPath, self.fontSize)
		self.image = Image.new('RGB', size, bgColor)	

	def rotate(self):
		self.image.rotate(random.randint(0, 20), expand=0)	

	def drawText(self, pos, txt, fill):
		draw = ImageDraw.Draw(self.image)
		draw.text(pos, txt, font=self.font, fill=fill)
		del draw	

	def randRGB(self):
		return (random.randint(0, 255),
					 random.randint(0, 255),
					 random.randint(0, 255))	

	def randPoint(self):
		(width, height) = self.size
		return (random.randint(0, width), random.randint(0, height))	

	def randLine(self, num):
		draw = ImageDraw.Draw(self.image)
		for i in range(0, num):
			draw.line([self.randPoint(), self.randPoint()], self.randRGB())
		del draw	

	def randChinese(self, num):
		gap = 5
		start = 0
		chars=""
		for i in range(0, num):
			char = RandomChar().GB2312()
			x = start + self.fontSize * i + random.randint(0, gap) + gap * i
			self.drawText((x, random.randint(-5, 5)), char, self.randRGB())
			self.rotate()
			chars+=char
		self.randLine(6)
		return chars
	def returnimg(self):
		return self.image
	def save(self, path):
		self.image.save(path)