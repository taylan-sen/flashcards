# 🧠 Flashcard Quiz App (Pygame)

This project is a **flashcard quiz application** built using **Python** and **Pygame**. It allows users to practice flashcards interactively via a graphical interface, tracking performance across sessions and adjusting the frequency of questions based on accuracy.

---

## 🚀 Features

- Interactive flashcard system using Pygame
- Load questions and answers from a CSV file
- Ask user for their name and track performance
- Save progress (correct/wrong counts) to a JSON file
- Increase frequency of questions the user gets wrong
- Decrease frequency of questions the user gets right

---

## 📁 File Structure

- `flashcards.py` – main Pygame application
- `flashcards.csv` – CSV file with flashcard questions and answers
- `user_data.json` – auto-generated file to store user performance data

---

## 📝 CSV Format

Each row in `flashcards.csv` should be:

```
"Question","Answer"
"What is the capital of France?","Paris"
"2 + 2 equals what?","4"
```

Quotes are required around both question and answer.

---

## 💾 How to Run

### 1. Install Dependencies

```bash
pip install pygame
```

### 2. Run the App

```bash
python flashcards.py
```

### 3. Play

- Enter your name when prompted.
- Answer the questions via keyboard.
- Feedback (Correct / Incorrect) is displayed after each answer.
- Your progress is saved and used to adjust which questions appear more often.

---

## 🛠 Requirements

- Python 3.7+
- Pygame library

---

## 📌 Notes

- Make sure `flashcards.csv` is in the same folder as `flashcards.py`.
- The app will automatically create and update `user_data.json` to track performance.

---

## 📃 License

This project is open source and free to use.

---