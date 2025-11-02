from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

# Menampilkan entry data
@app.get('/data')
def ShowData():
    df = pd.read_csv('bikeshare_trips_clean.csv').dropna()
    data = df.to_dict(orient='records')
    return data

# Menghapus entry data yang dikehendaki
@app.get('/data/delete/{duration}')
def DeleteData(duration: int):
    df = pd.read_csv('bikeshare_trips_clean.csv').dropna()
    df_new = df[df['duration_sec'] != duration]
    df_new.to_csv('bikeshare_trips_clean.csv', index=False)

    if duration not in df['duration_sec'].values:
        raise HTTPException(
            status_code=404, 
            detail=f'Data dengan durasi {duration} tidak ditemukan.'
        )

    return {
        'message': f'Data dengan durasi {duration} detik telah berhasil dihapus.',
        'data_awal': f'{len(df)} baris',
        'data_baru': f'{len(df_new)} baris'
    }
