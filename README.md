# zadko-weather-project: Random Forest Precipitation Nowcasting for the Zadko Observatory

The code contained in this repository accompanies the thesis of Matvey Y. Solovyov submitted in partial fulfilment of the Bachelor of Science (Hons) course.

We have developed a number of Random Forest models that we propose be used to improve the performance of the Zadko Observatory managed by OzGrav-UWA (henceforth reffered to as The Observatory).

## Contents

A 3-day subsample of the data used for computation is provided here (01.03.2015 - 03.03.2015).

### System logs

The logs of two of the sub-modules are used to analyse the current performance of the Observatory. Their analysis is contained in the logs_processing notebook.

### Weather data

These are records from the weather station operating at the Observatory. This data forms the main part of the project. It was first received as an SQL dump, and hence a script to convert it to csv is provided in txttocsv.py. Intial cleaning and setup is done in the script wx_cleaning.py where we save the data as a final csv. This is used in logs_processing to evaluate roof performance. The main analysis, model training and evaluation, is provided in the notebook "Precip RF models".
