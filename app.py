import streamlit as st
import sqlite3
import openai

# 设置OpenAI API密钥
openai.api_key = 'your-openai-api-key'

# 连接到SQLite数据库
conn = sqlite3.connect('text_database.db')
cursor = conn.cursor()

# 从数据库中获取数据的函数
def search_data(query):
    cursor.execute("SELECT content FROM documents WHERE content LIKE ?", ('%' + query + '%',))
    rows = cursor.fetchall()
    return [row[0] for row in rows]

# 自然语言处理生成报告的函数
def generate_report(contents):
    prompt = "基于以下信息生成一份报告：\n" + "\n".join(contents)
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

# Streamlit应用
st.title('定制化报告生成器')

# 用户输入查询关键字
query = st.text_input('请输入查询关键字')

# 获取并显示数据
if st.button('生成报告'):
    results = search_data(query)
    if results:
        report = generate_report(results)
        st.subheader('生成的报告')
        st.write(report)
    else:
        st.write("没有找到相关内容")

# 关闭数据库连接
conn.close()
