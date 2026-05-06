import streamlit as st
import preprocessor
import helper
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="WhatsApp Chat Analyser",
    page_icon="💬",
    layout="wide"
)

# ----------------- Custom CSS -----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}

.stApp {
    background-color: #0d1117;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1f3c;
    border-right: 1px solid #1e3a5f;
}
section[data-testid="stSidebar"] * {
    color: #cdd9e5 !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #1f6feb, #388bfd);
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    width: 100%;
    padding: 0.6rem;
    transition: opacity 0.2s;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    opacity: 0.88;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #161b27;
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 16px !important;
}
[data-testid="metric-container"] label {
    color: #58a6ff !important;
    font-weight: 600;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e6edf3 !important;
    font-weight: 800;
    font-size: 1.8rem !important;
}

/* Headings */
h1, h2, h3 {
    color: #e6edf3 !important;
}

/* Upload widget */
[data-testid="stFileUploader"] {
    background: #161b27;
    border: 2px dashed #1f6feb;
    border-radius: 12px;
    padding: 12px;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #161b27 !important;
    border-color: #1f6feb !important;
    border-radius: 10px !important;
    color: #e6edf3 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Divider */
hr {
    border-color: #1e3a5f !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: #161b27;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ----------------- Global Plot Style -----------------
sns.set_style("dark")
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.titlecolor"] = "#e6edf3"
plt.rcParams["axes.labelcolor"] = "#8b949e"
plt.rcParams["axes.edgecolor"] = "#1e3a5f"
plt.rcParams["axes.facecolor"] = "#0d1f3c"
plt.rcParams["figure.facecolor"] = "#161b27"
plt.rcParams["xtick.color"] = "#8b949e"
plt.rcParams["ytick.color"] = "#8b949e"
plt.rcParams["grid.color"] = "#1e3a5f"
plt.rcParams["grid.alpha"] = 0.5

# Chart colour palette
C = ["#388bfd", "#56d364", "#f78166", "#d2a8ff", "#ffa657", "#79c0ff", "#7ee787"]

# ----------------- Sidebar -----------------
st.sidebar.markdown("## 💬 WhatsApp Chat Analyser")
st.sidebar.markdown("---")

with st.sidebar.expander("📖 How to export your chat"):
    st.markdown("""
1. Open **WhatsApp** on your phone
2. Go to the chat you want to analyse
3. Tap **⋮ More → Export Chat**
4. Choose **Without Media**
5. Save the `.txt` file to your device
6. Upload it below ⬇️
    """)

st.sidebar.markdown("### 📁 Upload Chat File")
uploaded_file = st.sidebar.file_uploader("Choose a .txt file", type=["txt"])

# ----------------- Landing Page -----------------
if uploaded_file is None:
    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("""
<div style="text-align:center; padding: 60px 0 20px;">
  <div style="font-size:4rem;">💬</div>
  <h1 style="font-size:2.4rem; font-weight:900; color:#e6edf3; margin-bottom:10px;">
    WhatsApp Chat Analyser
  </h1>
  <p style="color:#8b949e; font-size:1.05rem; max-width:420px; margin:0 auto 12px;">
    Upload your WhatsApp chat export and uncover deep insights — timelines, emojis, word clouds & more.
  </p>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    features = [
        ("📆", "Timelines", "Monthly & daily message trends"),
        ("🔥", "Heatmap", "Your busiest days and hours"),
        ("☁️", "Word Cloud", "Most used words visualised"),
        ("😀", "Emoji Stats", "Top emojis in your chat"),
        ("🏆", "Leaderboards", "Most active users ranked"),
        ("👻", "Ghost Finder", "Spot silent group members"),
    ]
    c1, c2, c3 = st.columns(3)
    for i, col in enumerate([c1, c2, c3]):
        with col:
            for icon, title, desc in features[i*2:(i+1)*2]:
                st.markdown(f"""
<div style="background:#161b27; border:1px solid #1e3a5f; border-radius:14px;
     padding:20px; margin-bottom:14px; text-align:center;">
  <div style="font-size:1.8rem;">{icon}</div>
  <div style="font-weight:700; color:#e6edf3; margin:6px 0 4px;">{title}</div>
  <div style="font-size:0.85rem; color:#8b949e;">{desc}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br><p style='text-align:center; color:#8b949e; font-size:0.82rem;'>← Upload your chat file from the sidebar to get started</p>", unsafe_allow_html=True)
    st.stop()

# ----------------- Process File -----------------
bytes_data = uploaded_file.getvalue()
data = bytes_data.decode('utf-8')
df = preprocessor.preprocessor(data)

user_list = df['user'].unique().tolist()
if 'group_notification' in user_list:
    user_list.remove('group_notification')
user_list.sort()
user_list.insert(0, 'overall')

st.sidebar.markdown("### 👤 Select User")
selected_user = st.sidebar.selectbox('', user_list)
st.sidebar.markdown("<br>", unsafe_allow_html=True)
analyse_btn = st.sidebar.button('🔍 Show Analysis')

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h1 style='color:#e6edf3;'>📱 WhatsApp Chat Analyser</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:#8b949e;'>Analysing: <strong style='color:#58a6ff;'>{selected_user}</strong></p>", unsafe_allow_html=True)
st.markdown("---")

if analyse_btn:

    # ----------------- TOP STATS -----------------
    st.subheader('📌 Top Statistics')
    count, count_words, media, links_count, emoji_df = helper.fetch(selected_user, df)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("💬 Total Messages", count)
    with col2: st.metric("📝 Total Words", count_words)
    with col3: st.metric("📷 Media Messages", media)
    with col4: st.metric("🔗 Links Shared", links_count)

    st.markdown("<br>", unsafe_allow_html=True)

    # ----------------- MONTHLY TIMELINE -----------------
    st.subheader('📆 Monthly Timeline')
    df_timeline, df_timeline_date = helper.month_timeline(selected_user, df)

    fig, ax = plt.subplots()
    ax.plot(df_timeline['xlabels'], df_timeline['message'],
            color=C[0], marker='o', linewidth=2, markersize=5)
    ax.fill_between(df_timeline['xlabels'], df_timeline['message'],
                    alpha=0.15, color=C[0])
    ax.set_title("Messages Per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Messages")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # ----------------- GHOST USERS -----------------
    if len(df['user'].unique()) > 2 and selected_user == 'overall':
        st.subheader('👻 Users Contributing < 2% Messages')
        ghost = helper.ghost_finder(df)
        fig, ax = plt.subplots()
        ax.bar(ghost['user'], ghost['percentage'], color=C[2], edgecolor='#0d1117')
        ax.set_ylabel("Number of times")
        plt.xticks(rotation=90)
        st.pyplot(fig)

    # ----------------- DAILY TIMELINE -----------------
    st.subheader('📅 Daily Timeline')
    fig, ax = plt.subplots()
    ax.plot(df_timeline_date['dates'], df_timeline_date['message'],
            color=C[1], linewidth=1.5)
    ax.fill_between(df_timeline_date['dates'], df_timeline_date['message'],
                    alpha=0.12, color=C[1])
    ax.set_title("Messages Per Day")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # ----------------- CHAT TRAFFIC -----------------
    st.subheader('📊 Chat Traffic Analysis')
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📆 Monthly Traffic**")
        df_month = helper.busy_month(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(df_month['month'], df_month['message'], color=C[3], edgecolor='#0d1117')
        plt.xticks(rotation=90)
        st.pyplot(fig)

    with col2:
        st.markdown("**📅 Weekly Traffic**")
        df_day = helper.busy_day(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(df_day['day_name'], df_day['message'], color=C[4], edgecolor='#0d1117')
        plt.xticks(rotation=90)
        st.pyplot(fig)

    # ----------------- HEATMAP -----------------
    st.subheader('🔥 Weekly Activity Heatmap')
    df_heatmap = helper.heatmap(selected_user, df)
    fig, ax = plt.subplots()
    sns.heatmap(df_heatmap, cmap="Blues", linewidths=0.4,
                linecolor="#0d1117", ax=ax)
    st.pyplot(fig)

    # ----------------- MOST ACTIVE USERS -----------------
    if selected_user == 'overall':
        st.subheader('🏆 Most Active Users')
        x = helper.active(df)
        c1, c2 = st.columns(2)

        with c1:
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color=C[5], edgecolor='#0d1117')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with c2:
            c = (df['user'].value_counts() * 100 / df.shape[0]) \
                .reset_index() \
                .rename(columns={'user': 'User', 'count': 'Percentage'})
            st.dataframe(c, use_container_width=True)

    # ----------------- WORD CLOUD -----------------
    st.subheader('☁️ Word Cloud')
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    ax.axis("off")
    st.pyplot(fig)

    # ----------------- COMMON WORDS -----------------
    st.subheader('🔠 Top 20 Common Words')
    most_common = helper.most_common(selected_user, df)
    fig, ax = plt.subplots()
    ax.barh(most_common[0], most_common[1], color=C[6], edgecolor='#0d1117')
    ax.set_xlabel("Frequency")
    ax.invert_yaxis()
    st.pyplot(fig)

    # ----------------- EMOJI ANALYSIS -----------------
    st.subheader('😀 Emoji Analysis')
    c1, c2 = st.columns(2)

    with c1:
        st.dataframe(emoji_df, use_container_width=True)

    with c2:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(emoji_df['Emoji'], emoji_df['Emoji_count'],
               color=C[0], edgecolor='#0d1117')
        ax.set_title("Top 10 Emojis")
        st.pyplot(fig, use_container_width=True)
