# Face Anonimizer
размытие лиц на фото, видео и вебкамере.

<table>
  <tr>
    <td><img src=assets/attractive-1869761_640.jpg width=400></td>
    <td><img src=output/attractive-1869761_640.jpg width=400></td>
  </tr>
  <tr>
    <td><img src=assets/beard-1845166_640.jpg width=400></td>
    <td><img src=output/beard-1845166_640.jpg width=400></td>
  </tr>
</table>
Видеопримеры можно найти в папках <a href=https://github.com/lethnis/face-anonimizer/tree/main/assets>assets</a> и <a href=https://github.com/lethnis/face-anonimizer/tree/main/output>output</a>

# Использование
1. клонировать репозиторий, создать виртуальную среду с `python 3.11`, установить `requirements.txt`
2. для примнения размытия к фото и видео закинуть их в папку `assets`. Запустить `python main.py`. Так же можно указать путь до своей папки или файла, например `python main.py path/to/folder_or_file`.
3. для использования на вебкамере запустить python `webcam.py`. Для выхода нажать 'q'.
