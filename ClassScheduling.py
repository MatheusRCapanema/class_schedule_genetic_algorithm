import random

NUMB_OF_ELITE_SCHEDULES = 1
POPULATION_SIZE = 9
MUTATION_RATE = 0.3
TOURNAMENT_SELECTION_SIZE = 3


class Data:
    ROOMS = [["JB1", 60], ["JB2", 60], ["JA2/3", 80], ["IB3", 24], ["CB1", 48],
             ["CB2", 48], ["CB3", 48], ["CB4", 48], ["CB5", 48], ["IA5", 48],
             ["IA3", 48]]

    MEETING_TIMES = [["MT1", "SEGUNDA", "19:15 - 22:00"],
                     ["MT2", "TERÇA", "19:15 - 22:00"],
                     ["MT3", "QUARTA", "19:15 - 22:00"],
                     ["MT4", "QUINTA", "19:15 - 22:00"],
                     ["MT5", "SEXTA", "19:15 - 22:00"],
                     ["MT6", "SÁBADO", "19:15 - 22:00"]]

    INSTRUCTORS = [["I1", "Loert"],
                   ["I2", "Sofia"],
                   ["I3", "Bruno"],
                   ["I4", "Afonso"],
                   ["I5", "Carlos"],
                   ["I6", "Raul"],
                   ["I7", "Filipe"],
                   ["I8", "Thiago"],
                   ["I9", "Valnei"],
                   ["I10", "Akita"],
                   ["I11", "Letícia"],
                   ["I12", "Hernani"],
                   ["I13", "Lehrer"]]

    def __init__(self):
        self.rooms = []
        self.meeting_times = []
        self.instructors = []

        for room in self.ROOMS:
            self.rooms.append(Room(room[0], room[1]))
        for meeting_time in self.MEETING_TIMES:
            self.meeting_times.append(MeetingTime(meeting_time[0], meeting_time[1], meeting_time[2]))
        for instructor in self.INSTRUCTORS:
            self.instructors.append(Instructor(instructor[0], instructor[1]))

        courses_data = [

            ("C1", "Mat.Discreta", [self.instructors[8]], 48, [1, 2], 100),
            ("C2", "Geo.Analítica", [self.instructors[1]], 48, [1, 2], 90),
            ("C3", "APC I", [self.instructors[2]], 80, [1], 120),
            ("C4", "APC II", [self.instructors[2]], 48, [2], 110),
            ("C5", "Top.Matematica", [self.instructors[3]], 48, [1], 70),
            ("C6", "Calculo I", [self.instructors[4]], 48, [2], 95),
            ("C7", "Lógica", [self.instructors[5]], 48, [1, 2], 85),
            ("C8", "Est.Dados", [self.instructors[6]], 48, [3, 4], 105),
            ("C9", "Calculo II", [self.instructors[4]], 48, [3, 4], 100),
            ("C10", "Teo.Computação", [self.instructors[5]], 48, [3, 4], 88),
            ("C11", "PLP", [self.instructors[12]], 60, [5, 6], 95),
            ("C12", "Comp.Gráfica", [self.instructors[7]], 60, [5, 6], 80),
            ("C13", "PDM", [self.instructors[2]], 48, [5, 6], 75),
            ("C14", "Calc.Numérico", [self.instructors[8]], 80, [5, 6], 70),
            ("C15", "Tec.Web", [self.instructors[5]], 60, [5, 6], 90),
            ("C16", "Prob.Estatística", [self.instructors[9]], 48, [5, 6], 85),
            ("C17", "Int.Artificial II", [self.instructors[10]], 48, [7, 8], 80),
            ("C18", "An.Algoritimo", [self.instructors[12]], 80, [7, 8], 75),
            ("C19", "Adm. Serviços Internet", [self.instructors[11]], 48, [7, 8], 70),
            ("C20", "Top em BD", [self.instructors[2]], 60, [7, 8], 95),
            ("C21", "Sist Distr", [self.instructors[5]], 80, [7, 8], 100)
        ]

        self.courses = [Course(*course_data) for course_data in courses_data]

        dept1 = Department("MATH", [self.courses[0], self.courses[1], self.courses[4], self.courses[5],
                                    self.courses[8], self.courses[11], self.courses[12], self.courses[13],
                                    self.courses[15]])
        dept2 = Department("PROG", [self.courses[2], self.courses[3], self.courses[7], self.courses[14],
                                    self.courses[17]])
        dept3 = Department("TECH", [self.courses[6], self.courses[9], self.courses[10], self.courses[16],
                                    self.courses[18], self.courses[19], self.courses[20]])

        self.departments = [dept1, dept2, dept3]
        self.number_of_classes = sum(len(department.courses) for department in self.departments)

    def get_departments(self):
        return self.departments

    def get_rooms(self):
        return self.rooms

    def get_number_of_classes(self):
        return self.number_of_classes

    def get_instructors(self):
        return self.instructors

    def get_courses(self):
        return self.courses

    def get_meeting_times(self):
        return self.meeting_times


