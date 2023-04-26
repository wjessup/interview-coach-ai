# interview-coach-ai

Over the weekend I met with [MeritAmerica](https://meritamerica.org/), a non-profit focused on helping retrain americans to get better careers. For example, they help people who are uber drivers become java engineers and the foundation covers the cost for training and only takes a fee after the candidate has been placed in a job. They measure success by "long term wage increase" and have an 82 rate. 

I sat down with them to brainstorm how AI could help and came up with an idea of an interview coach. For people in this program they are transforming their lives. Often the first time they've ever used zoom is in the training, so it's not a surprise that most of the people who have passed coursework will be unconfident in their skills, nervous, and struggle to market their skills accordingly. 
            
I created this app to demonstrate an concept of an interview helper chatbot that would help folks learn to take better interviews. 

The next step would be to review actual interviews from the candidate (perhaps via brighthire api) and automatically review and create response suggestions.


## 💾 Installation

To install Interview Coach AI, follow these steps:

1. Clone the repository:
For this step you need Git installed, but you can just download the zip file instead by clicking the button at the top of this page ☝️
```
git clone https://github.com/wjessup/interview-coach-ai.git
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Open `main.py` and set your API key here: `openai.api_key = yourapikey`
  - Obtain your OpenAI API key from: https://platform.openai.com/account/api-keys.

## 🔧 Usage

1. Run the `main.py` Python script via Streamlit in your terminal:
```
streamlit run main.py
```
