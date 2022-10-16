import streamlit as st 
import pandas as pd 
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os
st.set_page_config(page_title='Analyse de données',layout='wide')


def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb

def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext in ('.csv','.xlsx'):
        return ext
    else:
        return False
    

# sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Téléchargez des fichiers .csv, .xlsx ne dépassant pas 10 MB")
    if uploaded_file is not None:
        st.write('Modes de fonctionnement')
        minimal = st.checkbox('Voulez-vous un rapport minimal ?')
        display_mode = st.radio('Mode affichage:',
                                options=('Bleu','Noir','Orange'))
        if display_mode == 'Dark':
            dark_mode= True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False
        
    
if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        filesize = get_filesize(uploaded_file)
        if filesize <= 10:
            if ext == '.csv':
                # time being let load csv
                df = pd.read_csv(uploaded_file)
            else:
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox('Sélectionnez la feuille',sheet_tuple)
                df = xl_file.parse(sheet_name)
                
                
            # generate report
            with st.spinner('Generation de Report'):
                pr = ProfileReport(df,
                                minimal=minimal,
                                dark_mode=dark_mode,
                                orange_mode=orange_mode
                                )
                
            st_profile_report(pr)
        else:
            st.error(f'La taille maximale autorisée est de 10 Mo. Mais reçu{filesize} MB')
            
    else:
        st.error('Veuillez télécharger uniquement le fichier .csv ou .xlsx')
        
else:
    st.title('Prifilage de données')
    st.info('Téléchargez vos données ')
    