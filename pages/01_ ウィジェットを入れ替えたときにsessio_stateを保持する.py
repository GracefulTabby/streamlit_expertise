import streamlit as st


def cb_btn_on_click():
    st.session_state.address = "東京都新宿区xxxタワービル"


def session_state_resave():
    """widgetKeyを介したウィジェットの入力値を保持させる
    - 問題
      - radioボタンなどを使用しウィジェットの構成を変えるとsession_stateが保持されない
    - 発生条件
      - ウィジェットキーを設定して入力値を保持している
      - ①ウィジェットを選択条件によって描画の有無を切り替える
        1. ウィジェットを描画状態で、入力する
        2. ウィジェットを条件選択で一度オフにする（radio切り替える等）
        3. 再度描画する
      - ②ウィジェットが描画されていない状態でsession_stateを書き換えた後、描画する
    - 症状
      - ウィジェットにsession_stateを介して上書きした内容が表示されず空になる
    - 対応
      - session_state.updateで一度session_stateをすべて置き換える（内容は全く同じ）

    参考:https://discuss.streamlit.io/t/keyed-widget-state-persistence-discussion-possible-fixes/37359/6
    """
    st.session_state.update(st.session_state)


"""
- 問題
    - radioボタンなどを使用しウィジェットの構成を変えるとsession_stateが保持されない
- 発生条件
    - ウィジェットキーを設定して入力値を保持している
    - ①ウィジェットを選択条件によって描画の有無を切り替える
        1. ウィジェットを描画状態で、入力する
        2. ウィジェットを条件選択で一度オフにする（radio切り替える等）
        3. 再度描画する
    - ②ウィジェットが描画されていない状態でsession_stateを書き換えた後、描画する
- 症状
    - ウィジェットキーに紐づくsession_stateの書き込んだ内容が表示されない
    - ウィジェットの構成が変わるとそもそもsesson_stateのキーがなくなる
- 対応
    - session_state.updateで一度session_stateをすべて置き換える（内容は全く同じ）
"""

with st.expander("セッションステートの中身", expanded=True):
    st.write(st.session_state)

st.info(
    """
### 症状の再現方法
1. 指定方法１を選択した状態で住所を入力（ボタンを押しても入力する）
2. 指定方法２を選択
3. 指定方法１or３を選択すると、住所の入力が消えてしまっている

### session_stateの状態について
- 指定方法のラジオボタンを切り替えることでsession_stateが消えていることがわかる
- 対策をオンにすると消えずに、
"""
)

measures = st.radio("対策オンオフ", ["off", "on"], horizontal=True)

if measures == "on":
    measures_func = session_state_resave
else:
    measures_func = None

radio_select = st.radio(
    "指定方法",
    options=["1", "2", "3"],
    on_change=measures_func,
)


if radio_select == "1":
    st.text_input("電話番号", key="tel")
    st.text_input("住所", key="address")
    st.button("住所を入力する", on_click=cb_btn_on_click)

elif radio_select == "2":
    st.text_input("国名", key="contry")

elif radio_select == "3":
    st.text_input("住所", key="address")


with st.expander("セッションステートの中身", expanded=True):
    st.write(st.session_state)
