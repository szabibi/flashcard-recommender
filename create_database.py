from db import commit, get_cur

cur = get_cur()

cur.execute('DROP TABLE IF EXISTS sets')
cur.execute('DROP TABLE IF EXISTS cards')

cur.execute('CREATE TABLE `sets` ('
            '`id` INTEGER NOT NULL,'
            '`name` TEXT NOT NULL,'
            '`last_reviewed` DATE DEFAULT CURRENT_DATE,'
            '`count` INTEGER,'
            '`accuracy` REAL,'
            '`last_flag` INTEGER DEFAULT 0,'
            'PRIMARY KEY(`id` AUTOINCREMENT));')

cur.execute('CREATE TABLE "cards" ('
            '"id" INTEGER,'
            '"set_id" INTEGER,'
            '"front" TEXT,'
            '"back" TEXT,'
            '"hint" TEXT,'
            'PRIMARY KEY("id" AUTOINCREMENT));')

# SETS
cur.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name="sets"')

cur.execute('INSERT INTO sets (name, last_reviewed, count, accuracy)'
            'VALUES("Numbers", "2023-05-10", 6, 25),'
            '("Opposites", "2023-05-06", 2, 75),'
            '("Animals", "2023-05-01", 8, 50),'
            '("Family I.", "2023-05-09", 1, 65),'
            '("Fruit", "2023-05-01", 0, 0)')

# FLASHCARDS
cur.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name="cards"')

cur.execute('INSERT INTO cards (set_id, front, back, hint)'
            'VALUES(2, "heavy", "หนัก", "mak-L"),'
            '(2, "light", "เบา", "bao-M"),'
            '(2, "big", "ใหญ่", "yai-L"),'
            '(2, "small", "เล็ก", "lek-H"),'
            '(2, "high, tall", "สูง", "suung-R"),'
            '(2, "short", "เตี้ย", "dtiiya-F"),'
            '(2, "low", "ต่ำ", "dtam-L"),'
            '(2, "good", "คี", "dee-M"),'
            '(2, "bad", "เลว", "leu-M"),'
            '(2, "beautiful", "สวย", "suuay-R"),'
            '(2, "ugly", "น่าเกลียค", "naa-F-kliiyad-L"),'
            '(2, "expensive", "แพง", "pheeng-M"),'
            '(2, "cheap", "ถูก", "thuuk-L"),'
            '(2, "strong", "แข็งแรง", "kheng-R-reeng-M"),'
            '(2, "weak", "อ่อนแอ", "aawn-L-ee-M"),'
            '(2, "happy", "คีใจ", "dee-M-jai-M"),'
            '(2, "sad", "เสียใจ", "siiya-R-jai-M"),'
            '(2, "fast", "เร็ว", "reu-M"),'
            '(2, "slow", "ช้า", "chaa-H"),'
            '(3, "cat", "แมว", "meeu-M"),'
            '(3, "dog", "หมา", "maa-R"),'
            '(3, "wolf", "หมาป่า", "maa-R-paa-L"),'
            '(3, "bird", "นก", "nok-H"),'
            '(3, "chicken", "ไก่", "kai-L"),'
            '(1, "hundred", "ร้อย", "rawy-H"),'
            '(1, "thousand", "พุม", "phum-M"),'
            '(1, "ten thousand", "หมั่น", "man-L"),'
            '(1, "seven", "เจ็ด", "jet-L"),'
            '(1, "eight", "แปด", "peet-L"),'
            '(1, "zero", "ศูนย์", "suun-R"),'
            '(4, "mother", "แม่", "mee-F"),'
            '(4, "father", "พ่อ", "phaaw-F"),'
            '(4, "grandma (maternal)", "ยาย", "yaay-M"),'
            '(4, "grandpa (maternal)", "ตา", "dtaa-M"),'
            '(4, "family", "ครอบครัว", "kraawp-F-kruua-M"),'
            '(5, "apple", "แอปเปิล", "eep-H-pooen-F"),'
            '(5, "strawberry", "สตรอเบอร์รี่", "sa-L-dtraaw-M-booe-M-rii-F"),'
            '(5, "banana", "กล้วย", "kluay-F"),'
            '(5, "pear", "แพร์", "phee-M"),'
            '(5, "pineapple", "สับปะรด", "sap-L-pa-L-rot-H")'
            )

commit()