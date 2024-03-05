


create env 

python -m venv env
/venv/Scripts/activate.bat

Install dependencies

pip install -r requirements.txt


Start service

uvicorn main:app --reload




TODO:
1. Use docker to start the service
2. Refactor services
3. Refactor endpoints
4. Add jwt to endpoints
   
