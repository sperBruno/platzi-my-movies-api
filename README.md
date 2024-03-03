


create env 

python -m venv env
/venv/Scripts/activate.bat

Install dependencies

pip install -r requirements.txt


Start service

uvicorn main:app --reload