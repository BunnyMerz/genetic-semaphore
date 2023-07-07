road_names = "A B C Q X Y Z".split(' ')

inp = [
  "A 0 10 B",
  "B 0 10 C",
  "C 1 10 Q",
  "Q 2 10 A X",
  "X 0 10 Y",
  "Y 0 10 Z",
  "Z 1' 10 Q"
]

num_sem = 0
unique_s = set()
matrix = []
roads_info = []
for x in inp:
  row = [0]*len(road_names)
  name, sem_id_i, w, *conn = x.split(' ')
  i = 0
  if sem_id_i == '0':
    sem_id = None
  elif sem_id_i[-1] == "'":
    i = 1
    sem_id = int(sem_id_i[:-1]) - 1
    unique_s.add(sem_id)
  else:
    sem_id = int(sem_id_i) - 1
    unique_s.add(sem_id)
    
  for con in conn:
    row[road_names.index(con)] = 1
  matrix.append(row)

  roads_info.append([int(w), sem_id, i])

num_sem = len(unique_s)