class Schedule:
    def __init__(self, data):
        self.data = data
        self.classes = []
        self.number_of_conflicts = 0
        self.fitness = -1
        self.class_numb = 0
        self.is_fitness_changed = True

    def initialize(self):
        self.classes = []
        for dept in self.data.get_departments():
            for course in dept.get_courses():
                new_class = Class(self.class_numb, dept, course)
                self.class_numb += 1
                self.classes.append(new_class)
        self.distribute_classes_evenly()
        self.is_fitness_changed = True
        return self

    def distribute_classes_evenly(self):
        meeting_times = self.data.get_meeting_times()
        rooms = self.data.get_rooms()
        instructors = self.data.get_instructors()

        # Assegura que cada dia da semana tenha pelo menos uma aula.
        day_classes = {day[1]: [] for day in self.data.MEETING_TIMES}
        for class_ in self.classes:
            day = random.choice(list(day_classes.keys()))
            time = random.choice(meeting_times)
            room = random.choice(rooms)
            instructor = random.choice(instructors)

            class_.set_meeting_time(time)
            class_.set_room(room)
            class_.set_instructor(instructor)
            day_classes[day].append(class_)

        # Verifica se algum dia ficou sem aulas e redistribui se necessário
        for day in day_classes.keys():
            if not day_classes[day]:  # Se o dia estiver vazio
                # Escolhe uma classe aleatória para realocar neste dia
                random_class = random.choice(self.classes)
                random_time = random.choice(meeting_times)
                random_class.set_meeting_time(random_time)
                day_classes[day].append(random_class)

    def select_time_room_instructor(self, course):
        available_times = self.data.get_meeting_times()
        available_rooms = self.data.get_rooms()
        available_instructors = course.instructors

        while available_times and available_rooms and available_instructors:
            meeting_time = random.choice(available_times)
            room = random.choice(available_rooms)
            instructor = random.choice(available_instructors)

            if not self.is_time_room_instructor_conflict(meeting_time, room, instructor):
                return meeting_time, room, instructor
        return None, None, None

    def is_time_room_instructor_conflict(self, meeting_time, room, instructor):
        for existing_class in self.classes:
            if existing_class.meeting_time.id == meeting_time.id:
                if existing_class.room.number == room.number:
                    return True
                if existing_class.instructor.id == instructor.id:
                    return True
        return False

    def calculate_fitness(self):
        self.number_of_conflicts = 0
        # Verifica conflitos de sala e instrutor no mesmo horário
        for i in range(len(self.classes)):
            for j in range(len(self.classes)):
                if i != j:
                    if self.classes[i].meeting_time == self.classes[j].meeting_time and \
                       (self.classes[i].room == self.classes[j].room or self.classes[i].instructor == self.classes[j].instructor):
                        self.number_of_conflicts += 1
        self.fitness = 1 / (1.0 * self.number_of_conflicts + 1)
        self.is_fitness_changed = False
        return self.fitness

    def get_classes(self):
        return self.classes

    def get_fitness(self):
        if self.is_fitness_changed:
            self.fitness = self.calculate_fitness()
            self.is_fitness_changed = False
        return self.fitness


class Population:
    def __init__(self, size, data):
        self.schedules = []
        for i in range(size):
            self.schedules.append(Schedule(data).initialize())

    def get_schedules(self):
        return self.schedules


