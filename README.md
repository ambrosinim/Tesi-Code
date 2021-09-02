# Tesi-Code
Cartelle nella Repository e contenuto:
- Braccio_arduino_finalcode:
  Codice C++ Arduino per comunicare con il PC e muovere il braccio controllando i 3 servomotori.
- Python Code:  
  - Codice Python per l'applicazione PC
  - Modelli (ad eccezione dei VGG16)
  - Codice per il testing dei modelli
  - Codice per il plotting dell Confusion Matrices
  - Codice per la formazione di un dataset (training o testing)
- More models:
  alcuni dei modelli ottenuti durante il training, meno performanti di quelli contenuti in Python Code
- Jupyter notebooks for training:
  Notebooks in cui è presentato il training dei modelli più performanti.


# Training
Per eseguire modifiche sl training dei modelli è consigliata l'apertura su Colab (https://research.google.com/colaboratory/)
I jupyter notebooks includono già l'accesso al dataset su cui è stato effettuato il traing, validatione e testing.
## Traing dataset: https://github.com/ma-tesi/hands_dataset.git
# Testing Finale
il testing finale può esssere svolto lavorando nella cartella Python Code seguendo questi passaggi:
1. aprire ed eseguire il file testpickle.py che genera i file X_test.pickle e Y_test.pickle a partire dalla cartella Test Data. I file generati contengono rispettivamente gli input del testing e le relative labels corrette;
2. aprire ed eseguire il file test.py che stampa le informazioni relative alle prestazioni di ciascun modello e le confusion matrices.
