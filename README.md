## Website URL ➡️ https://whatsapp-chat-analyzer-kyxnvhjyj6cbenzqjn5oun.streamlit.app/


# 💬 WhatsApp Chat Analyser

> Upload your WhatsApp chat export and instantly uncover deep insights — who talks the most, what words dominate, which emojis fly, and when conversations peak.

![Python](https://img.shields.io/badge/Python-3.8+-1f6feb?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b?style=flat-square&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-latest-150458?style=flat-square&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-56d364?style=flat-square)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📌 **Top Statistics** | Total messages, words, media, and links at a glance |
| 📆 **Monthly Timeline** | See how chat activity has evolved over time |
| 📅 **Daily Timeline** | Day-by-day message volume trends |
| 📊 **Traffic Analysis** | Busiest months and days of the week |
| 🔥 **Activity Heatmap** | Hour-by-hour and day-by-day intensity grid |
| 🏆 **Most Active Users** | Leaderboard with percentage breakdown |
| 👻 **Ghost Finder** | Spot group members who contribute less than 2% |
| ☁️ **Word Cloud** | Visual map of your most-used words |
| 🔠 **Top 20 Words** | Ranked bar chart of word frequency |
| 😀 **Emoji Analysis** | Top 10 emojis with counts and charts |

---

## 🖥️ Screenshots

> _Add screenshots here after running the app_

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/whatsapp-chat-analyser.git
cd whatsapp-chat-analyser

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 📤 How to Export Your WhatsApp Chat

1. Open **WhatsApp** on your phone
2. Go to the chat you want to analyse
3. Tap **⋮ (three dots) → More → Export Chat**
4. Select **Without Media** to keep the file small
5. Save or share the `.txt` file to your device
6. Upload it in the app sidebar

---

## 🗂️ Project Structure

```
whatsapp-chat-analyser/
├── app.py              # Main Streamlit application
├── preprocessor.py     # Chat parsing and cleaning
├── helper.py           # Analysis functions
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

- **[Python](https://python.org)** — Core language
- **[Streamlit](https://streamlit.io)** — Web app framework
- **[Pandas](https://pandas.pydata.org)** — Data processing
- **[Matplotlib](https://matplotlib.org)** — Charts and plots
- **[Seaborn](https://seaborn.pydata.org)** — Heatmaps and styling
- **[WordCloud](https://github.com/amueller/word_cloud)** — Word cloud generation

---

## 📦 requirements.txt

```
streamlit
pandas
matplotlib
seaborn
wordcloud
emoji
urlextract
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ and Python</p>
