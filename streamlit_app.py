import streamlit as st # type: ignore
import pandas as pd # type: ignore

from function import *

st.set_page_config(page_title="SiRinjani - BPS NTB", page_icon='assets/Logo.png', layout="wide")
st.logo('assets/Logo Long.png', icon_image='assets/Logo.png')

st.markdown(
    """
    <style>
        body {
            overflow-x: hidden;
            overflow-y: hidden; 
        }

        .stElementContainer[data-testid="stElementContainer"] hr {
            margin: 0.5em 0 1em 0;
        }

        .stMainBlockContainer {
            padding-top: 4rem;
            padding-bottom: 4rem;
        }

        img {
            border-radius: 5px;
        }

        .stMultiSelect [data-testid="stWidgetLabel"],
        .stTextInput [data-testid="stWidgetLabel"] {
            margin-top: -5px;
        }

        .stMultiSelect [data-testid="stMarkdownContainer"],
        .stSlider label[data-testid="stWidgetLabel"],
        .stTextInput label[data-testid="stWidgetLabel"] {
            padding-left: 5px;
            color: rgba(250, 250, 250, 0.6);
        }

        #MainMenu,
        footer,
        .stAppToolbar {
            visibility: hidden;
        }


    /**** Tabs ****/
        
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            justify-content: left;
            gap: 2px;
            width: 100%;
        }

        .stTabs [data-baseweb="tab"] {
            flex: 1; 
            height: 50px;
            border-radius: 4px 4px 0px 0px;
            gap: 25px;
            padding-top: 5px;
            padding-bottom: 10px;
            text-align: center;
            position: relative; 
            font-size: 18px;
            font-weight: 600;
        }

        .stTabs [data-baseweb="tab"]:focus,
        .stTabs [data-baseweb="tab"]:active,
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            outline: none;
        }

        .stTabs [data-baseweb="tab"]:after {
            content: ""; 
            display: block;
            height: 2px; 
            background-color: #007bff; 
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            transform: scaleX(0);
            transition: transform 0.3s ease; 
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"]:after {
            transform: scaleX(1); 
            background-image: linear-gradient(to right, #7375b6, #39a1b1);
            box-shadow: 0 0 10px rgba(57, 161, 177, 0.5);
            animation: glowing-underline 2s ease-in-out infinite;
        }

        @keyframes glowing-underline {
            0% {
                box-shadow: 0 0 10px rgba(57, 161, 177, 0.5);
            }
            50% {
                box-shadow: 0 0 30px rgba(57, 161, 177, 1); 
            }
            100% {
                box-shadow: 0 0 10px rgba(57, 161, 177, 0.5);
            }
        }
        

    /**** Nav Bar ****/

        [data-testid="stSidebarNavSeparator"] {
            display: none !important;
        }

        [data-testid="stSidebarUserContent"] {
            padding-top: 0rem;
        }

        [data-testid="stSidebarNavLink"] {
            display: flex;
            align-items: center;
            padding: 5px; 
            border-radius: 8px;
            padding-left: 5px;
            transition: all 0.3s ease;
        }

        [data-testid="stSidebarNavLink"][aria-current="page"] {
            background-color: #2b2b2d !important;
        }

        [data-testid="stSidebarNavLink"] span:nth-child(1) {
            margin-left: 5px;
            margin-right: 10px;
            font-weight: 500;
            font-size: 20px;
        }

        .element-container:has(iframe[height="0"]) {
            display: none;
        }


    /**** Select Box ****/

        .stSelectbox [data-testid="stWidgetLabel"] {
            margin-top: 0;
        }

        .stSelectbox [data-testid="stMarkdownContainer"] {
            padding-left: 5px;
            color: rgba(250, 250, 250, 0.6);
        }
      

    /**** Button ****/

        .stButton > button, 
        .stLinkButton > a {
            background-image: linear-gradient(to right, #7375b6, #39a1b1);
            line-height: 37px;
            color: white;
            font-size: 16px;
            border: none;
            padding: 10px 20px;
            border-radius: 10px;
            box-shadow: 0 0 5px rgba(57, 161, 177, 0.5);
            animation: glowing 2s ease-in-out infinite;
        }

        @keyframes glowing {
            0% {
                box-shadow: 0 0 5px rgba(57, 161, 177, 0.5);
            }
            50% {
                box-shadow: 0 0 10px rgba(57, 161, 177, 1);
            }
            100% {
                box-shadow: 0 0 5px rgba(57, 161, 177, 0.5);
            }
        }


    /**** Check Box ****/

        [data-testid="stCheckbox"] label > div:first-child > div { 
            background-image: linear-gradient(to right, #39a1b1, #7375b6);
            box-shadow: 0 0 10px rgba(57, 161, 177, 0.8); 
            border-radius: 4px; 
            animation: glowing 2s ease-in-out infinite;
        }

        [data-testid="stCheckbox"]:hover label > div:first-child > div {
            box-shadow: 0 0 30px rgba(57, 161, 177, 0.7); 
        }

        @keyframes glowing-checkbox {
            0% {
                box-shadow: 0 0 40px rgba(57, 161, 177, 1),
                            inset 0 0 20px rgba(255, 255, 255, 0.3);
            }
            50% {
                box-shadow: 0 0 60px rgba(57, 161, 177, 1),
                            inset 0 0 30px rgba(255, 255, 255, 0.5);
            }
            100% {
                box-shadow: 0 0 40px rgba(57, 161, 177, 1),
                            inset 0 0 20px rgba(255, 255, 255, 0.3);
            }
        }

        [data-testid="stCheckbox"] [data-testid="stMarkdownContainer"] p { 
            color: rgba(250, 250, 250, 0.6);
            transition: color 0.3s ease;
            font-size: 14px;
        }

        [data-testid="stCheckbox"] input:checked + div [data-testid="stMarkdownContainer"] p {
            color: #ffffff;
            font-weight: bold;
        }
    </style>
    """, 
    unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if 'dataset' not in st.session_state:
    st.session_state.dataset = None
if 'satker' not in st.session_state:
    st.session_state.satker = None
if 'bulan' not in st.session_state:
    st.session_state.bulan = None
if 'tahun' not in st.session_state:
    st.session_state.tahun = None

login_page      = st.Page(login, title="Log in")
logout_page     = st.Page(logout, title="Keluar", icon=":material/logout:")

dashboard       = st.Page("features/dashboard.py", title="Dashboard", icon=":material/dashboard:")
tabel           = st.Page("features/tabel.py", title="Tabel", icon=":material/table:")

if st.session_state.logged_in:
    
    pg = st.navigation({
        ' '      : [dashboard],
        'Menu'   : [
                    tabel
                   ],
        'Selesai' : [logout_page]
    })

else:
    pg = st.navigation([login_page])

pg.run()