FROM python
COPY . . 
RUN pip3 install -r requirements.txt
CMD ["python", "bot.py"]