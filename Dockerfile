# Set the base image to construct from
FROM svizor/zoomcamp-model:mlops-3.10.0-slim
# Set the working directory
WORKDIR /app
# Start by installing pip
RUN pip install --upgrade pip
# Then bring in pip install pipenv
RUN pip install pipenv
# Copy in the pipenv files for the python environment.
COPY ["Pipfile", "Pipfile.lock", "./"]
# Run the pipenv install
RUN pipenv install --system --deploy
# Copy over the python files and data now
COPY ["starter.py", "./"]
# make the directory to store the data
RUN mkdir data
# Copy in the data
COPY ["./data/yellow_tripdata_2022-04.parquet", "./data"]
# CD back up to the parent
RUN cd ..
# LS the final directories
RUN ls 
# Now ls the data directory
RUN cd data && ls
# Run the script
ENTRYPOINT ["python", "starter.py", "2022", "04"]