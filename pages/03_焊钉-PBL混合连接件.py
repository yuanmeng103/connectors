import streamlit as st      
import joblib
import xgboost as xgb
import numpy as np
import base64
import os
import pandas as pd

st.set_page_config(layout="wide")

def set_background(image_name):
    # 获取脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, image_name)

    if not os.path.exists(image_path):
        st.error(f"找不到背景图片: {image_path}")
        return

    # 1️⃣ 读取图片并生成 base64
    with open(image_path, "rb") as f:
        data = f.read()
    img_base64 = base64.b64encode(data).decode()  # ✅ 一定要在 f-string 前生成

    # 2️⃣ 注入 CSS
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        /* 背景浅化 */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.3); /* 越大越浅 */
            z-index: -1;
        }}

        /* 控件半透明背景 */
        .stBlock {{
            background: rgba(255, 255, 255, 0.3);
            padding: 1rem;
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- 调用背景图 ----------------
set_background("../1.png")  # 这里写你的图片名

def load_model(model_filename):
    # 获取当前文件（即子页面 .py）的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 向上跳一级到根目录，然后进入 models 文件夹
    model_path = os.path.join(os.path.dirname(current_dir), "models", model_filename)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"{model_path} 不存在")
    
    model = xgb.XGBRegressor()
    model.load_model(model_path)
    return model

# —— 调用函数 —— 
stud_PBL_model = load_model("stud_PBL_model.json")

# 全局样式：统一字体、大小、加粗，并缩小参数说明与输入框的间距
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'SimSun', 'Times New Roman', serif !important;
}

/* 平台标题 */
.stTitle {
    font-size: 32px !important;
    font-weight: bold !important;
}

/* 平台说明文字 */
.stMarkdown div[style*="line-height"] {
    font-size: 26px !important;
}

/* ---- 输入框区域 ---- */
input, select, textarea, label, div, span {
    font-family: 'Times New Roman', 'SimSun', serif !important;
    font-size: 30px !important;
}

/* 参数说明与输入框间距 */
.stNumberInput > label, .stMarkdown {
    margin-bottom: 2px !important;
}

