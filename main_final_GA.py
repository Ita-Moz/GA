import random
import time
import numpy as np
from prettytable import PrettyTable
import sys

sys.path.append('./db')
from mysql_helper import connect_to_mysql

# Hàm Global
# Hàm xuất ra number phần tử ngẫu nhiên của list có thể trùng nhau
def random_elements_list(list, number):
    arr = []
    for i in range(0, number):
        arr.append(list[random.randint(0, len(list)-1)])
    return arr

# Hàm xuất ra number phần tử ngẫu nhiên của list không trùng nhau
def random_elements_no_duplicates(array, number):
    array_copy = array.copy()
    result = []
    for i in range(number):
        random_index = random.randint(0, len(array_copy) - 1)
        result.append(array_copy[random_index])
        array_copy.pop(random_index)
    return result

# Hàm chuyển một list các tuple thành một list
def tuple_to_list(tuple_list):
            return [item for tpl in tuple_list for item in tpl]
# Phòng học
class Room:
    def __init__(self, id, name, capacity, type):
        self._id = id
        self._name = name
        self._capacity = capacity
        self._type = type

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_capacity(self):
        return self._capacity

    def get_type(self):
        return self._type

    def __str__(self):
        return "Room: " + self._id + " | " + self._name + " | " + str(self._capacity) + " | " + self._type

# Giảng viên
class Instructor:
    def __init__(self, id, name, sex, email, phone, address):
        self._id = id
        self._name = name
        self._sex = sex
        self._email = email
        self._phone = phone
        self._address = address

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_sex(self):
        return self._sex

    def get_email(self):
        return self._email

    def get_phone(self):
        return self._phone

    def get_address(self):
        return self._address

    def __str__(self):
        return "Instructor: " + self._id + " | " + self._name + " | " + str(self._sex) + " | " + self._email + " | " + self._phone + " | " + self._address

# Khoảng thời gian học (3 tiết/ca)
class TimeLessons:
    def __init__(self, id, time):
        self._id = id
        self._time = time

    def get_id(self):
        return self._id

    def get_time(self):
        return self._time

    def __str__(self):
        return "TimeLessons: " + self._id + " | " + self._time

# Lớp học phần(Khoá học)
class Course:
    def __init__(self, id, name, maxNumberOfStudents, instructors,subject):
        self._id = id
        self._name = name
        self._maxNumberOfStudents = maxNumberOfStudents
        self._instructors = instructors
        self._subject = subject

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_maxNumberOfStudents(self):
        return self._maxNumberOfStudents

    def get_instructors(self):
        return self._instructors
    def get_subject(self):
        return self._subject

    def __str__(self):
        return "Course: " + self._id + " | " + self._name + " | " + str(self._maxNumberOfStudents) 

# Học phần(Môn học)
class Subject:
    def __init__(self, id, name, numberOfPeriods):
        self._id = id
        self._name = name
        self._numberOfPeriods = numberOfPeriods

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_numberOfPeriods(self):
        return self._numberOfPeriods

class Classes:
    def __init__(self,stt,course,instructors):
        self._stt = stt
        self._course = course
        self._instructors = instructors
        self._room = None
        self._time = None
    
    def get_stt(self):
        return self._stt
    def get_course(self):
        return self._course
    def get_instructors(self):
        return self._instructors
    def get_room(self):
        return self._room
    def get_time(self):
        return self._time
    def set_room(self,room):
        self._room = room
    def set_time(self,time):
        self._time = time

    def __str__(self):
        return str(self._course.get_id())+","+str(self._room.get_id())+","+str(self._time.get_id())

