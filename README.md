# 🔍 Checkers AI

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![pygame](https://img.shields.io/badge/pygame-2.0%2B-green.svg)
![NumPy](https://img.shields.io/badge/NumPy-1.19%2B-yellow.svg)
![License-MIT](https://img.shields.io/badge/License-MIT-brightgreen?style=flat)

> **An interactive Checkers game with AI opponent** powered by Minimax and optional Alpha‑Beta pruning algorithms, visualized in real time using Pygame.

---

## 🎮 Features & Highlights

* 🔴 **Red vs. Blue**: Human vs. Human or Human vs. AI modes
* 🤖 **AI Algorithms**: Minimax and Optional Alpha‑Beta Pruning
* 📊 **Metrics**: Nodes expanded, time per move
* 🎨 **Real‑Time Visualization**: Pygame board rendering
* 👑 **King Promotion**: Auto‑promote on reaching the opposite side
* 🔄 **Jump & Capture**: Multi‑jump capture sequences

---

## 🛠️ Tech Stack

* **Language**: Python 3.7+
* **Graphics**: Pygame
* **Computation**: NumPy

---

## 📥 Installation

1. Clone repository:

   ```bash
   git clone https://github.com/asadsandhu/checkers-ai.git
   cd checkers-ai
   ```
2. (Optional) Create virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\\Scripts\\activate   # Windows
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🎮 Running the Game

```bash
python checkers_ai.py
```

* **Mode Selection:** 1 for Human vs AI, 2 for Human vs Human
* **AI Color:** Choose Red (R) or Blue (B)
* **Algorithm:** 1 for Minimax, 2 for Alpha‑Beta Pruning
* **Search Depth:** Enter depth limit (e.g., 3–5)
* **Controls:** Click to select and move pieces. Valid moves and captures will be enforced.

---

## ⚙️ Configuration & Customization

* **DEPTH\_LIMIT:** Adjust default search depth
* **BOARD\_SIZE:** Change to other square sizes (with code tweaks)
* **Colors & Styles:** Modify RGB constants at top of script

---

## 📂 Project Structure

```text
├── README.md
├── checkers_ai.py
├── requirements.txt
├── .gitignore
└── assets/
    └── Board.png
```

---

## 🤝 Contributing

1. ⭐ Star the repo
2. 🍴 Fork
3. 📥 Clone
4. 💡 New branch
5. 🚀 Commit & push
6. 🔃 Open PR

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
