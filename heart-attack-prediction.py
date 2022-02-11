import streamlit as st
import numpy as np
import pickle as pkl
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
scal=MinMaxScaler()

# Loading the saved model
model=pkl.load(open("C:/Users/Andrea/Downloads/final_model.p","rb"))

# Loading the dataset
df=pd.read_csv("C:/Users/Andrea/Downloads/heart.csv")

st.set_page_config(page_title="Предвидување на ризик од срцев удар",page_icon="⚕️",layout="centered",initial_sidebar_state="expanded")

def preprocess(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal):   
 
    # Pre-processing user input   
    if sex=="машки":
        sex=1 
    else: sex=0
    
    
    if cp=="Типична ангина":
        cp=3
    elif cp=="Атипична ангина":
        cp=1
    elif cp=="Не-ангинална болка":
        cp=2
    elif cp=="Асимптоматски":
        cp=0
    
    if exang=="Да":
        exang=1
    elif exang=="Не":
        exang=0
 
    if fbs=="Да":
        fbs=1
    elif fbs=="Не":
        fbs=0
 
    if slope=="Нагорен: подобар пулс со вежбање (невообичаено)":
        slope=2
    elif slope=="Рамно: минимална промена (типично здраво срце)":
          slope=1
    elif slope=="Наведнат: знаци на нездраво срце":
        slope=0 
 
    if restecg=="Ништо нема да се забележи":
        restecg=1
    elif restecg=="Абнормалност на ST-T бран":
        restecg=2
    elif restecg=="Можна или дефинитивна хипертрофија на левата комора":
        restecg=0

    feat=['age', 	'sex', 	'cp', 'trestbps', 'chol', 	'fbs', 	'restecg', 	'thalach' ,	'exang', 	'oldpeak' ,	'slope', 	'ca', 'thal']
    df[feat] = scal.fit_transform(df[feat])

    user_input=[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
    user_input=np.array(user_input)
    user_input=user_input.reshape(1,-1)
    user_input = scal.transform(user_input)
    prediction = model.predict(user_input)

    return prediction

# Front-End

html_temp = """ 
    <div style ="background-color:pink;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Предвидување на ризик од <br /> срцев удар</h1> 
    </div>
    <br /> 
    """
      
# Header
st.markdown(html_temp, unsafe_allow_html = True) 
      
# Form
age=st.selectbox ("Возраст:",range(1,99,1))
sex = st.radio("Пол:", ('машки', 'женски'))
cp = st.selectbox('Тип на болка во градите:',("Асимптоматски","Атипична ангина","Не-ангинална болка", "Типична ангина")) 
trestbps=st.selectbox('Шеќер во крвта во мирување:',range(1,500,1))
chol=st.selectbox('Серумскиот холестерол во mg/dl:',range(1,1000,1))
fbs=st.radio("Шеќер во крвта при постење повисок од 120 mg/dl:", ['Да','Не'])
restecg=st.selectbox('Електрокардиографски резултати во мирување:',("Ништо нема да се забележи","Абнормалност на ST-T бран","Можна или дефинитивна хипертрофија на левата комора"))
thalach=st.selectbox('Максимален пулс:',range(1,300,1))
exang=st.radio('Ангина индуцирана од вежбање:',["Да","Не"])
oldpeak=st.number_input('ST депресија предизвикана од вежбање во однос на одмор (се гледа стресот на срцето за време на вежбањето):')
slope = st.selectbox('Наклон на ST сегментот:',("Нагорен: подобар пулс со вежбање (невообичаено)","Рамно: минимална промена (типично здраво срце)","Наведнат: знаци на нездраво срце"))
ca=st.slider('Број на главни садови на кои се детектирани масни наслаги користејќи флуросопија:', min_value=0, max_value=4)
thal=st.slider('Резултат на талиум стрес:', min_value=1, max_value=3)

pred=preprocess(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)

if st.button("Предвиди"):    
  if pred[0] == 0:
    st.error('Предупредување! Имате висок ризик да добиете срцев удар!')
    
  else:
    st.success('Честитки! Имате помал ризик да добиете срцева болест!')
    
# Sidebar
st.sidebar.header("ЗА АПЛИКАЦИЈАТА")
st.sidebar.subheader("Проект по биомедицинска електроника")
st.sidebar.info("Оваа веб-апликација со помош на машинско учење ви помага да откриете дали сте изложени на ризик да развиете срцева болест.")
st.sidebar.info("Внесете ги бараните полиња и кликнете на копчето „Предвиди“ за да проверите дали имате здраво срце")
st.sidebar.warning("Внимание: ова е само предвидување, а не докторски совет. Ве молиме посетете лекар ако чувствувате дека симптомите продолжуваат.")
st.sidebar.text('Изработил: Андреа Ивановска 16/2017')
st.sidebar.text("Верзија: 1.0.0 | Декември 2021")