# Face Anonimizer
Размытие лиц на фото, видео и вебкамере.  
Для детекции лиц использовалась модель [BlazeFace (short-range)](https://developers.google.com/mediapipe/solutions/vision/face_detector#blazeface_short-range).

<table>
  <tr>
    <td><img src=assets/attractive-1869761_640.jpg width=400></td>
    <td><img src=output/attractive-1869761_640.jpg width=400></td>
  </tr>
  <tr>
    <td><img src=assets/beard-1845166_640.jpg width=400></td>
    <td><img src=output/beard-1845166_640.jpg width=400></td>
  </tr>
  <tr>
    <td><img src=https://github.com/lethnis/face-anonimizer/assets/88483002/713a2693-ce96-417d-86d6-4286a2b49da8 width=400></td>
    <td><img src=https://github.com/lethnis/face-anonimizer/assets/88483002/c482e43f-7b41-4a8a-82b8-d016f6e0829d width=400></td>
  </tr>
  <tr>
    <td><img src=https://github.com/lethnis/face-anonimizer/assets/88483002/3c67c094-28ff-4d67-b0a7-cfc2193ae689 width=400></td>
    <td><img src=https://github.com/lethnis/face-anonimizer/assets/88483002/7fd2e08d-a70f-4b69-ada6-e6929f6b1596 width=400></td>
  </tr>
</table>

# Использование
1. клонировать репозиторий, создать виртуальную среду с `python 3.11`, установить `requirements.txt`
2. для примнения размытия к фото и видео закинуть их в папку `assets`. Запустить `python main.py`. Так же можно указать путь до своей папки или файла, например `python main.py path/to/folder_or_file`.
3. для использования на вебкамере запустить python `webcam.py`. Для выхода нажать 'q'.
