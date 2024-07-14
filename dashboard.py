import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open('model/xgboost_model.pkl', 'rb'))

# Define prediction function
def credit_prediction(model, features):
    # Convert features to DataFrame
    features_df = pd.DataFrame([features])
    # Perform prediction
    prediction = model.predict(features_df)
    return prediction[0]

def main():
    # Set page config
    st.set_page_config(page_title="Dashboard Analisis Resiko Pengajuan Kredit", layout="wide")

    # Add custom CSS
    st.markdown(
    """
    <style>
    .main {
        background-color: #95040A;
        color: white;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

    # Create title and header
    st.markdown('<h1 class="custom-title">Dashboard Prediksi Pengajuan Kredit</h1>', unsafe_allow_html=True)

    # Add an image below the title
    st.image('Background Dashboard.jpg', use_column_width=True)

    st.sidebar.header("Kriteria Calon Kredit Nasabah")
    NAME_INCOME_TYPE = st.sidebar.selectbox('Tipe Pemasukan', ['Bekerja', 'Pengusaha', 'Pensiunan', 'Pengangguran', 'Pelajar', 'Cuti Melahirkan', 'Pegawai Negeri', 'Staff Komersial'])
    AMT_ANNUITY = st.sidebar.number_input('Jumlah Angsuran Wajib', min_value=0, step=1)
    NAME_EDUCATION_TYPE = st.sidebar.selectbox('Pendidikan Terakhir', ['SD', 'SMP', 'SMA', 'Sarjana', 'Gelar Akademis (S2-S3)'])
    AMT_INCOME_TOTAL = st.sidebar.number_input('Total Pendapatan Bulanan', min_value=0, step=1)
    AMT_CREDIT = st.sidebar.number_input('Jumlah Kredit', min_value=0, step=1)
    CODE_GENDER = st.sidebar.selectbox('Jenis Kelamin', ['Laki-laki', 'Perempuan'])
    AMT_GOODS_PRICE = st.sidebar.number_input('Nominal Aset Kepemilikan', min_value=0, step=1)
    CNT_CHILDREN = st.sidebar.number_input('Jumlah Anak', min_value=0, step=1)
    FLAG_OWN_CAR = st.sidebar.checkbox('Punya Mobil')
    FLAG_OWN_REALTY = st.sidebar.checkbox('Punya Properti')
    REG_CITY_NOT_WORK_CITY = st.sidebar.checkbox('Tinggal di Perkotaan')
    YEARS_EMPLOYED = st.sidebar.number_input('Lama Bekerja (tahun)', min_value=0, step=1)
    RATE_OF_LOAN = st.sidebar.number_input('Tingkat Suku Bunga', min_value=0.0, step=0.01)
    AGE_YEARS = st.sidebar.number_input('Usia (tahun)', min_value=0, step=1, format='%d')  # Integer input
    YEARS_REGISTRATION = st.sidebar.number_input('Lama Registrasi (tahun)', min_value=0, step=1)
    EXT_SOURCE_1 = st.sidebar.number_input('Berikan Skor Status 1', min_value=0.0, step=0.01)
    EXT_SOURCE_2 = st.sidebar.number_input('Berikan Skor Status 2', min_value=0.0, step=0.01)
    EXT_SOURCE_3 = st.sidebar.number_input('Berikan Skor Status 3', min_value=0.0, step=0.01)

    # Convert gender to required format
    gender_code = 'M' if CODE_GENDER == 'Laki-laki' else 'F'
    
    # Convert checkboxes to 1 or 0
    flag_own_car = 1 if FLAG_OWN_CAR else 0
    flag_own_realty = 1 if FLAG_OWN_REALTY else 0
    reg_city_not_work_city = 1 if REG_CITY_NOT_WORK_CITY else 0
    
    # Convert education type to required format
    education_mapping = {
        'SD': 'Incomplete higher',
        'SMP': 'Lower secondary',
        'SMA': 'Secondary / secondary special',
        'Sarjana': 'Higher education',
        'Gelar Akademis (S2-S3)': 'Academic degree'
    }
    education_type_converted = education_mapping[NAME_EDUCATION_TYPE]
    
    working_mapping = {
        'Bekerja': 'Working',
        'Pengusaha': 'Businessman',
        'Pensiunan': 'Pensioner',
        'Pengangguran': 'Unemployed',
        'Pelajar': 'Student',
        'Cuti Melahirkan': 'Maternity leave',
        'Pegawai Negeri': 'State servant',
        'Staff Komersial': 'Commercial associate'
    }
    working_type_converted = working_mapping[NAME_INCOME_TYPE]

    # Collect features
    features_pred = {
        'NAME_INCOME_TYPE': working_type_converted,
        'AMT_ANNUITY': AMT_ANNUITY,
        'NAME_EDUCATION_TYPE': education_type_converted,
        'AMT_INCOME_TOTAL': AMT_INCOME_TOTAL,
        'AMT_CREDIT': AMT_CREDIT,
        'CODE_GENDER': gender_code,
        'AMT_GOODS_PRICE': AMT_GOODS_PRICE,
        'CNT_CHILDREN': CNT_CHILDREN,
        'FLAG_OWN_CAR': flag_own_car,
        'FLAG_OWN_REALTY': flag_own_realty,
        'REG_CITY_NOT_WORK_CITY': reg_city_not_work_city,
        'YEARS_EMPLOYED': YEARS_EMPLOYED,
        'RATE_OF_LOAN': RATE_OF_LOAN,
        'AGE_YEARS': AGE_YEARS,
        'YEARS_REGISTRATION': YEARS_REGISTRATION,
        'EXT_SOURCE_1': EXT_SOURCE_1,
        'EXT_SOURCE_2': EXT_SOURCE_2,
        'EXT_SOURCE_3': EXT_SOURCE_3
    }

    # Create prediction button
    if st.sidebar.button('Prediksi Calon Nasabah'):
        risk_status_num = credit_prediction(model, features_pred)
        
        # Map the numeric prediction to descriptive risk categories
        risk_status_map = {
            0: "LOW RISK",
            1: "MEDIUM RISK",
            2: "HIGH RISK",
            3: "VERY HIGH RISK"
        }
        risk_status = risk_status_map.get(risk_status_num, "UNKNOWN RISK")
        
        # Display user inputs in a narrative format
        narrative = (
        f"Calon kredit nasabah dengan status pemasukan {NAME_INCOME_TYPE}, "
        f"dan pendidikan terakhirnya adalah {NAME_EDUCATION_TYPE}, "
        f"berjenis kelamin {CODE_GENDER}, "
        f"total pendapatan bulanan {AMT_INCOME_TOTAL}, "
        f"sebelumnya memiliki jumlah kredit {AMT_CREDIT}, "
        f"nominal aset yang dimiliki {AMT_GOODS_PRICE}, "
        f"memiliki jumlah anak {CNT_CHILDREN}, "
        f"{'punya mobil' if FLAG_OWN_CAR else 'tidak punya mobil'}, "
        f"{'punya properti' if FLAG_OWN_REALTY else 'tidak punya properti'}, "
        f"{'tinggal di perkotaan' if REG_CITY_NOT_WORK_CITY else 'tidak tinggal di perkotaan'}, "
        f"sudah bekerja {YEARS_EMPLOYED} tahun, "
        f"tingkat suku bunga yang diharapkan {RATE_OF_LOAN}, "
        f"usia {AGE_YEARS} tahun, "
        f"sudah terdaftar sejak {YEARS_REGISTRATION} tahun."
        )
        
        # Display prediction result
        st.subheader('Detail Kriteria Nasabah:')
        st.write(narrative)
        
        st.subheader('Status Pengajuan Kredit:')
        st.success(risk_status)
        
if __name__ == '__main__':
    main()
