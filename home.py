import streamlit as st
import base64
import os

# 1. 页面基本配置
st.set_page_config(
    page_title="钢-混组合结构连接件抗剪承载力在线预测平台",
    page_icon="🏗️",
    layout="wide"
)

# 2. 背景图设置函数 (复用你之前的逻辑)
def set_background(image_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 注意：如果图片在 assets 文件夹，路径需改为 os.path.join(current_dir, "assets", image_name)
    image_path = os.path.join(current_dir, "assets", image_name) 

    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        img_base64 = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{img_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background-color: rgba(255, 255, 255, 0.6); /* 主页背景建议稍微浅一点 */
                z-index: -1;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# 调用背景 (确保 assets 文件夹里有这幅图)
set_background("1.jpg")

# 3. 主页标题与欢迎语
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="font-size: 42px; color: #1E3A8A; font-family: 'SimSun';">
            🏗️ 钢-混组合结构连接件抗剪承载力在线预测平台
        </h1>
        <p style="font-size: 24px; color: #333; margin-top: 10px;">
            Online Prediction Platform for Shear Capacity of Connectors in Steel-Concrete Composite Structures
        </p>
    </div>
    <hr style="border: 1px solid #1E3A8A;">
""", unsafe_allow_html=True)

# 4. 平台功能板块介绍
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style="background-color: rgba(255,255,255,0.8); padding: 20px; border-radius: 15px; height: 300px; border-left: 5px solid #1E3A8A; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color: #1E3A8A;">📌 01_焊钉连接件</h3>
            <p style="font-size: 18px; line-height: 1.6;">
                支持单钉及群钉连接件的抗剪承载力预测。<br>
                考虑直径、高度、间距及材料强度等多种参数影响。
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background-color: rgba(255,255,255,0.8); padding: 20px; border-radius: 15px; height: 300px; border-left: 5px solid #1E3A8A; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color: #1E3A8A;">📌 02_PBL连接件</h3>
            <p style="font-size: 18px; line-height: 1.6;">
                针对开孔钢板（PBL）连接件进行精准预测。<br>
                涵盖孔径、板厚、贯穿钢筋及混凝土强度的综合作用。
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style="background-color: rgba(255,255,255,0.8); padding: 20px; border-radius: 15px; height: 300px; border-left: 5px solid #1E3A8A; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h3 style="color: #1E3A8A;">📌 03_焊钉-PBL混合连接件</h3>
            <p style="font-size: 18px; line-height: 1.6;">
                结合焊钉与PBL优点的混合型连接件预测。<br>
                适用于复杂组合结构的高级工程设计需求。
            </p>
        </div>
    """, unsafe_allow_html=True)

# 5. 操作指南
st.markdown("""
    <div style="margin-top: 40px; padding: 20px; background-color: rgba(30, 58, 138, 0.1); border-radius: 10px;">
        <h4 style="color: #1E3A8A;">👈 使用指南 (User Guide)</h4>
        <ul style="font-size: 20px; line-height: 2;">
            <li>点击左侧侧边栏的 <b>"Pages"</b> 菜单展开选项。</li>
            <li>根据实际工程需求选择对应的连接件模型。</li>
            <li>在预测页面输入几何参数与材料性能，点击 <b>"计算抗剪承载力"</b> 获取结果。</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# 6. 页脚信息
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #666; font-size: 14px;">
        基于 XGBoost 机器学习算法提供技术支持
    </div>
""", unsafe_allow_html=True)