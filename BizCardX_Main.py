


from cv2 import colorChange
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import sqlite3

def image_to_text(path):

    input_image= Image.open(path)

    # convert image to arry format
    img_arr= np.array(input_image)

    Reader= easyocr.Reader(["en"])
    Text=Reader.readtext(img_arr, detail=0)

    return Text,input_image


def extracted_text(texts):

  extracted_dict= {"NAME":[], "DESIGNATION":[], "COMPANY_NAME":[], "CONTACT":[], "EMAIL":[], "WEBSITE":[], "ADDRESS":[], "PINCODE":[]}

  extracted_dict["NAME"].append(texts[0])
  extracted_dict["DESIGNATION"].append(texts[1])

  for i in range(2,len(texts)):

    if texts[i].startswith("+") or (texts[i].replace("-","").isdigit()and "-" in texts[i]):
      extracted_dict["CONTACT"].append(texts[i])

    elif "@" in texts[i] and ".com" in texts[i]:
      extracted_dict["EMAIL"].append(texts[i])

    elif "www" in texts[i] or "WWW" in texts[i] or "Www" in texts[i] or "wWw" in texts[i] or "wwW" in texts[i]:
      small=texts[i].lower()
      extracted_dict["WEBSITE"].append(small)

    elif "TamilNadu" in texts[i] or "Tamil Nadu" in texts[i] or "Tamilnadu" in texts[i] or "Tamil nadu" in texts[i] or texts[i].isdigit():
      extracted_dict["PINCODE"].append(texts[i])

    elif re.match(r'^[A-Za-z]',texts[i]):
      extracted_dict["COMPANY_NAME"].append(texts[i])

    else:
      address= re.sub(r'[,;]','', texts[i])
      extracted_dict["ADDRESS"].append(address)

  for key,value in extracted_dict.items():

    if len(value)>0:
      joint_value= " ".join(value)
      extracted_dict[key]= [joint_value]

    else:
      value = "NA"
      extracted_dict[key]= [value]

  return extracted_dict


# streamlit part

st.set_page_config(layout= "wide")



select=option_menu(menu_title=None, options=["About","Upload & Modify","Delete"], icons=["house","upload","trash"] ,orientation="horizontal",
                   default_index=0,
                   styles={"container":{"padding": "0!important", "background-color": "LightBlue", "size": "cover"},
                           "icons":{"color": "white", "font-size": "20px"},
                           "nav-link":{"font-size": "20px", "text-align":"center", "margin": "-2px", "--hover-color": "#7234fa"},
                           "nav-link-selected": {"background-color": "#7234fa"}})


if select == "About":
  st.header("BizcardX Data Extraction")
  
  st.write("BizcardX is a Python application is degigned for extracting the data from Business card.")
  st.markdown(" ")
  st.markdown(" ")
  st.write("The purpose of this application is extract the data from a Business card (Image format) using the OCR (optical character regonition) and store the extracted data as a dataframe in SQlite3 and automate the extracting details from business card to modify the details in simple steps.")
  
  st.subheader("Skills Involved")
  st.markdown(" ")
  st.markdown(" ")
  st.write("OCR")
  st.write("Streamlit")
  st.write("SQlite3")
  st.write("Python")
    

    
