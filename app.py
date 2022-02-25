import streamlit as st
import pandas as pd
import sqlite3

con = sqlite3.connect("dbsqlite.db")
cur = con.cursor()

st.title('Job dashboard')

lieu = pd.read_sql_query("""SELECT distinct(lieu) 
                            from evenement 
                            """, con)

new_row = pd.DataFrame({'lieu':'Default'}, index =[0])
new_lieu = pd.concat([new_row, lieu]).reset_index(drop = True)                           
chosen_lieu = st.sidebar.selectbox('Lieu', new_lieu)

job = ["Default","Data engineer","Data analyst","Data scientist"]
chosen_job = st.sidebar.selectbox('Type de poste', job)

langue = ["Français","Anglais"]
chosen_langue = st.sidebar.selectbox('Langue', langue)

if chosen_lieu != "Default":
    if chosen_langue == "Français":
        bdd_langue = "fr"
        language_code = "fr-FR"
    elif chosen_langue == "Anglais":
        bdd_langue = "en"
        language_code = "en-US"

    df = pd.read_sql_query(f"""SELECT * 
                            from evenement 
                            WHERE lieu = "{chosen_lieu}" and langue = "{bdd_langue}";""", con)
    st.dataframe(df.astype(str))

    if len(df) != 0:
        location = st.slider("Choissisez l'index de votre offre", -1,len(df)-1)
        if location != -1:
            test2 = ["Offre entière", "Mots clés"]
            test = st.selectbox("Choissisez le mode", test2)
        try:
            description = df.iloc[location]["description"]
            offre = df.iloc[location]["intitule_offre"]
            lieu = df.iloc[location]["lieu"]
            entreprise = df.iloc[location]["nom_entreprise"]
            date = df.iloc[location]["date_publication_annonce"]
            id = df.iloc[location]["id"]
            key_words = df.iloc[location]["key_words"]
            if test == "Offre entière":
                st.write("Intitulé : ", offre)
                st.write("Lieu : ", lieu)
                st.write("Nom entreprise : ", entreprise)
                st.write("Date de publication : ", date)
                st.write(description)
                #st.write("key words : ",key_words)
            elif test == "Mots clés":
                st.write("Key words : ")
                st.write(key_words)
               
        except:
            st.write("")
    else :
        st.write("Aucune offre disponible")

if chosen_job == "Data analyst":
    df = pd.read_sql_query("""select nom_commune, avg(valeur_fonciere/surface_reelle_bati) 
                            from dvf 
                            where type_local="Appartement" and code_departement = '38'
                            group by nom_commune 
                            order by avg(valeur_fonciere/surface_reelle_bati)  ASC
                            limit 20;""", con)
    st.dataframe(df.astype(str))

con.close()

