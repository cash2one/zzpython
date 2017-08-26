#-*- coding: UTF-8 -*-
#!/usr/bin/python
class PriceOffer:
    def __init__(self, id="", title="", category="", name="", instruction="", downloadNum="", gmtCreated=""):
        self.id = id
        self.title = title
        self.category = category
        self.name = name
        self.instruction = instruction
        self.downloadNum = downloadNum
        self.gmtCreated = gmtCreated
    