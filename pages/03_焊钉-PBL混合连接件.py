import streamlit as st      
import joblib
import xgboost as xgb
import numpy as np
import base64
import os

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
set_background("1.jpg")  # 这里写你的图片名

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
    font-size: 24px !important;
}

/* ---- 输入框区域 ---- */
input, select, textarea, label, div, span {
    font-family: 'Times New Roman', 'SimSun', serif !important;
    font-size: 24px !important;
}

/* 参数说明与输入框间距 */
.stNumberInput > label, .stMarkdown {
    margin-bottom: 2px !important;
}

/* 输入框内部间距缩小 */
.stNumberInput>div>div>div>input {
    font-size: 24px !important;      /* 控制字体大小 */
    padding: 6px 12px !important;    /* 控制内部上下左右间距 */
    height: 48px !important; 
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ---- selectbox 高度和宽度 ---- */
div[data-baseweb="select"] > div {
    min-height: 50px !important;  /* 控制外框高度 */
    width: 220px !important;      /* 控制宽度 */
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
st.title("Stud-PBL混合连接件抗剪承载力预测平台 Prediction Platform for the Shear Bearing Capacity of Stud-PBL Hybrid Connectors")

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(os.path.dirname(current_dir), "4.png")
with open(file_path, "rb") as f:
    data = f.read()
encoded = base64.b64encode(data).decode()

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
        用户只需输入几何与材料参数，即可获得预测结果。(注：无贯穿钢筋时，dr和fyr取0)
    </div>
    <div style="flex: 0 0 260px; margin-left: 40px;">
        <img src="data:image/png;base64,{encoded}"
             style="width:100%; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.25);">
    </div>
</div>
""", unsafe_allow_html=True)

# 输入参数（论文风格下标）
st.markdown("#### 输入参数")

# 单钉参数
st.markdown('<p style="font-size:26px;">焊钉直径 <i>d</i><sub>s</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
ds = st.number_input("ds", min_value=10.0, max_value=30.0, step=1.0, label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">焊钉高度 <i>h</i><sub>s</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
hs = st.number_input("hs", min_value=50.0, max_value=100.0, step=1.0, label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">开孔直径 <i>d</i><sub>p</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
dp = st.number_input("dp", min_value=25.0, max_value=80.0, step=1.0, label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">开孔板高度 <i>h</i><sub>p</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
hp = st.number_input("dp", min_value=80.0, max_value=160.0, step=1.0, label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">贯穿钢筋直径 <i>d</i><sub>r</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
dr = st.number_input("dr", min_value=0.0, max_value=28.0, step=1.0, label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">单侧焊钉总数 <i>n</i>', unsafe_allow_html=True)
n = st.number_input("n", min_value=1.0, max_value=4.0, step=1.0, label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">焊钉直径 <i>a</i><sub>s</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
as = st.number_input("as", min_value=50.0, max_value=205.0, step=0.1, label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">焊钉中与PBL孔中心横向间距(垂直于剪力方向) <i>h</i><sub>sp</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
hsp = st.number_input("dr", min_value=40.0, max_value=150.0, step=0.1, label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">焊钉中与PBL孔中心横向间距(沿剪力方向) <i>l</i><sub>sp</sub> <span style="font-style:normal;">(mm)</span></p>', unsafe_allow_html=True)
lsp = st.number_input("dr", min_value=40.0, max_value=120.0, step=0.1, label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">PBL开孔数量 <i>n</i><sub>p</sub>', unsafe_allow_html=True)
np = st.number_input("np", min_value=1.0, max_value=0.0, step=1.0, label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">混凝土立方体抗压强度 <i>f</i><sub>cu</sub> <span style="font-style:normal;">(MPa)</span></p>', unsafe_allow_html=True)
fcu = st.number_input("fcu", min_value=30.0, max_value=85.0, step=0.1, key="fcu", label_visibility="collapsed")

st.markdown('<p style="font-size:26px;">贯穿钢筋的屈服强度 <i>f</i><sub>yr</sub> <span style="font-style:normal;">(MPa)</span></p>', unsafe_allow_html=True)
fyr = st.number_input("fyr", min_value=0.0, max_value=500.0, step=0.1, key="fsy", label_visibility="collapsed")


# 计算按钮
if st.button("计算抗剪承载力"):
    X = np.array([[ds, hs, dp, hp, dr, n, as, hsp, lsp, np, fcu, fyr]])
    y_pred = stud_PBL_model.predict(X)[0]
    
    st.success(f"预测抗剪承载力: {y_pred:.2f} kN")
