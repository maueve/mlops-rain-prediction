FROM python:3.10-slim

WORKDIR /app

#COPY ../../data/models/model.pkl /app/model.pkl
#COPY model.pkl /app/model.pkl

#COPY requirements.txt requirements.txt

COPY . .

RUN pip install -r requirements.txt

#COPY prediction_service.py prediction_service.py

#COPY middleware.py middleware.py

#COPY middleware.py middleware.py


#EXPOSE 8000

CMD ["uvicorn", "prediction_service:app", "--host", "0.0.0.0", "--port", "8000"]