from itertools import combinations

class Transicao:
	def __init__(self,estado_atual,letra,estado_prox):
		self.estado_atual = estado_atual
		self.letra = letra
		self.estado_prox = estado_prox

class Automato:
	def __init__(self, alfabeto, estados, inicial, final, transicoes, qtd_transicao,palavras):
		self.alfabeto = alfabeto.split()
		self.estados = estados.split()
		self.inicial = inicial
		self.final = final
		self.transicoes = transicoes
		self.qtd_transicao = qtd_transicao
		self.palavras = palavras

	def __str__(self):
		transicoes = []
		for t in self.transicoes:
			transicoes.append(f"{t.estado_atual} {t.letra} {t.estado_prox}")
		return f"""
		O alfabeto é: {self.alfabeto};
		Estados: {self.estados};
		Estado Inicial: {self.inicial};
		Estado Final: {self.final};
		As transições:{transicoes};
		Quantidade de transições: {self.qtd_transicao};
		Palavras: {self.palavras}.
		\n"""
	#a b
	def verificarPalavra(self, palavra):
		estado_atual = self.inicial
		for letra in palavra:
			letra_atual = letra
			transicoes_possiveis = self.transicoesPorEstado(estado_atual)
			for transicao in transicoes_possiveis:
				if(transicao.letra == letra_atual):
					estado_atual = transicao.estado_prox
					break
		if estado_atual in self.final:
			return f"M aceita a palavra <{palavra}>\n"
		else:
			return f"M Rejeita a palavra <{palavra}>\n"
				
	
	def executarAutomato(self):
		resultado = []
		for palavra in self.palavras:
			resultado.append(self.verificarPalavra(palavra))	
		return resultado

# Função para transformar um não-deterministico com transições vazias para um não-deterministico
	def AFNeToAFN(self):
		nova_transicao = []

		# Verificamos se a transição possui um vazio (ê)
		# A B C
		for e in self.estados:
			# A a B 
			for t in self.transicoes:
				estado_atual = t.estado_atual

				estado_seguinte = t.estado_prox
				if (t.estado_atual == e):
					if (t.letra in self.alfabeto):
						nova_transicao.append(t)
					# Caso a letra lida for vazio (ê)
					# 'A a A', 'A b A', 'A b B', 'B ê C'
					# 'A a A', 'A b A', 'A b B', 'A b C'
					else:
						for tr in self.transicoes:
							if (tr.estado_prox == estado_atual):
								estado_novo = Transicao(tr.estado_atual,tr.letra,estado_seguinte)
								nova_transicao.append(estado_novo)

		#checar se algum estado não tem transição
		estadoIni = set()
		estadoFi = set()
		for nt in nova_transicao:
			estadoIni.add(nt.estado_atual)
			estadoFi.add(nt.estado_prox)
		estadofora = [x for x in estadoFi if x not in estadoIni]

		# Retira-se o estado que não possui nenhuma transição
		for t in nova_transicao:
			for ef in estadofora:
				if (t.estado_prox == ef):
					nova_transicao.remove(t)

		#atualizando o automato
		nova_transicao.sort(key= lambda x : x.estado_atual)
		self.transicoes = nova_transicao
		self.qtd_transicao = len(nova_transicao)
		self.estados = sorted(list(estadoIni))

		
# Função para transformar um não-deterministico para deterministico
	def AFNtoAFD(self):
		#Usando a biblioteca itertools, pegamos todas as combinações de estados 
		novos_estados = []
		temp_estados = list(combinations(self.estados, 2))
		count = 3
		#Caso o automato tenha a junção de 3 ou mais estados, ele irá rodar este while para obter todos as combinações possíveis
		if len(self.estados) > 2:
			while (len(list(combinations(self.estados, count))) != 0):
				temp_estados += list(combinations(self.estados, count))
				count += 1

		#Transformação de tupla para lista
		for e in temp_estados:
			novos_estados.append(''.join(sorted(e)))

		#Verificação de novos estados finais
		estados_finais = list(self.final)
		for e in novos_estados:
			if (self.final in e):
				estados_finais.append(e)

				
		novas_transicoes = []
		temp_estadoAtual = []
		for e in self.estados:
			temp_estadoAtual = self.transicoesPorEstado(e)
			novas_transicoes += self.criarNovasTransicoesSimples(temp_estadoAtual)
			temp_estadoAtual.clear()
		
		for ne in novos_estados:
			novas_transicoes += self.criarNovasTransicoesComplexas(ne,novas_transicoes)
			
		self.estados = sorted(self.estados + novos_estados)
		self.final = sorted(estados_finais)
		self.transicoes = novas_transicoes
		self.qtd_transicao = len(novas_transicoes)

	# Função que retorna todas as transições de um estado
	def transicoesPorEstado(self,estadoAtual):
		return list(filter(lambda x: x.estado_atual == estadoAtual, self.transicoes))
		
	# 'A a A', 'A b A', 'A b C', 'A b D'
	def criarNovasTransicoesSimples(self,transicoes_atuais):
		novo_estado = ''
		novas_transicoes = []
		for letra in self.alfabeto:
			for t in transicoes_atuais:
				if (letra == t.letra):
					novo_estado += t.estado_prox
			if(novo_estado != ''):
				novas_transicoes.append(Transicao(t.estado_atual,letra,novo_estado))
			novo_estado = ''
		return novas_transicoes

	def criarNovasTransicoesComplexas(self,novo_estado,transicoes):
		transicoes_relativas = []
		novas_transicoes = []
		estado_seguinte = ''
		for t in transicoes:
			if (t.estado_atual in novo_estado):
				transicoes_relativas.append(t)
		for a in self.alfabeto:
			for tr in transicoes_relativas:
				if(a == tr.letra):
					estado_seguinte += tr.estado_prox
			estado_seguinte = set(estado_seguinte)
			estado_seguinte = ''.join(sorted(estado_seguinte))
			novas_transicoes.append(Transicao(novo_estado,a,estado_seguinte))
			estado_seguinte = ''

				
		return novas_transicoes

# Tabela para AFD
#    a    |   b
#A   A    |   AC
#C	 -    |   CD
#D	 CD	  |   -
#AC  A    |   ACD
#AD  ACD  |   AC
#CD  CD   |   CD
#ACD ACD  |   ACD
#E