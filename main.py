import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from datetime import datetime
import pytz
import pycountry_convert as pc

co0 = "#444466"  # preto
co1 = "#feffff"  # branca
co2 = "#6f9fbd"  # azul

fundo_manhã = "#6cc4cc"
fundo_tarde = "#bfb86d"
fundo_noite = "#484f60"
fundo = fundo_manhã

janela = Tk()
janela.title("Previsão do tempo")
janela.geometry("320x350")
janela.configure(bg=fundo)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=157)

frame_top = Frame(janela, width=380, height=50, bg=fundo, pady=0, padx=0)
frame_top.grid(row=1, column=0)

frame_corpo = Frame(janela, width=320, height=300, bg=fundo, pady=12, padx=0)
frame_corpo.grid(row=2, column=0, sticky=NW)

estilo = ttk.Style(janela)
estilo.theme_use("clam")

# Inicializando o ícone como um widget vazio para ser configurado depois
txticone = Label(frame_corpo, bg=fundo)
txticone.place(x=175, y=50)

# Função para buscar informações da API e atualizar os dados
def informacao():
    cidade = txt.get()
    if not cidade.strip():
        txtcidade.config(text="Por favor, insira uma cidade.")
        return

    key = "00db42c84e515c63e40a32bb8b58d71c"
    link_api = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={key}&units=metric&lang=pt_br"

    try:
        r = requests.get(link_api)
        dados = r.json()

        if r.status_code == 200:
            # País
            dados_pais = dados["sys"]["country"]
            pais = pytz.country_names[dados_pais]

            # Continente
            def pais_form(i):
                pais_alpha = pc.country_name_to_country_alpha2(i)
                pais_continente_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
                pais_continente_nome = pc.convert_continent_code_to_continent_name(pais_continente_codigo)
                return pais_continente_nome

            continente = pais_form(pais)

            # Data e hora
            fusohorario = pytz.timezone(pytz.country_timezones[dados_pais][0])
            horario = datetime.now(fusohorario).strftime("%d/%m/%Y | %H:%M:%S")

            # Clima
            temperatura = dados["main"]["temp"]
            pressao = dados["main"]["pressure"]
            velocidade_vento = dados["wind"]["speed"]
            descricao = dados["weather"][0]["description"]

            cidade_nome = f"{cidade.title()} - {pais} - {continente}"
            txtcidade.config(text=cidade_nome)
            txtdata.config(text=horario)
            txttemp.config(text=f"{temperatura:.1f}°C")
            txtpresao.config(text=f"Pressão: {pressao} hPa")
            txtvelocidadevento.config(text=f"Vento: {velocidade_vento} m/s")
            txtclima.config(text=descricao.capitalize())

            # Atualizando o fundo e o ícone com base no horário
            global fundo
            hora_programa = datetime.now(fusohorario).hour
            if hora_programa <= 5:
                fundo = fundo_noite
                caminho_imagem = 'icons/noite.png'
                
            elif hora_programa <= 11:
                fundo = fundo_manhã
                caminho_imagem = 'icons/ensolarado.png'
                
            elif hora_programa <= 17:
                fundo = fundo_tarde
                caminho_imagem = 'icons/por-do-sol.png'
                
            else:
                fundo = fundo_noite
                caminho_imagem = 'icons/noite.png'
                

            # Atualizando a imagem
            try:
                imagem = Image.open(caminho_imagem)
                imagem = imagem.resize((130, 130))
                imagem = ImageTk.PhotoImage(imagem)
                txticone.config(image=imagem, bg= fundo)
                txticone.image = imagem
            except Exception as e:
                txtcidade.config(text="Erro ao carregar ícone.")

            # Atualizando cores de fundo
            janela.configure(bg=fundo)
            frame_top.configure(bg=fundo)
            frame_corpo.configure(bg=fundo)
            txtcidade["bg"] = fundo
            txtdata["bg"] = fundo
            txtpresao["bg"] = fundo
            txtvelocidadevento["bg"] = fundo
            txtclima["bg"] = fundo
            txttemp["bg"] = fundo
        else:
            txtcidade.config(text="Cidade não encontrada.")
    except Exception as e:
        txtcidade.config(text="Erro ao buscar dados.")

# Campo de entrada para a cidade
txt = Entry(frame_top, width=20, justify="left", font=("", 14), highlightthickness=1, relief="solid")
txt.place(x=15, y=10)

# Botão que chama a função informacao
btn = Button(frame_top, command=informacao, text="Ver Clima", bg=co1, fg=co2, font=("Ivy 9 bold"), relief="raised", overrelief=RIDGE)
btn.place(x=250, y=10)

txtcidade = Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 13"))
txtcidade.place(x=10, y=4)

txtdata = Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 10"))
txtdata.place(x=10, y=54)

txttemp = Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 40"))
txttemp.place(x=10, y=100)

txtpresao = Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 10"))
txtpresao.place(x=10, y=195)

txtvelocidadevento = Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 10"))
txtvelocidadevento.place(x=10, y=225)

txtclima = Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 10 bold"))
txtclima.place(x=180, y=195)

janela.mainloop()
