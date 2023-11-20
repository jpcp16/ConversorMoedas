import requests
import PySimpleGUI as sg

sg.theme('Dark Green 4')

# Importar dados da API
def obter_taxas():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    data = response.json()
    return data['rates']

# Converção das Moedas
def converter_moedas(valor, moeda_origem, moeda_destino, taxas):
    if moeda_origem in taxas and moeda_destino in taxas:
        taxa_origem = taxas[moeda_origem]
        taxa_destino = taxas[moeda_destino]
        valor_em_usd = valor / taxa_origem
        valor_convertido = valor_em_usd * taxa_destino
        return valor_convertido
    else:
        return None

taxa_cambio = obter_taxas()

# PySimpleGUI
layout = [
    [sg.Text('Valor a converter:'), sg.Input(key='valor')],
    [sg.Text('Moeda de origem:'), sg.Combo(list(taxa_cambio.keys()), size=(15, 1), key='moeda_origem')],
    [sg.Text('Moeda de destino:'), sg.Combo(list(taxa_cambio.keys()), size=(15, 1), key='moeda_destino')],
    [sg.Button('Converter'), sg.Button('Sair')],
    [sg.Text('Valor convertido:'), sg.Output(key='valor_convertido')]
]
janela = sg.Window('CONVERSOR DE MOEDAS - JP', layout)


while True:
    evento, valores = janela.read()
    if evento == 'Sair':
        break

    # Converte o valor inserido de acordo com as moedas de origem e destino selecionadas.
    valor = float(valores['valor'])
    moeda_origem = valores['moeda_origem']
    moeda_destino = valores['moeda_destino']
    valor_convertido = converter_moedas(valor, moeda_origem, moeda_destino, taxa_cambio)

    # Exibe o resultados
    if valor_convertido is not None:
        janela['valor_convertido'].update(f'{valor_convertido:.2f} {moeda_destino}')
    else:
        janela['valor_convertido'].update('Moeda não encontrada')

janela.close()