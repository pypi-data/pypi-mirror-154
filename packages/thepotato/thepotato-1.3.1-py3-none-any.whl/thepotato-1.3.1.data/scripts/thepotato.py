#BIBLIOTECAS IMPORTADAS
import pandas as pd
import requests
from datetime import datetime
import time

#INICIO
print("------POTATO THE PROJECT------", "\n v1.3.1 - Beta")


link = "https://www.commodities-api.com/api/latest?access_key=9rzk9chud8q29qw9b6f1hf5ap77s9p81gszwv2pfs0fg6l2yk7xussm6f98p"
        
resposta = requests.get(link)
preco = resposta.json()

preço_dolar = preco["data"]["rates"]["BRL"]
café = preco["data"]["rates"]["COFFEE"] * 4.6656
petroleo = preco["data"]["rates"]["BRENTOIL"] * 12832
trigo = preco["data"]["rates"]["WHEAT"] * 180033
algodao = preco["data"]["rates"]["COTTON"] * 2.045
açucar = preco["data"]["rates"]["SUGAR"] * 0.0399
arroz = preco["data"]["rates"]["RICE"] * 299.65
ethanol = preco["data"]["rates"]["ETHANOL"] * 4.666
feijao =preco["data"]["rates"]["SOYBEAN"] * 287.83
ng = preco["data"]["rates"]["NG"] * 69.52
madeira =preco["data"]["rates"]["LUMBER"] * 441.880
borracha = preco["data"]["rates"]["RUBBER"] * 298.474
milho = preco["data"]["rates"]["CORN"] * 61.730

while True:
    quest = input("Você deseja uma planilha com os preços?[Y / N]:").upper()

    if quest == "Y":
        tabela = pd.read_excel("lista_preços2.xlsx")
        
        tabela.loc[0, "PREÇO"] = float(preço_dolar)
        tabela.loc[1, "PREÇO"] = float(café)
        tabela.loc[2, "PREÇO"] = float(petroleo)
        tabela.loc[3, "PREÇO"] = float(trigo)
        tabela.loc[4, "PREÇO"] = float(algodao)
        tabela.loc[5, "PREÇO"] = float(açucar)
        tabela.loc[6, "PREÇO"] = float(arroz)
        tabela.loc[7, "PREÇO"] = float(ethanol)
        tabela.loc[8, "PREÇO"] = float(feijao)
        tabela.loc[9, "PREÇO"] = float(ng)
        tabela.loc[10, "PREÇO"] = float(madeira)
        tabela.loc[11, "PREÇO"] = float(borracha)
        tabela.loc[12, "PREÇO"] = float(milho)

        tabela.loc[0, "DATA ATUAL"] = datetime.now()
        tabela.to_excel("lista_preços2.xlsx", index=False)

        break
        
    elif quest == "N":
        print("Ok, não incomodaremos novamente : )")
        break
    else:
        print("Não entendi : (")
        break

    
#CLASS
class Thepotato:
    def __init__(self):
        pass

    #Nome
    def cafe(self):
        self.cafe = "Café"
        print("O nome da Commoditie é:", self.cafe)
        print("O preço é: ", café)

        if café < café * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def petroleo(self):
        self.petroleo = "Petroleo"
        print("O nome da Commoditie é:", self.petroleo)
        print("O preço é: ", petroleo)

        if petroleo < petroleo * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def tri(self):
        self.tri = "Trigo"
        print("O nome da Commoditie é:", self.tri)
        print("O preço é: ", trigo)
        
        if trigo < trigo * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def alg(self):
        self.alg = "Algodão"
        print("O nome da Commoditie é:", self.alg)
        print("O preço é: ", algodao)

        
        if algodao < algodao * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def açu(self):
        self.açu = "Açucar"
        print("O nome da Commoditie é:", self.açu)
        print("O preço é: ", açucar)
        
        if açucar < açucar * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def arro(self):
        self.arro = "Arroz"
        print("O nome da Commoditie é:", self.arro)
        print("O preço é: ", arroz)
        
        if arroz < arroz * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def eth(self):
        self.eth = "Ethanol"
        print("O nome da Commoditie é:", self.eth)
        print("O preço é: ", ethanol)
        
        if ethanol < ethanol * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def fei(self):
        self.fei = "Feijão"
        print("O nome da Commoditie é:", self.fei)
        print("O preço é: ", feijao)
        
        if feijao < feijao * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def nat(self):
        self.nat = "Gás Natural"
        print("O nome da Commoditie é:", self.nat)
        print("O preço é: ", ng)
        
        if ng < ng * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def mad(self):
        self.mad = "Madeira"
        print("O nome da Commoditie é:", self.mad)
        print("O preço é: ", madeira)
        
        if madeira < madeira * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def bor(self):
        self.bor = "Borracha"
        print("O nome da Commoditie é:", self.bor)
        print("O preço é: ", borracha)
        
        if borracha < borracha * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")

    def mil(self):
        self.mil = "Milho"
        print("O nome da Commoditie é:", self.mil)
        print("O preço é: ", milho)
        
        if milho < milho * 0.97:
            print("Recomendação: Compra")
        else:
            print("Recomendação: Venda")
        print("-------------------")


    #Funçao de hora
    def hora(self):
        print("Preços atualizados:", datetime.now())
