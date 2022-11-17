import readinput as r
import conversor as af

if __name__ == "__main__":
	#colocar o nome do arquivo a ser lido
	file = r.readText("entrada.txt")
	maquina = file.fileTreatment()
	autoFin = af.Automato(maquina["alfabeto"],
		maquina["estados"], maquina["inicial"], 
		maquina["final"], maquina["transicoes"], 
		len(maquina["transicoes"]), maquina["palavras"])

	with open("saida.txt", "w") as f:
		f.write("Maquina AFND-e")
		f.write(str(autoFin))
		
		f.write("Maquina AFND")
		autoFin.AFNeToAFN()
		f.write(str(autoFin))
		
		f.write("Maquina AFD")
		autoFin.AFNtoAFD()
		f.write(str(autoFin))

		f.write('\n')
		for resultado in autoFin.executarAutomato():
			f.write(resultado)