import streamlit as st      
import joblib
import xgboost as xgb
import numpy as np
import base64
import os

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
single_model = load_model("single_model.json")
group_model = load_model("group_model.json")

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
        焊钉连接件抗剪承载力预测平台<br>
        <span style='font-size: 26px; font-weight: normal;'>Prediction Platform for the Shear Bearing Capacity of Stud Connectors</span>
    </h1>
    """, unsafe_allow_html=True)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(os.path.dirname(current_dir), "2.png")
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
    <div style="flex: 3; font-size: 24px; line-height: 1.8; text-align: justify; color: #333; padding-right: 30px;">
        基于机器学习算法（XGBoost），结合639个单钉推出试验和193个群钉推出试验的数据库，
        部署为在线预测平台，
        该平台能够快速预测单钉与群钉连接件的抗剪承载力。
        用户只需输入几何与材料参数，即可获得预测结果。
    </div>
    <div style="flex: 2; text-align: center;">
        <img src="data:image/png;base64,{encoded}"
             style="width:100%; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.25);">
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<p style="font-size:24px; font-weight:bold;">请选择模型类型：</p>', unsafe_allow_html=True)

model_type = st.selectbox(
    "模型选择",  # 非空 label
    ("单钉模型", "群钉模型"),
    label_visibility="collapsed"  # 隐藏原 label
)

# --- 辅助函数：统一标签样式 ---
# 修改后的函数定义，支持 4 个参数：名称、主符号、下标、单位
def label_html(text, symbol="", subscript="", unit=""):
    """
    text: 中文名称 (如: 开孔直径)
    symbol: 主符号 (如: d)
    subscript: 下标 (如: p)
    unit: 单位 (如: mm)
    """
    sub_str = f'<sub>{subscript}</sub>' if subscript else ""
    unit_str = f' <span style="font-style:normal;">({unit})</span>' if unit else ""
    return f'<p style="font-size:26px; margin-bottom:-10px; white-space:nowrap;">{text} <i>{symbol}</i>{sub_str}{unit_str}</p>'

st.markdown("#### 输入参数")

# 开启三列网格
col1, col2, col3 = st.columns(3)

# --- 第一列 ---
with col1:
    st.markdown(label_html("焊钉直径", "d", "s", "mm"), unsafe_allow_html=True)
    ds = st.number_input("ds_v", 10.0, 40.0, 22.0, key="ds_k", label_visibility="collapsed")
    
    st.markdown(label_html("焊钉高度", "h", "s", "mm"), unsafe_allow_html=True)
    hs = st.number_input("hs_v", 50.0, 500.0, 200.0, key="hs_k", label_visibility="collapsed")

    st.markdown(label_html("混凝土弹模", "E", "c", "GPa"), unsafe_allow_html=True)
    Ec = st.number_input("Ec_v", 20.0, 60.0, 30.0, key="Ec_k", label_visibility="collapsed")

    st.markdown(label_html("混凝土抗压强度", "f", "cu", "MPa"), unsafe_allow_html=True)
    fcu = st.number_input("fcu_v", 20.0, 80.0, 50.0, key="fcu_k", label_visibility="collapsed")

# --- 第二列 ---
with col2:
    st.markdown(label_html("焊钉屈服强度", "f", "ys", "MPa"), unsafe_allow_html=True)
    fys = st.number_input("fys_v", 200.0, 700.0, 400.0, key="fys_k", label_visibility="collapsed")

    st.markdown(label_html("焊钉抗拉强度", "f", "ts", "MPa"), unsafe_allow_html=True)
    fts = st.number_input("fts_v", 200.0, 600.0, 450.0, key="fts_k", label_visibility="collapsed")

    # 只有是群钉模型时才显示的参数
    if model_type == "群钉模型":
        st.markdown(label_html("纵向间距", "l", "z", "mm"), unsafe_allow_html=True)
        lz = st.number_input("lz_v", 0.0, 400.0, 100.0, key="lz_k", label_visibility="collapsed")

        st.markdown(label_html("焊钉层数", "n", "z", ""), unsafe_allow_html=True)
        nz = st.number_input("nz_v", 0.0, 30.0, 2.0, key="nz_k", label_visibility="collapsed")
    else:
        # 必须在这里初始化，否则单钉模型下 X 数组会找不到变量
        lz, nz = None, None

# --- 第三列 ---
with col3:
    if model_type == "群钉模型":
        st.markdown(label_html("横向间距", "l", "h", "mm"), unsafe_allow_html=True)
        lh = st.number_input("lh_v", 0.0, 400.0, 80.0, key="lh_k", label_visibility="collapsed")

        st.markdown(label_html("焊钉列数", "n", "h", ""), unsafe_allow_html=True)
        nh = st.number_input("nh_v", 0.0, 30.0, 2.0, key="nh_k", label_visibility="collapsed")
    else:
        # 同理初始化
        lh, nh = None, None

st.write("---")

# 计算按钮
if st.button("计算抗剪承载力"):
    if model_type == "单钉模型":
        X = np.array([[ds, hs, Ec, fcu, fys, fts]])
        y_pred = single_model.predict(X)[0]
    else:
        X = np.array([[ds, hs, lz, nz, lh, nh, Ec, fcu, fys, fts]])
        y_pred = group_model.predict(X)[0]
    st.success(f"预测抗剪承载力: {y_pred:.2f} kN")
