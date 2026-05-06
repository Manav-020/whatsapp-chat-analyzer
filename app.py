

import streamlit as st
import preprocessor
import helper
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------- Global Style -----------------
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["axes.titleweight"] = "bold"

st.sidebar.title('📊 WhatsApp Chat Analysis')

uploaded_file = st.sidebar.file_uploader("📁 Choose a chat file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocessor(data)

    user_list = df['user'].unique().tolist()
    st.header('📱 WhatsApp Chat Analyzer')

    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, 'overall')

    selected_user = st.sidebar.selectbox('👤 Select User', user_list)

    if st.sidebar.button('🔍 Show Analysis'):

        # ----------------- TOP STATS -----------------
        st.subheader('📌 Top Statistics')

        count, count_words, media, links_count, emoji_df = helper.fetch(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💬 Total Chats", count)
        with col2:
            st.metric("📝 Total Words", count_words)
        with col3:
            st.metric("📷 Media Messages", media)
        with col4:
            st.metric("🔗 Links Shared", links_count)

        # ----------------- MONTHLY TIMELINE -----------------
        st.subheader('📆 Monthly Timeline')
        df_timeline, df_timeline_date = helper.month_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(df_timeline['xlabels'], df_timeline['message'],
                color='#1f77b4', marker='o')
        ax.set_title("Messages Per Month")
        ax.set_xlabel("Month")
        ax.set_ylabel("Messages")
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # ----------------- GHOST USERS -----------------
        if len(df['user'].unique())>2 and selected_user == 'overall':
            st.subheader('👻 Users Contributing < 2% Messages')
            ghost = helper.ghost_finder(df)

            fig, ax = plt.subplots()
            ax.bar(ghost['user'], ghost['percentage'], color='#ff7f0e')
            ax.set_ylabel("Percentage")
            plt.xticks(rotation=90)
            st.pyplot(fig)

        # ----------------- DAILY TIMELINE -----------------
        st.subheader('📅 Daily Timeline')
        fig, ax = plt.subplots()
        ax.plot(df_timeline_date['dates'], df_timeline_date['message'],
                color='#d62728')
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
            ax.bar(df_month['month'], df_month['message'], color='#2ca02c')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.markdown("**📅 Weekly Traffic**")
            df_day = helper.busy_day(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(df_day['day_name'], df_day['message'], color='#9467bd')
            plt.xticks(rotation=90)
            st.pyplot(fig)

        # ----------------- HEATMAP -----------------
        st.subheader('🔥 Weekly Activity Heatmap')
        df_heatmap = helper.heatmap(selected_user, df)

        fig, ax = plt.subplots()
        sns.heatmap(df_heatmap, cmap="YlOrRd", linewidths=0.5, ax=ax)
        st.pyplot(fig)

        # ----------------- MOST ACTIVE USERS -----------------
        if selected_user == 'overall':
            st.subheader('🏆 Most Active Users')
            x = helper.active(df)

            c1, c2 = st.columns(2)
            with c1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='#17becf')
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with c2:
                c = (df['user'].value_counts() * 100 / df.shape[0]) \
                    .reset_index() \
                    .rename(columns={'user': 'User', 'count': 'Percentage'})
                st.dataframe(c)

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
        ax.barh(most_common[0], most_common[1], color='#bcbd22')
        ax.set_xlabel("Frequency")
        st.pyplot(fig)

        # ----------------- EMOJI ANALYSIS -----------------
        st.subheader('😀 Emoji Analysis')
        c1, c2 = st.columns(2)

        with c1:
            st.dataframe(emoji_df)

        with c2:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(emoji_df['Emoji'], emoji_df['Emoji_count'], color='#e377c2')
            ax.set_title("Top 10 Emojis")
            st.pyplot(fig,use_container_width=True)