/* 输入框内部间距缩小 */
.stNumberInput>div>div>div>input {
    font-size: 28px !important;    /* 匹配上面的大小 */
    height: 60px !important;       /* 字体变大后，高度也要相应增加，比如从 48px 改为 60px */
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ---- selectbox 高度和宽度 ---- */
div[data-baseweb="select"] > div {
    min-height: 60px !important;  /* 增加高度 */
    width: 300px !important;      /* 增加宽度，防止文字挤压 */
}

div[data-baseweb="select"] input {
    font-size: 28px !important;   /* 增大字体 */
}

/* selectbox 显示区域字体和高度 */
div[data-baseweb="select"] input {
    font-size: 24px !important;   /* 字体大小 */
    height: 48px !important;      /* 高度 */
    padding: 6px 12px !important; /* 内部间距 */
}

/* 下拉选项字体大小 */
div[data-baseweb="select"] ul li {
    font-size: 24px !important;
}

/* ---- st.success 输出框内字体大小 ---- */
div[data-testid="stSuccess"] div[data-testid="stMarkdownContainer"] {
    font-size: 28px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# 平台标题
st.markdown("""
    <h1 style='text-align: center; line-height: 1.2;'>
        焊钉-PBL混合连接件抗剪承载力预测平台<br>
        <span style='font-size: 26px; font-weight: normal;'>Prediction Platform for the Shear Bearing Capacity of Stud-PBL Hybrid Connectors</span>
    </h1>
    """, unsafe_allow_html=True)

curr_d = os.path.dirname(os.path.abspath(__file__))
root_d = os.path.dirname(curr_d)
f_ptr = os.path.join(root_d, "4.png")

if os.path.exists(f_ptr):
    with open(f_ptr, "rb") as f:
        img_data = f.read()
    encoded = base64.b64encode(img_data).decode()
else:
    st.error(f"找不到文件: {f_ptr}")
    encoded = ""

# --- 优雅布局 ---
st.markdown(f"""
<div style="
    background-color: #f8f9fa;
    border-radius: 15px;
    padding: 25px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
">
    <div style="flex: 1; font-size: 24px; line-height: 1.8; text-align: justify; color: #333;">
        基于机器学习算法（XGBoost），结合98个焊钉-PBL混合连接件有限元和推出试验数据库，
        部署为在线预测平台，
        该平台能够快速预测焊钉-PBL混合连接件的抗剪承载力。
        用户只需输入几何与材料参数，即可获得预测结果。(注：端部是否承压：0-端部不承压，1-端部承压。无贯穿钢筋时，<i>d</i><sub>r</sub> 和 <i>f</i><sub>yr</sub> 取 0)
    </div>
    <div style="flex: 0 0 260px; margin-left: 40px;">
        <img src="data:image/png;base64,{encoded}"
             style="width:100%; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.25);">
    </div>
</div>
""", unsafe_allow_html=True)

# 输入参数（论文风格下标）
st.markdown("#### 输入参数")

# --- 开启三列网格 ---
col1, col2, col3 = st.columns(3)

with col1:
    # 1. 焊钉直径
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">焊钉直径 <i>d</i><sub>s</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
    ds = st.number_input("ds_val", 10.0, 30.0, 22.0, step=1.0, key="ds_k", label_visibility="collapsed")

    # 2. 开孔直径
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">开孔直径 <i>d</i><sub>p</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
    dp = st.number_input("dp_val", 25.0, 80.0, 60.0, step=1.0, key="dp_k", label_visibility="collapsed")

    # 3. 贯穿钢筋直径
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">贯穿钢筋直径 <i>d</i><sub>r</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
    dr = st.number_input("dr_val", 0.0, 28.0, 20.0, step=1.0, key="dr_k", label_visibility="collapsed")

    # 4. 垂直剪力间距
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">焊钉和PBL横向间距 <i>h</i><sub>sp</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
    hsp = st.number_input("hsp_val", 40.0, 400.0, 100.0, step=0.1, key="hsp_k", label_visibility="collapsed")

with col2:
    # 5. 焊钉高度
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">焊钉高度 <i>h</i><sub>s</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
    hs = st.number_input("hs_val", 50.0, 300.0, 200.0, step=1.0, key="hs_k", label_visibility="collapsed")

    # 6. 开孔板高度
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">开孔板高度 <i>h</i><sub>p</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
    hp = st.number_input("hp_val", 80.0, 200.0, 130.0, step=1.0, key="hp_k", label_visibility="collapsed")

    # 7. 单侧焊钉总数
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">单侧焊钉总数 <i>n</i></p>', unsafe_allow_html=True)
    n = st.number_input("n_val", 1.0, 10.0, 2.0, step=1.0, key="n_k", label_visibility="collapsed")

    # 8. 沿剪力方向间距
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">焊钉和PBL纵向间距 <i>l</i><sub>sp</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
    lsp = st.number_input("lsp_val", 40.0, 150.0, 80.0, step=0.1, key="lsp_k", label_visibility="collapsed")

with col3:
    # 9. PBL开孔数量
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">PBL开孔数量 <i>n</i><sub>p</sub></p>', unsafe_allow_html=True)
    n_p = st.number_input("np_val", 1.0, 6.0, 1.0, step=1.0, key="np_k", label_visibility="collapsed")

    # 10. 混凝土抗压强度
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">混凝土立方体抗压强度 <i>f</i><sub>cu</sub> <span style="font-style:normal;">(MPa)</span></p>', unsafe_allow_html=True)
    fcu = st.number_input("fcu_val", 30.0, 85.0, 50.0, step=0.1, key="fcu_k", label_visibility="collapsed")

    # 11. 钢筋屈服强度
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">钢筋屈服强度 <i>f</i><sub>yr</sub> <span style="font-style:normal;">(MPa)</span></p>', unsafe_allow_html=True)
    fyr = st.number_input("fyr_val", 0.0, 500.0, 400.0, step=0.1, key="fyr_k", label_visibility="collapsed")

    # 12. 端部是否承压
    st.markdown('<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">端部是否承压  Bearing_Flag</p>', unsafe_allow_html=True)
    Bearing_Flag = st.number_input("Bearing_Flag_input", 0, 1, 0, step=1, key="flag_k", label_visibility="collapsed")

st.write("---")

# 计算按钮
if st.button("计算抗剪承载力"):
    # 1. 显式定义特征列名，必须和 Excel 表头完全一致
    cols = ['ds', 'hs', 'dp', 'hp', 'dr', 'n', 'hsp', 'lsp', 'n_p', 'fcu', 'fyr', 'Bearing_Flag']
    
    # 2. 构造 DataFrame (这样模型会按名字认人，不按排队顺序)
    X_input = pd.DataFrame([[ds, hs, dp, hp, dr, n, hsp, lsp, n_p, fcu, fyr, Bearing_Flag]], 
                           columns=cols)
    
    # 3. 调试：看看传进去的到底长啥样
    # st.write(X_input) 
    
    # 4. 预测
    y_pred = stud_PBL_model.predict(X_input)[0]
    st.success(f"预测抗剪承载力: {y_pred:.2f} kN")
