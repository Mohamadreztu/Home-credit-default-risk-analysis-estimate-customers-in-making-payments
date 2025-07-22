import streamlit as st
import pandas as pd
import joblib
import os

# Load model safely using joblib
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'xgboost_model.pkl')
    if not os.path.exists(model_path):
        st.error(f"Model tidak ditemukan di path: {model_path}")
        st.stop()
    model = joblib.load(model_path)
    return model

model = load_model()

# Define prediction function
def credit_prediction(model, features):
    features_df = pd.DataFrame([features])
    prediction = model.predict(features_df)
    return prediction[0]

def main():
    st.set_page_config(page_title="Dashboard Analisis Resiko Pengajuan Kredit", layout="wide")

    st.markdown(
    """
    <style>
    .main {
        background-color: #95040A;
        color: white;
    }
    .custom-box {
        border: 2px solid white;
        padding: 20px;
        margin: 10px 0;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    st.image('Background Dashboard.jpg', use_container_width=True)

    st.markdown("""
    <div class="custom-box">
        <h4>Perhatian!</h4>
        <p>Sistem ini dirancang untuk membantu Anda dalam menganalisis risiko pengajuan kredit secara lebih mudah dan akurat.</p>
        <h6>Langkah-langkah penggunaan:</h6>
        <p>1. Masukkan data kriteria calon nasabah di sidebar. <br>
        2. Klik tombol "Prediksi Calon Nasabah" untuk melihat hasilnya.</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar inputs
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
    AGE_YEARS = st.sidebar.number_input('Usia (tahun)', min_value=0, step=1)
    YEARS_REGISTRATION = st.sidebar.number_input('Lama Registrasi (tahun)', min_value=0, step=1)
    EXT_SOURCE_1 = st.sidebar.number_input('Skor Status 1', min_value=0.0, step=0.01)
    EXT_SOURCE_2 = st.sidebar.number_input('Skor Status 2', min_value=0.0, step=0.01)
    EXT_SOURCE_3 = st.sidebar.number_input('Skor Status 3', min_value=0.0, step=0.01)

    # Preprocessing input values
    gender_code = 'M' if CODE_GENDER == 'Laki-laki' else 'F'
    flag_own_car = int(FLAG_OWN_CAR)
    flag_own_realty = int(FLAG_OWN_REALTY)
    reg_city_not_work_city = int(REG_CITY_NOT_WORK_CITY)

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

    if st.sidebar.button('Prediksi Calon Nasabah'):
        risk_status_num = credit_prediction(model, features_pred)
        risk_status_map = {
            0: "BERESIKO RENDAH",
            1: "BERESIKO MENENGAH",
            2: "BERESIKO TINGGI",
            3: "BERESIKO SANGAT TINGGI"
        }
        risk_status = risk_status_map.get(risk_status_num, "UNKNOWN RISK")

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

        st.subheader('Detail Kriteria Nasabah:')
        st.write(narrative)

        st.subheader('Status Pengajuan Kredit:')
        st.success(risk_status)

if __name__ == '__main__':
    main()
