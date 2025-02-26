PROJECT = 'but-tp'

STUDENTS_GROUP = 'binomes@thomasvial.fr'

ADMIN_ACCOUNT = 'binome_zz@thomasvial.fr'

STUDENT_ACCOUNTS = [
    f'binome_{group}{number:02}@thomasvial.fr'
    for group in 'abcd'
    for number in range(1, 11)
] + [ADMIN_ACCOUNT]

#STUDENT_ACCOUNTS = STUDENT_ACCOUNTS[-3:]

SOURCE_DATA_DIR = '../../vectors/final_output'
