FROM python:3.12.3
ADD eurofaang_ri_be eurofaang_ri_be
WORKDIR eurofaang_ri_be
ADD requirements.txt ./
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]