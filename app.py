import time
import numpy as np
import pandas
import requests
from sklearn import linear_model
from scipy import stats
import statsmodels.api as sm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from flask import Flask, render_template, request

option = Options()
option.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)

app = Flask(__name__)

def predictFromGivenShare(share,givenDate,value):
    url = "https://www.ibovx.com.br/default.aspx"
    driver.get(url)
    driver.find_element_by_id('ContentPlaceHolderCentro_txtAcoesBovespa').send_keys(share)
    driver.find_element_by_id('ContentPlaceHolderCentro_btnBuscaPapel').click()
    time.sleep(1)
    select = Select(driver.find_element_by_id('ContentPlaceHolderCentro_ddlNumeroPregoes'))
    select.select_by_visible_text("últimos 30")
    driver.find_element_by_id('ContentPlaceHolderCentro_btnBuscaPapel').click()
    
    #get data from table
    element = driver.find_element_by_id("idConteudo")
    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.select_one("table[style='width:100%;border:1px;border-color:#DFE2E5;']")
    table = str(table).replace(',','.')
    #['data','var_perc','var','cotacao','abertura','minimo','maximo','volume','total_neg']
    df_full = pandas.read_html(str(table),skiprows=(0,12),header=None)[0]
    df_full.columns = ['data','var_perc','var','fechamento','abertura','minimo','maximo','volume','total_neg']
    df = df_full[['data','fechamento','abertura']]
    #df_full['fechamento'] = df_full['fechamento'].str.replace(',', '.').astype(float)
    #df_full['abertura'] = df_full['abertura'].str.replace(',', '.').astype(float)
    time.sleep(1)

    return predict(df,givenDate,value)

def date2num(date_time):
    d,m,y = date_time.split('/')
    num = int(d)*10 + int(m)*100 + int(y)*1000 # these weights can be anything as long as 
                                          # they are ordered
    return num

def normalizeDate(dates,date_time):
  aux = []
  for d in list(dates):
    aux.append(date2num(d))
  aux.append(date2num(date_time))
  aux = np.array(aux)
  aux_normalized = (aux - np.min(aux))/(np.max(aux) - np.min(aux))
  tam = aux_normalized.size -1
  return aux_normalized[tam]

def predict(df,givenDate,value):
  #df = pandas.read_csv("dados.csv")
  dates = df['data']
  date_features = []
  for d in list(df['data']):
    date_features.append(date2num(d))

  date_features = np.array(date_features)
  date_features_normalized = (date_features - np.min(date_features))/(np.max(date_features) - np.min(date_features))
  df[["data"]] = date_features_normalized

  X = df[["data","fechamento"]]
  y = df[["abertura"]]

  model = linear_model.LinearRegression()
  model.fit(X,y)
  model.score(X, y)
  X1 = sm.add_constant(X)
  result = sm.OLS(y, X1).fit()
  date_to_predict = normalizeDate(dates,givenDate)
  #print(date_features_normalized)
  predictedValue = model.predict([[date_to_predict,value]])

  return predictedValue

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        criteria = request.form['criteria']
        date_criteria = request.form['date_criteria']
        value_criteria = request.form['value_criteria']
        result = predictFromGivenShare(criteria,date_criteria,value_criteria)
        return render_template('index.html',results=result,criteria=criteria)
    return render_template('index.html',results={})

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')

