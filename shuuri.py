import streamlit as st

# 料金データ（元のJavaScriptデータを完全再現）
price_data = {
    "国産時計": {
        "SEIKO（一般）": {"quartz3": 11000, "quartzChrono": 15400, "mechanical3": 15400, "mechanicalChrono": 17600},
        "SEIKO（DOLCE/EXCELINE/LASSALE）": {"quartz3": 15400, "quartzChrono": 16500, "mechanical3": 17600, "mechanicalChrono": 19800},
        "SEIKO（GS・CREDOR）": {"quartz3": 33000, "quartzChrono": 38500, "mechanical3": 44000, "mechanicalChrono": 48400},
        "CITIZEN": {"quartz3": 11000, "quartzChrono": 15400, "mechanical3": 15400, "mechanicalChrono": 17600},
        "CITIZEN（EXCEED）": {"quartz3": 15400, "quartzChrono": 16500, "mechanical3": 17600, "mechanicalChrono": 19800},
        "CASIO": {"quartz3": 11000, "quartzChrono": 15400, "mechanical3": 15400, "mechanicalChrono": 17600},
        "ORIENT": {"quartz3": 11000, "quartzChrono": 15400, "mechanical3": 15400, "mechanicalChrono": 17600},
        "その他国産": {"quartz3": 11000, "quartzChrono": 15400, "mechanical3": 15400, "mechanicalChrono": 17600}
    },
    "舶来時計": {
        "グループA（CYMA、ETERNA、ENICAR、FENDI、NINARICCI等）": {"quartz3": 27500, "quartzChrono": 33000, "mechanical3": 36300, "mechanicalChrono": 44000},
        "グループB（DIOR、DUNHILL、GUCCI、HAMILTON、HUNTING WORLD、LONGINES等）": {"quartz3": 30800, "quartzChrono": 38500, "mechanical3": 49500, "mechanicalChrono": 55000},
        "グループC（CHANEL、EBEL、HERMES、JUVENIA等）": {"quartz3": 33000, "quartzChrono": 38500, "mechanical3": 55000, "mechanicalChrono": 66000},
        "グループD（BREITLING、BAUME & MERCIER、CARTIER、CORUM、FRANK MULLER等）": {"quartz3": 38500, "quartzChrono": 44000, "mechanical3": 66000, "mechanicalChrono": 77000},
        "グループE（AUDEMARS PIGUET、CHOPARD、PATEK PHILIPPE等）": {"quartz3": 66000, "quartzChrono": 77000, "mechanical3": 110000, "mechanicalChrono": 132000}
    },
    "OMEGA・TAG HEUER": {
        "OMEGA": {"quartz3": 33000, "quartzChrono": 38500, "mechanical3": 49500, "mechanicalChrono": 55000},
        "TAG HEUER": {"quartz3": 38500, "quartzChrono": 44000, "mechanical3": 66000, "mechanicalChrono": 77000}
    },
    "ROLEX": {
        "ROLEX": {"quartz3": 49500, "quartzChrono": 55000, "mechanical3": 77000, "mechanicalChrono": 88000}
    }
}

# 初期化
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'selections' not in st.session_state:
    st.session_state.selections = {}

# カスタムCSS（元のデザインを再現）
st.markdown("""
<style>
.step-counter { color: #7f8c8d; margin-bottom: 10px; }
.card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
.option-btn { padding: 15px 20px; border: 2px solid #3498db; border-radius: 8px; margin-bottom: 10px; cursor: pointer; }
.option-btn:hover { background: #3498db; color: white; }
.selected { background: #3498db !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# ステップ管理
def render_step():
    steps = [
        {
            "title": "大分類を選択してください",
            "options": ["国産時計", "舶来時計", "OMEGA・TAG HEUER", "ROLEX"],
            "key": "category"
        },
        {
            "title": "ブランド・価格帯を選択してください",
            "options": lambda: list(price_data[st.session_state.selections["category"]].keys()),
            "key": "brand"
        },
        {
            "title": "機構を選択してください",
            "options": ["クォーツ 3針", "クォーツ クロノグラフ", "メカニカル 3針", "メカニカル クロノグラフ"],
            "key": "mechanism"
        },
        {
            "title": "特殊仕様を選択してください",
            "options": [
                {"label": "シースルーバック（+2,200円）", "value": "seethrough", "price": 2200},
                {"label": "OMEGA コーアクシャル（+11,000円）", "value": "coaxial", "price": 11000, "condition": lambda: st.session_state.selections.get("brand") == "OMEGA"}
            ],
            "key": "special",
            "type": "checkbox"
        },
        {
            "title": "磨きオプションを選択してください",
            "options": [
                {"label": "ライトポリッシュ（3連）", "price": 6600},
                {"label": "ライトポリッシュ（5連）", "price": 8800},
                {"label": "新品仕上げ（3連）", "price": 11000},
                {"label": "新品仕上げ（5連）", "price": 13200}
            ],
            "key": "polish",
            "type": "checkbox",
            "condition": lambda: st.session_state.selections.get("category") in ["ROLEX", "OMEGA"]
        }
    ]
    
    current_step_data = steps[st.session_state.current_step - 1]
    
    with st.container():
        st.markdown(f'<div class="card"><div class="step-counter">ステップ {st.session_state.current_step}/5</div>', unsafe_allow_html=True)
        st.subheader(current_step_data["title"])
        
        if current_step_data.get("type") == "checkbox":
            selected = []
            for option in current_step_data["options"]:
                if "condition" in option and not option["condition"]():
                    continue
                if st.checkbox(option["label"], key=option["value"]):
                    selected.append(option)
            st.session_state.selections[current_step_data["key"]] = selected
        else:
            col1, col2 = st.columns(2)
            options = current_step_data["options"]() if callable(current_step_data["options"]) else current_step_data["options"]
            for i, option in enumerate(options):
                btn = col1.button(option, key=f"{current_step_data['key']}_{i}", use_container_width=True)
                if btn:
                    st.session_state.selections[current_step_data["key"]] = option
                    st.session_state.current_step += 1
                    st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# メイン処理
def main():
    st.title("修理料金案内アシスト")
    
    if st.session_state.current_step <= 4:
        render_step()
    else:
        show_result()

# 結果表示
def show_result():
    # 計算ロジック（元のJavaScriptを完全再現）
    category = st.session_state.selections["category"]
    brand = st.session_state.selections["brand"]
    mechanism = st.session_state.selections["mechanism"]
    
    mechanism_key = {
        "クォーツ 3針": "quartz3",
        "クォーツ クロノグラフ": "quartzChrono",
        "メカニカル 3針": "mechanical3",
        "メカニカル クロノグラフ": "mechanicalChrono"
    }[mechanism]
    
    base_price = price_data[category][brand][mechanism_key]
    
    # 保証期間計算
    warranty = "1年"
    if category == "国産時計" and "GS" in brand:
        warranty = "2年"
    elif category in ["舶来時計", "OMEGA・TAG HEUER", "ROLEX"] and "mechanical" in mechanism_key:
        warranty = "2年"
    
    # 結果表示
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("修理料金計算結果")
        st.markdown(f"""
        - 分類: {category}
        - ブランド: {brand}
        - 機構: {mechanism}
        - 基本料金: ¥{base_price:,}〜
        - 保証期間: {warranty}
        """)
        
        # 磨きオプション表示
        if "polish" in st.session_state.selections:
            st.markdown("---")
            st.write("※磨きの対応可否や詳細は修理業者判断の場合があります")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
