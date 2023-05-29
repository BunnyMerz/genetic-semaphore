road_names = "A B C D E F G G' H H' I I' J J' K L M N O P Q R S T U U' V X X'".split(' ')

inp = [
  'A 0 250 P', # A não tem sinal (0), 20m e vai pra P
  'B 1 200 A Q',
  "C 0 250 B",
  "D 0 200 C",
  "E 1' 250 A Q",
  "F 2 300 D E",
  "G 5 250 F",
  "G' 0 250 H",
  "H 7 400 U X",
  "H' 0 400 G",
  "I 0 1000 S",
  "I' 0 1000 X'",
  "J 0 200 R",
  "J' 6 200 T U'",
  "K 4 200 I' S V",
  "L 0 250 K",
  "M 0 200 L",
  "N 4' 250 I' S V",
  "O 3' 250 M N",
  "P 0 600 O",
  "Q 3 600 M N",
  "R 2' 300 D E",
  "S 0 300 J' R",
  "T 5' 500 F G'",
  "U 6 400 J T",
  "U' 7' 400 H' X",
  "V 6' 700 J T U'",
  "X 0 400 I",
  "X' 7 400 H' U",
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