
from selenium import webdriver 


from selenium.webdriver.common.by import By


from selenium.webdriver.chrome.service import Service 


from selenium.webdriver.common.action_chains import ActionChains


from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as ec 


import pandas as pd 


import time 


from selenium.common.exceptions import TimeoutException 


chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Configuração do WebDriver 
service = Service(chrome_driver_path)  
options = webdriver.ChromeOptions() 
options.add_argument("--disable-gpu") 
options.add_argument("--window-size=1920,1080") 



driver = webdriver.Chrome(service=service, options=options) 


url_base = "https://www.kabum.com.br/promocao/COMPUTADORKABUM"
driver.get(url_base)
time.sleep(5) # aguarda 5 seg para garantir que a pág carregue 


dic_produtos = {"marca": [], "preco": []} # criar um dicionário vazio para armazenar as marcas e preços das cadeiras 


pagina = 1

while True:
    print(f"\n Coletando dados da página {pagina}...")

    try: 
        WebDriverWait(driver,10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME,"productCard"))
        )
        print("Elementos encontrados com sucesso!")
    except TimeoutException:
        print("Tempo de espera excedido!")

    produtos = driver.find_elements(By.CLASS_NAME,"productCard")

    for produto in produtos:
        try:
            nome= produto.find_element(By.CLASS_NAME,"nameCard").text.strip()
            preco= produto.find_element(By.CLASS_NAME,"priceCard").text.strip()

            print(f"{nome} - {preco}")

            dic_produtos["marca"].append(nome)
            dic_produtos["preco"].append(preco)

        except Exception: 
            print("Erro ao coletar dados:" , Exception)



    try:
        botao_proximo = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )

        if botao_proximo:
            driver.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(1)

            driver.execute_script("arguments[0].click();", botao_proximo)
            print(f"Indo para a página {pagina}")
            pagina += 1

            time.sleep(5)

        else:
            print("Você chegou na última página!")
            break

    except Exception as e:
        print("Erro ao tentar avançar para a próxima página", e)
        break


driver.quit()

df = pd.DataFrame(dic_produtos)
df.to_excel("computadores.xlsx", index=False)

print(f"Arquivo 'cadeiras' salvo com sucesso! ({len(df)} produtos capturados!)")