class GeneticAlgorithm:
    @staticmethod
    def evolve(population):
        return GeneticAlgorithm.mutate_population(GeneticAlgorithm.crossover_population(population))

    @staticmethod
    def crossover_population(pop):
        crossover_pop = Population(0, pop.get_schedules()[0].data)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = GeneticAlgorithm.select_tournament_population(pop).get_schedules()[0]
            schedule2 = GeneticAlgorithm.select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(GeneticAlgorithm.crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    @staticmethod
    def mutate_population(population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            GeneticAlgorithm.mutate_schedule(population.get_schedules()[i])
        return population

    @staticmethod
    def crossover_schedule(schedule1, schedule2):
        crossover_schedule = Schedule(schedule1.data).initialize()
        min_len = min(len(schedule1.get_classes()), len(schedule2.get_classes()))
        for i in range(min_len):
            if random.random() > 0.5:
                crossover_schedule.get_classes().append(schedule1.get_classes()[i])
            else:
                crossover_schedule.get_classes().append(schedule2.get_classes()[i])
        return crossover_schedule

    @staticmethod
    def mutate_schedule(mutate_schedule):
        for class_ in mutate_schedule.get_classes():
            if MUTATION_RATE > random.random():
                new_meeting_time = random.choice(mutate_schedule.data.get_meeting_times())
                new_room = random.choice(mutate_schedule.data.get_rooms())
                class_.set_meeting_time(new_meeting_time)
                class_.set_room(new_room)
        mutate_schedule.calculate_fitness()

    @staticmethod
    def select_tournament_population(pop):
        tournament_pop = Population(0, pop.get_schedules()[0].data)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[random.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Course:
    def __init__(self, number, name, instructors, max_number_of_students, semesters, num_students):
        self.number = number
        self.name = name
        self.instructors = instructors
        self.max_number_of_students = max_number_of_students
        self.semesters = semesters
        self.num_students = num_students

    def get_semesters(self):
        return self.semesters

    def get_name(self):
        return self.name

    def get_max_number_of_students(self):
        return self.max_number_of_students

    def get_num_students(self):
        return self.num_students


class Instructor:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name


class Room:
    def __init__(self, number, seating_capacity):
        self.number = number
        self.seating_capacity = seating_capacity

    def get_id(self):
        return self.number

    def get_seating_capacity(self):
        return self.seating_capacity


class MeetingTime:
    def __init__(self, id, day, time):
        self.id = id
        self.day = day
        self.time = time

    def get_id(self):
        return self.id

    def get_day(self):
        return self.day

    def get_time(self):
        return self.time


class Department:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses

    def get_name(self):
        return self.name

    def get_courses(self):
        return self.courses


class Class:
    def __init__(self, id, dept, course, grade=None):
        self.id = id
        self.dept = dept
        self.course = course
        self.grade = grade
        self.instructor = None
        self.meeting_time = None
        self.room = None

    def get_id(self):
        return self.id

    def get_department(self):
        return self.dept

    def get_course(self):
        return self.course

    def get_instructor(self):
        return self.instructor

    def get_meeting_time(self):
        return self.meeting_time

    def get_room(self):
        return self.room

    def set_instructor(self, instructor):
        self.instructor = instructor

    def set_meeting_time(self, meeting_time):
        self.meeting_time = meeting_time

    def set_room(self, room):
        self.room = room

    def __str__(self):
        return str(self.dept.get_name() + "," + self.course.get_number()
                   + "," + self.room.get_number() + "," + str(self.instructor.get_id())
                   + "," + str(self.meeting_time.get_id()))


def run_genetic_algorithm():
    data = Data()
    generation_number = 0
    max_generations = 1000  # Define um limite para o número de gerações para evitar um loop infinito

    # Inicializa a população
    population = Population(POPULATION_SIZE, data)

    # Calcula o fitness para a população inicial
    population.schedules.sort(key=lambda x: x.get_fitness(), reverse=True)

    # Enquanto não encontrar a solução ideal e não atingir o limite de gerações
    while population.schedules[0].get_fitness() < 1.0 and generation_number < max_generations:
        generation_number += 1
        print(f"Geracao {generation_number}, Melhor fitness: {population.schedules[0].get_fitness()}")

        # Evolui a população
        population = GeneticAlgorithm().evolve(population)

        # Ordena a população pelo fitness, para facilitar a verificação do melhor indivíduo
        population.schedules.sort(key=lambda x: x.get_fitness(), reverse=True)

    # Imprime a melhor grade horária encontrada
    best_schedule = population.schedules[0]
    print_schedule_by_semester(best_schedule)


def print_schedule_by_semester(best_schedule):
    # Organize courses by semester, day of the week, and time
    schedule_by_semester = {}
    day_order = {mt[1]: i for i, mt in enumerate(Data.MEETING_TIMES)}  # Maps days to their order

    for class_ in best_schedule.get_classes():
        for semester in class_.course.get_semesters():
            if semester not in schedule_by_semester:
                schedule_by_semester[semester] = {day[1]: [] for day in Data.MEETING_TIMES}  # Initialize all days
            day = class_.meeting_time.get_day()
            schedule_by_semester[semester][day].append(class_)

    for semester in sorted(schedule_by_semester.keys()):
        print(f"\n=== Semestre {semester} ===")
        for day in Data.MEETING_TIMES:  # Ensure order and inclusion of all days
            day_name = day[1]
            print(f"\nDia: {day_name}")
            classes = schedule_by_semester[semester][day_name]
            if not classes:  # No classes scheduled for this day
                print(" Sem aulas")
                continue
            for class_ in sorted(classes, key=lambda x: x.meeting_time.get_time()):
                print(
                    f"{class_.meeting_time.get_time()} | {class_.course.get_name()} | Sala: {class_.room.get_id()} | Prof: {class_.instructor.get_name()}")
        print("\n" + "-" * 50)


run_genetic_algorithm()