class Schedule:
    def __init__(self,data):
        self._data = data
        self._classes = []
        self._fitness = 0
        self._numberOfConflicts = 0
        self._isFitnessChanged = False
        self._idCLasses = 0
    
    # Create individual
    def create_schedule(self):
        for i in range(0,len(self._data.get_courses())):
            newClasses = Classes(self._idCLasses,self._data.get_courses()[i],self._data.get_courses()[i].get_instructors())
            self._idCLasses += 1
            newClasses.set_room(random.choice(self._data.get_rooms()))
            newClasses.set_time(random.choice(self._data.get_time_lessons()))
            self._classes.append(newClasses)
        return self
    def set_classes(self,classes):
        self._classes = classes
        
    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            # Kiểm tra logic sức chứa phòng học và số lượng sinh viên
            if(classes[i].get_room().get_capacity() < classes[i].get_course().get_maxNumberOfStudents()):
                self._numberOfConflicts += 1
            for j in range(i+1, len(classes)):
                # Kiểm tra trùng lịch giảng dạy
                if(classes[i].get_instructors() == classes[j].get_instructors() and classes[i].get_time() == classes[j].get_time()):
                    self._numberOfConflicts += 1
                # Kiểm tra trùng lịch học
                if(classes[i].get_course() == classes[j].get_course() and classes[i].get_time() == classes[j].get_time()):
                    self._numberOfConflicts += 1
                # Kiểm tra trùng lịch giảng dạy và học
                if(classes[i].get_room() == classes[j].get_room() and classes[i].get_time() == classes[j].get_time()):
                    if(classes[i].get_course() != classes[j].get_course()):
                        self._numberOfConflicts += 1
        # Đảm bảo cho giá trị fitness luôn nằm trong khoảng từ 0-1
        return 1/((1.0*self._numberOfConflicts + 1))

    def get_fitness(self):
        if(self._isFitnessChanged == True):
            self._fitness = '{:.3f}'.format(self.calculate_fitness())
            self._isFitnessChanged = False
        return self._fitness

    def get_numberOfConflicts(self):
        return self._numberOfConflicts
    
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes
    def __str__(self):
        value = ""
        for i in range(0,len(self._classes)):
            value += str(self._classes[i]) + ","
        value += str(self._classes[len(self._classes)-1])
        return value

class Data:
    def __init__(self):
        self.cursor = connect_to_mysql.cursor()
        self._rooms = self.query_rooms()
        self._instructors = self.query_instructors()
        self._timeLessons = self.query_time_lessons()
        self._courses = self.query_courses()
        self._subjects = self.query_subjects()
        self._numberCourseOfSubjects = self.get_number_courses()
        
    def get_number_courses(self):
        self.cursor.execute("""
        SELECT count(courses.id) as number
        FROM courses
        """)
        number = self.cursor.fetchone()
        return number[0]
    def query_courses(self):
        self.cursor.execute("""
        SELECT courses.id,courses.name,courses.max_students, instructors.id,subjects.id
        FROM courses
        join instructors_subjects on courses.instructor_subject_id = instructors_subjects.id
        join instructors on instructors_subjects.instructor_id = instructors.id
        join subjects on instructors_subjects.subject_id = subjects.id
        """)
        courses = self.cursor.fetchall()
        array = []
        for course in courses:
            newCourse = Course(course[0],course[1],course[2],course[3],course[4])
            array.append(newCourse)
        return array
    def query_rooms(self):
        self.cursor.execute("""
        SELECT * FROM rooms
        """)
        rooms = self.cursor.fetchall()
        array = []
        for room in rooms:
            newRoom = Room(room[0],room[1],room[2],room[3])
            array.append(newRoom)
        return array
    def query_instructors(self):
        self.cursor.execute("""
        SELECT * FROM instructors
        """)
        instructors = self.cursor.fetchall()
        array = []
        for instructor in instructors:
            newInstructor = Instructor(instructor[0],instructor[1],instructor[2],instructor[3],instructor[4],instructor[5])
            array.append(newInstructor)
        return array
    def query_time_lessons(self):
        self.cursor.execute("""
        SELECT * FROM timelessons
        """)
        time_lessons = self.cursor.fetchall()
        array = []
        for time_lesson in time_lessons:
            newTimeLesson = TimeLessons(time_lesson[1],time_lesson[2])
            array.append(newTimeLesson)
        return array
    def query_subjects(self):
        self.cursor.execute("""
        SELECT subjects.id,subjects.name,subjects.number_of_periods
        FROM subjects
        """)
        list_subjects = self.cursor.fetchall()
        array = []
        for subject in list_subjects:
            newSubject = Subject(subject[0],subject[1],subject[2])
            array.append(newSubject)
        return array
    
    def get_rooms(self):
        return self._rooms
        
    def get_instructors(self):
        return self._instructors

    def get_time_lessons(self):
        return self._timeLessons

    def get_number_of_periods(self):
        return self._timeLessons

    def get_courses(self):
        return self._courses

    def get_subjects(self):
        return self._subjects

    def get_number_course_of_subject(self):
        return self._numberCourseOfSubjects

