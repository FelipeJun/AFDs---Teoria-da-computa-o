import re
import io
import conversor as af

class readText:
	def __init__(self,path_file):
		self.path = path_file;
		
	def __str__(self):
		f = io.open(self.path,mode="r", encoding="utf-8");
		return f.read()

	def fileTreatment(self):
		f = open(self.path,mode="r", encoding="utf-8");
		text = f.read()
		# Usando a biblioteca de ReGex do python, usamos o split para separar por linha
		lines = re.split("\n",text)
		automato = {}
		temp_transicao = []
		transicoes = []
		palavras = []
		#Feita a leitura e separação das caracteristicas do automato
		for l in lines:
			if(not l.startswith("#")):
				if(l.startswith("A ")): automato["alfabeto"] = (l[2:])
				if(l.startswith("Q ")): automato["estados"] = (l[2:])
				if(l.startswith("q ")): automato["inicial"] = l[2:]	
				if(l.startswith("F ")): automato["final"] = l[2:]
				if(l.startswith("T ")): temp_transicao.append(l[2:])
				if(l.startswith("P ")): palavras.append(l[2:])

		for t in temp_transicao:
			temp = t.split(' ')
			transicoes.append(af.Transicao(temp[0],temp[1],temp[2]))
		automato["transicoes"] = transicoes
		automato["palavras"] = palavras
		# Exceptions para caso uma das caracteristicas não sejam encontradas no arquivo
		if ("alfabeto" not in automato or automato["alfabeto"] == 0): 
			raise Exception("Arquivo não possui alfabeto")
		if ("estados" not in automato or automato["estados"] == 0):
			raise Exception("Arquivo não possui estados")
		if ("inicial" not in automato or automato["inicial"] == 0):
			raise Exception("Arquivo não possui estado inicial")
		if ("final" not in automato or automato["final"] == 0):
			raise Exception("Arquivo não possui estado final")	
		if ("transicoes" not in automato or len(automato["transicoes"]) == 0):
			raise Exception("Arquivo não possui transições")
		if ("palavras" not in automato or len(automato["palavras"]) == 0):
			raise Exception("Arquivo não possui palavras de exemplo")

		return automato