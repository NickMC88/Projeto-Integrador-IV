from encodings.utf_8 import encode
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup



def leitor(contagem):
    #Dando scroll na página
    lenOfPage = 10
    lastCount = -1
    match = False
    #Se o infinite scroll for igual a true vai rolar pra sempre
    infinite_scroll = False

    print("Rolando paginas...")
    while not match:
        if infinite_scroll:
            lastCount = lenOfPage
        else:
            lastCount += 1

        print("Numero de scrolls:", lastCount, sep=" ")
        # wait for the browser to load, this time can be changed slightly ~3 seconds with no difference, but 5 seems
        # to be stable enough
        sleep(5)

        if infinite_scroll:
            lenOfPage = browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")
        else:
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")

        if lastCount == lenOfPage:
            match = True



    page_content = browser.page_source

    site = BeautifulSoup(page_content, 'html.parser')
    resultados = []

    textos = site.findAll('div', attrs={'class': 'icdlwmnq'})
   

    sleep(10)

    for post in textos:
        descricao = post.find('div', attrs={'dir': 'auto'})
        if descricao == None:
            pass
        else:
            resultados.append(descricao.getText())
  
    df = pd.DataFrame(resultados)
    df.to_csv(f"result{contagem}.csv", encoding = "utf-8", index = False)
 


browser = webdriver.Firefox()

usuario = "projetoIntegradorIV2022@outlook.com"
senha = "Projeto@963"

browser.get("https://www.facebook.com")
print("Acessou o Facebook...")
sleep(1)

try:
    campo_nome_usuario = browser.find_element(by=By.ID, value="email")
    campo_nome_usuario.send_keys(usuario)
    print("Entrou com o nome de usuário...")
    sleep(1)
except Exception as excpt:
    print(f"Tivemos uma falha: {excpt}")
    browser.quit()
    exit(1)

try:
    campo_senha = browser.find_element(by=By.ID, value="pass")
    campo_senha.send_keys(senha)
    print("Entrou com a senha de usuário...")
    sleep(1)
except Exception as excpt:
    print(f"Tivemos uma falha: {excpt}")
    browser.quit()
    exit(1)

try:
    botao_login = browser.find_element(by=By.NAME, value="login")
    botao_login.click()
    print("Clicou no botão de login...")
    sleep(1)
except Exception as excpt:
    print(f"Tivemos uma falha: {excpt}")
    browser.quit()
    exit(1)


browser.get("https://www.facebook.com/search/posts/?q=lula")

leitor(contagem=1)

browser.get("https://www.facebook.com/search/posts/?q=Bolsonaro")

leitor(contagem=2)

df1 = pd.read_csv("result1.csv", encoding="utf-8")

df2 = pd.read_csv("result2.csv", encoding="utf-8")

texto = [df1, df2]

resultado = pd.concat(texto)
resultado.rename({"0":"resultado"}, axis=1,inplace=True)
resultado.to_csv("final.csv", encoding = "utf-8", index = False)

print("Pronto!")
input("Pressione enter para sair...")
browser.quit()
print("Fim...")