elif select == "Upload & Modify":

   uploaded_file= st.file_uploader("Upload The Image", type=["png", "jpg", "jpeg"])

   if uploaded_file is not None:
    st.image(uploaded_file, width= 300)

    text_image, input_image= image_to_text(uploaded_file)

    text_dict= extracted_text(text_image)

    if text_dict:
      st.success("TEXT IS EXTRACTED SUCCESSFULLY !")

    df= pd.DataFrame(text_dict)

    # Converting Image to Bytes

    Image_bytes= io.BytesIO()
    input_image.save(Image_bytes, format= "PNG")

    Image_data= Image_bytes.getvalue()

    # Creating Dictionary
    data ={"IMAGE":[Image_data]}
    df_1= pd.DataFrame(data)

    concat_df = pd.concat([df,df_1], axis= 1)

    st.dataframe(concat_df)

    button_1 = st.button("save", use_container_width=True)

    if button_1:
      mydb= sqlite3.connect("bixcard_db")
      cursor= mydb.cursor()

      #Table Creation

      create_table_query = """ CREATE TABLE IF NOT EXISTS bizcard_details(name VARCHAR(250),
                                                                  designation VARCHAR(250),
                                                                  company_name VARCHAR(250),
                                                                  contact VARCHAR(250),
                                                                  email VARCHAR(250),
                                                                  website TEXT,
                                                                  address TEXT,
                                                                  pincode VARCHAR(250),
                                                                  image TEXT)"""

      cursor.execute(create_table_query)
      mydb.commit()

      mydb= sqlite3.connect("bixcard_db")
      cursor= mydb.cursor()

      # Insert Query

      insert_query_1= """INSERT INTO bizcard_details(name, designation, company_name, contact, email, website, address, pincode, image)

                        VALUES(?,?,?,?,?,?,?,?,?)"""

      sql_data = concat_df.values.tolist()[0]
      cursor.execute(insert_query_1,sql_data)
      mydb.commit()

      st.success("SUCCESSFULLY SAVED!")

   method = st.radio("Select The Method",["None","Preview","Modify"])

   if method == "None":
    st.write("")

   if method == "Preview":

    mydb= sqlite3.connect("bixcard_db")
    cursor= mydb.cursor()

    #select query
    select_query = "SELECT * FROM bizcard_details"

    cursor.execute(select_query)
    table = cursor.fetchall()
    mydb.commit()

    table_df= pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE",
                                          "ADDRESS", "PINCODE", "IMAGE"))
    st.dataframe(table_df)

   elif method == "Modify":

        mydb= sqlite3.connect("bixcard_db")
        cursor= mydb.cursor()

        #select query
        select_query = "SELECT * FROM bizcard_details"

        cursor.execute(select_query)
        table = cursor.fetchall()
        mydb.commit()

        table_df= pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE",
                                              "ADDRESS", "PINCODE", "IMAGE"))

        col1,col2 = st.columns(2)
        with col1:

          name= st.selectbox("Select The Name", table_df["NAME"])

        df_3= table_df[table_df["NAME"] == name]

        df_4 = df_3.copy()


        col1,col2= st.columns(2)
        with col1:
          modify_name = st.text_input("Name", df_3["NAME"].unique()[0])
          modify_designation = st.text_input("Designation", df_3["DESIGNATION"].unique()[0])
          modify_company_name = st.text_input("Company_name", df_3["COMPANY_NAME"].unique()[0])
          modify_contact = st.text_input("Contact", df_3["CONTACT"].unique()[0])
          modify_email = st.text_input("Email", df_3["EMAIL"].unique()[0])

          df_4["NAME"] = modify_name
          df_4["DESIGNATION"] = modify_designation
          df_4["COMPANY_NAME"] = modify_company_name
          df_4["CONTACT"] = modify_contact
          df_4["EMAIL"] = modify_email

        with col2:
          modify_website = st.text_input("Website", df_3["WEBSITE"].unique()[0])
          modify_address = st.text_input("Address", df_3["ADDRESS"].unique()[0])
          modify_pincode = st.text_input("Pincode", df_3["PINCODE"].unique()[0])
          modify_image = st.text_input("Image", df_3["IMAGE"].unique()[0])

          df_4["WEBSITE"] = modify_website
          df_4["ADDRESS"] = modify_address
          df_4["PINCODE"] = modify_pincode
          df_4["IMAGE"] = modify_image

        st.dataframe(df_4)

        col1,col2 = st.columns(2)
        with col1:
          button_3 = st.button("Modify", use_container_width= True)

        if button_3:

          mydb= sqlite3.connect("bixcard_db")
          cursor= mydb.cursor()

          cursor.execute(f"DELETE FROM bizcard_details WHERE NAME='{name}'")
          mydb.commit()

          # Insert Query

          insert_query_1= """INSERT INTO bizcard_details(name, designation, company_name, contact, email, website, address, pincode, image)

                            VALUES(?,?,?,?,?,?,?,?,?)"""

          sql_data = df_4.values.tolist()[0]
          cursor.execute(insert_query_1,sql_data)
          mydb.commit()

          st.success("SUCCESSFULLY MODIFIED!")




elif select == "Delete":

  mydb= sqlite3.connect("bixcard_db")
  cursor= mydb.cursor()

  col1,col2 = st.columns(2)
  with col1:

    select_query = "SELECT NAME FROM bizcard_details"

    cursor.execute(select_query)
    table1 = cursor.fetchall()
    mydb.commit()

    Names = []

    for i in table1:
      Names.append(i[0])

    select_name = st.selectbox("Select The Name", Names)

  with col2:

    select_query = f"SELECT DESIGNATION FROM bizcard_details WHERE NAME ='{select_name}'"

    cursor.execute(select_query)
    table2 = cursor.fetchall()
    mydb.commit()

    Designation = []

    for j in table2:
      Designation.append(j[0])

    select_designation = st.selectbox("Select The Designation", Designation)

  if select_name and select_designation:
    col1,col2,col3 = st.columns(3)

    with col1:
      st.write(f"Selected Name : {select_name}")
      st.write("")
      st.write("")
      st.write("")
      st.write(f"selected Designation : {select_designation}")

    with col2:
      st.write("")
      st.write("")
      st.write("")
      st.write("")

      Remove = st.button("DELETE", use_container_width= True)

      if Remove:

        cursor.execute(f"DELETE FROM bizcard_details WHERE NAME ='{select_name}' AND DESIGNATION ='{select_designation}'" )
        mydb.commit()

        st.warning("DELETED!")