class Display:
    def __init__(self,data):
        self._data = data
    
    def print_all_data(self):
        self.print_subjects()
        self.print_instructors()
        self.print_courses()
        self.print_rooms()
        self.print_time_lessons()

    def print_subjects(self):
        x = PrettyTable()
        subjects = self._data.get_subjects()
        print("--- Bảng thông tin môn học ---")
        x.field_names = ["STT", "Mã môn học", "Tên môn học", "Lớp học phần", "Số tiết"]
        for i in range (0,len(subjects)):
            courses = subjects[i].get_courses()
            tempStr = '['
            for j in range (0,len(courses)-1):
                tempStr += courses[j].get_name() + ','
            tempStr += courses[len(courses)-1].get_name() + ']'
            x.add_row([str(i+1), subjects[i].get_id(), subjects[i].get_name(), tempStr, str(subjects[i].get_numberOfPeriods())])
        print(x)
    
    def print_instructors(self):
        x = PrettyTable()
        instructors = self._data.get_instructors()
        print("--- Bảng thông tin giảng viên ---")
        x.field_names = ["STT", "Mã giảng viên", "Tên giảng viên", "Giới tính", "Email", "Số điện thoại", "Địa chỉ"]
        for i in range (0,len(instructors)):
            x.add_row([str(i+1),instructors[i].get_id(),instructors[i].get_name(),instructors[i].get_sex(),instructors[i].get_email(),instructors[i].get_phone(),instructors[i].get_address()])
        print(x)

    def print_courses(self):
        x = PrettyTable()
        courses = self._data.get_courses()
        print("--- Bảng thông tin lớp học phần ---")
        x.field_names = ["STT", "Mã lớp học phần", "Tên lớp học phần", "Số lượng sinh viên", "Giảng viên"]
        for i in range (0,len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = '['
            for j in range (0,len(instructors)-1):
                tempStr += instructors[j].get_name() + ','
            tempStr += instructors[len(instructors)-1].get_name() + ']'
            x.add_row([str(i+1),courses[i].get_id(),courses[i].get_name(),str(courses[i].get_maxNumberOfStudents()),tempStr])
        print(x)

    def print_rooms(self):
        x = PrettyTable()
        rooms = self._data.get_rooms()
        print("--- Bảng thông tin phòng học ---")
        x.field_names = ["STT", "Mã phòng học", "Tên phòng học", "Số lượng chỗ ngồi", "Loại phòng học"]
        for i in range (0,len(rooms)):
            x.add_row([str(i+1),rooms[i].get_id(),rooms[i].get_name(),str(rooms[i].get_capacity()),rooms[i].get_type()])
        print(x)    

    def print_time_lessons(self):
        x = PrettyTable()
        timeLessons = self._data.get_time_lessons()
        print("--- Bảng thông tin thời gian học ---")
        x.field_names = ["STT", "Mã thời gian học", "Thời gian học"]
        for i in range (0,len(timeLessons)):
            x.add_row([str(i+1),timeLessons[i].get_id(),timeLessons[i].get_time()])
        print(x)

    def print_schedule(self,schedule):
        x = PrettyTable()
        print("--- Bảng thời khóa biểu ---")
        x.field_names = ["STT", "Môn học(id)", "Lớp học phần(maxNumberOfStudents)", "Room(capacity)", "Giảng viên(id)", "Thời gian(id)"]
        classes = schedule.get_classes()
        for i in range (0,len(classes)):
            x.add_row([str(i+1),
                       classes[i].get_subject().get_name() + '(' + classes[i].get_subject().get_id()+')', 
                       classes[i].get_course().get_id() + '(' + str(classes[i].get_course().get_maxNumberOfStudents())+')',
                       classes[i].get_room().get_name() + '('+ str(classes[i].get_room().get_capacity())+')', 
                       classes[i].get_instructors().get_name()  + '(' + classes[i].get_instructors().get_id()+')', 
                       classes[i].get_time().get_time() + '(' + classes[i].get_time().get_id()+')'])
        print(x)
    
    def print_generation(self,population):
        x = PrettyTable()
        print("--- Bảng thế hệ (fitness) ---")
        x.field_names = ["STT","Fitness","Conflicts","Thời khóa biểu([Classes])"]
        for i in range (0, len(population)):
            classes = population[i].get_classes()
            x.add_row([str(i),population[i].get_fitness(),population[i].get_numberOfConflicts(),[str(x) for x in classes]])
            # [str(x) for x in  classes]
        x.align["Thời khóa biểu([Classes])"] = "l"
        x.max_width["Thời khóa biểu([Classes])"] = 120
        print(x)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Population:
    def __init__(self, population_size):
        self._population_size = population_size
        self._schedules = []
        schedule = [Schedule(data).create_schedule() for i in range(population_size)]
        self._schedules = schedule
    def get_schedules(self):
        return self._schedules

class GA:
    def selection_tournament(self, population):
        tournament = Population(0)
        # Chọn ngẫu nhiên 5 schedule trong population
        for i in range (0,5):
            tournament.get_schedules().append(population.get_schedules()[random.randrange(0,len(population.get_schedules()))])
        # Sắp xếp các schedule theo fitness giảm dần
        tournament.get_schedules().sort(key=lambda x:float(x.get_fitness()), reverse=True)
        # Trả về schedule có fitness cao nhất
        return tournament.get_schedules()[0]
    
    def crossover(self, schedule1, schedule2):
        schedule_crossover = Schedule(data).create_schedule()
        for i in range (0,len(schedule_crossover.get_classes())):
            if(random.random() > 0.5):
                schedule_crossover.get_classes()[i] = schedule1.get_classes()[i]
            else:
                schedule_crossover.get_classes()[i] = schedule2.get_classes()[i]
        return schedule_crossover
    
    # list schedule - input
    def crossover_population(self, population,num_elite_schedule):
        crossover_pop = Population(0)
        # bổ sung cá thể tốt nhất vào quần thể mới
        for i in range(num_elite_schedule):
            crossover_pop.get_schedules().append(population.get_schedules()[i])
        # Lai ghép các cá thể còn lại
        i = num_elite_schedule
        while i < len(population.get_schedules()):
            schedule1 = self.selection_tournament(population)
            schedule2 = self.selection_tournament(population)
            crossover_pop.get_schedules().append(self.crossover(schedule1,schedule2))
            i += 1
        return crossover_pop

    def mutation(self, mutation_schedule,mutation_rate):
        schedule = Schedule(data).create_schedule()
        for i in range (0,len(mutation_schedule.get_classes())):
            if(mutation_rate > random.randint(0,100)):
                mutation_schedule.get_classes()[i] = schedule.get_classes()[i]
        return mutation_schedule

    def mutation_population (self,population, mutation_rate,num_elite_schedule):
        for i in range (num_elite_schedule, len(population.get_schedules())):
            population.get_schedules()[i] = self.mutation(population.get_schedules()[i],mutation_rate)
        return population
    
    # population là gồm nhiều schedule 
    def run(self, population,mutation_rate,num_elite_schedule):
        # Tiến hành lai ghép
        crossover_pop = self.crossover_population(population,num_elite_schedule)
        # Tiến hành đột biến
        mutation_pop = self.mutation_population(crossover_pop,mutation_rate,num_elite_schedule)
        return mutation_pop
data = Data()
def main():
    display = Display(data)
    best_fitness = 0
    # xác định dân số ban đầu của quần thể
    population_size = 10
    # xác định số thế hệ (lần lặp lại) thuật toán
    num_generations = 0
    # Tỉ lệ đột biến
    mutation_rate = 10
    # Số lượng chọn cá thể ưu tú để bỏ vào quần thể mới
    num_elite_schedule = 1

    # Tạo quần thể ban đầu
    population = Population(population_size)
    population.get_schedules().sort(key=lambda x:float(x.get_fitness()), reverse=True)
    best_fitness = population.get_schedules()[0].get_fitness()
    # Khởi tạo và chạy thuật toán GA
    ga = GA()
    start_time = time.time()

    while(float(best_fitness) != 1.000):
        num_generations += 1
        print('Số thế hệ: ', num_generations)
        population = ga.run(population,mutation_rate,num_elite_schedule)    
        population.get_schedules().sort(key=lambda x:float(x.get_fitness()), reverse=True)
        best_fitness = population.get_schedules()[0].get_fitness()
        print('Số lượng schedule trong quần thể: ', len(population.get_schedules()))
        print('Best schedule fitness: ', best_fitness)

    end_time = time.time()
    print("Thời gian chạy thuật toán: ", end_time - start_time, " giây")
    print('Best schedule fitness: ', best_fitness)
    display.print_schedule(population.get_schedules()[0])
    display.print_generation(population.get_schedules())

if __name__ == "__main__":
    main()

