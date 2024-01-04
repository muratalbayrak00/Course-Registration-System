from typing import List
from JsonParser import JSONParser
from CourseRegistrationSystem import CourseRegistrationSystem
from Grade import Grade
from Advisor import Advisor
from CourseSection import CourseSection
from Student import Student
from JsonMethods import JSONMethods

class SystemController:
    def __init__(self):
        self.student = None
        self.student_list = []
        self.advisor = None
        self.advisor_list = []
        self.course_list = []

    def main(self):
        print("Welcome to the system!")
        self.login()

    def login(self):
        jP = JSONParser()
        global student_list
        global course_list
        global advisor_list
        student_list = jP.parse_students()
        course_list = jP.parse_courses()
        advisor_list = jP.parse_advisor()

        try:
            print("1: Student\n2: Advisor\n0: Close System")
            user_type = int(input())

            if user_type < 0 or user_type > 2:
                print("Invalid input, try again!")
                self.login()
                return

            if user_type == 0:
                print("Exiting...")
                exit(1)
            if user_type == 1:
                self.login_as_student()
            elif user_type == 2:
                self.login_as_advisor()
        except ValueError:
            print("Invalid input, try again!")
            self.login()

    def welcome_student(self):
        try:
            print("Please choose what you want to do:\n1: View transcript\n2: Course Registration\n3: Request Final Project\n4: View course schedule\n0: Log out")
            i = int(input())
            if i < 0 or i > 4:
                print("Invalid input, try again!")
                self.welcome_student()
                return
            if i == 1:
                self.show_transcript_screen(student)
            elif i == 2:
                self.course_registration_screen(student, course_list)
            elif i == 3:
                self.show_final_request(student)
            elif i == 4:
                self.show_schedule_screen(student)
            else:
                print("Logging out...")
                self.login()
                return
        except ValueError:
            print("Invalid input, try again!")
            self.welcome_student()
    
    def login_as_student(self):
        username = input("Username: ")
        password = input("Password: ")
        global student
        student = self.find_student(username)
        if student is not None and student.password == password:
            self.student = student
            print("Welcome", student.name)
            self.welcome_student()
        else:
            print("Username or password is incorrect!")
            self.login_as_student()

    def find_student(self, username):
        for student in student_list:
            if (student.username == username):
                return student
        return None
    
    def find_advisor(self, username):
        for advisor in advisor_list:
            if (advisor.get_username() == username):
                return advisor
        return None
    
    def welcome_advisor(self, advisor) -> None:
        global student_list
        advisor.set_advised_students_init(student_list)
        request_students = advisor.list_requested_students()
        crg = CourseRegistrationSystem()

        if not request_students:
            self.handle_no_course_requests()
        else:
            self.handle_course_requests(request_students, crg)
    
    def login_as_advisor(self, username="", password=""):
        username = input("Username: ")
        password = input("Password: ")
        global advisor
        advisor = self.find_advisor(username)
        if advisor and advisor.get_password() == password:
            # Login successful
            print(f"Welcome {advisor.get_name()}")
            self.welcome_advisor(advisor)
        else:
            print("Username or password is incorrect!")
            self.login_as_advisor_input()

    def login_as_advisor_input(self):
        try:
            username = input("Username: ")
            password = input("Password: ")
            self.login_as_advisor(username, password)
        except ValueError:
            print("Username or password is incorrect!")
            self.login_as_advisor()

   

    def view_student_transcript(self,advisor):
        try:
            print(advisor.students_to_string())
            print("X: Enter the index of the student whose transcript you want to see.\n0: Go back to the main menu")

            student_index = int(input())

            advised_students = advisor.get_advised_students()
            if 0 < student_index <= len(advised_students):
                selected_student = advised_students[student_index - 1]
                print(f"Student ID: {selected_student.get_student_id()}\nGPA: {selected_student.get_gpa()}\nTranscript of the selected student: \n{selected_student.view_transcript()}")
                self.handle_back_option(advisor)
            elif student_index == 0:
                self.welcome_advisor(advisor)
            else:
                print("Invalid index, returning to the main menu.")
                self.welcome_advisor(advisor)
        except ValueError:
            print("Invalid index, returning to the main menu.")
            self.welcome_advisor(advisor)
        
    def handle_back_option(self, advisor):
        try:
            print("1: Back to view advised students\n0: Go back to the main menu")
            back_option = int(input())

            if back_option == 1:
                self.view_student_transcript(advisor)
            elif back_option == 0:
                self.welcome_advisor(advisor)
            else:
                print("Invalid option, returning to the main menu.")
                self.welcome_advisor(advisor)
        except ValueError:
            print("Invalid option, returning to the main menu.")
            self.welcome_advisor(advisor)

    def show_schedule_screen(self, student):
        if student.get_enrolled_courses():
            self.show_student_schedule(student)
        else:
            print("Your course schedule cannot be viewed because you are not registered for the courses. Return main menu...")
            self.welcome_student()
            
    def show_transcript_screen(self, student):
        try:
            print(student.view_transcript().__str__())
            for c in student.get_enrolled_courses():
                g = Grade(c, "--")
                print(g.__str__())
            
            print("\n1: Go back to main menu")
            l = int(input())
            if l != 1:
                print("Invalid Input, going to the main menu")
            self.welcome_student()
            return

        except ValueError:
            print("Invalid Input, going to the main menu")
            self.welcome_student()

    def course_registration_screen(self, student, course_list):
        if student.get_requested_courses():
            print("You already sent your list. Here are the courses that were sent to the advisor:")
            requested = student.get_requested_courses()
            l = 1
            headers_requested_courses = f"      {'Course ID':<15} {'Course Name':<40} {'Credit':<8} {'Prerequisite Lesson':<20} {'Term':<10} {'Instructor':<20}"
            print(headers_requested_courses)
            for course in requested:
                print(f"{l}- {course.__str__()}")
                l += 1
            self.welcome_student()
            return

        if student.get_enrolled_courses():
            print("You have already registered for courses. Here are your courses:")
            enrolled = student.get_enrolled_courses()
            l = 1
            headers_enrolled_courses = f"      {'Course ID':<15} {'Course Name':<40} {'Credit':<8} {'Prerequisite Lesson':<20} {'Term':<10} {'Day-Hour':<23} {'Instructor':<20}"
            print(headers_enrolled_courses)
            for course in enrolled:
                print(f"{l}- {course.__str__()}")
                l += 1
            self.welcome_student()
            return

        course_registration_system = CourseRegistrationSystem(student, course_list)
        available_courses = course_registration_system.list_available_courses()
        n = 1
        headers_available_courses = f"      {'Course ID':<15} {'Course Name':<40} {'Credit':<8} {'Prerequisite Lesson':<20} {'Term':<10} {'Day-Hour':<23} {'Instructor':<20}"
        print(headers_available_courses)
        for available_course in available_courses:
            print(f"{n}: {available_course.__str__()}")
            n += 1

        try:
            print("Please write the number of the courses you want to enroll with commas")
            selected = input().strip().split(",")
            number_of_nte = 0
            number_of_fte = 0
            number_of_te = 0

            for s in selected:
                selected_course = available_courses[int(s) - 1]
                course_code = selected_course.get_course_id()

                if course_code.startswith("NTE"):
                    number_of_nte += 1
                elif course_code.startswith("FTE"):
                    number_of_fte += 1
                elif course_code.startswith("TE"):
                    number_of_te += 1

            if number_of_nte > 1 or number_of_fte > 1 or number_of_te > 1:
                print("You can't select more than 1 NTE, 1 FTE, and 1 TE course.")
                self.course_registration_screen(student, course_list)
                return

            for s in selected:
                if int(s) > len(available_courses) or int(s) < 1:
                    print(f"Enter valid numbers 1 to {len(available_courses)}\ntry again")
                    self.welcome_student()
                    return

            if len(student.get_enrolled_courses()) + len(selected) > 8:
                print(f"You have already enrolled {len(student.get_enrolled_courses())} courses, "
                    f"you can select a maximum of {8 - len(student.get_enrolled_courses())} courses")
                self.course_registration_screen(student, course_list)
                return

            requested_courses = [available_courses[int(s) - 1] for s in selected]
            for course in requested_courses:
                if course.get_course_section().get_enrollment_capacity() == 0:
                    print(f"Your course selection {course.get_course_name()}'s capacity is full, do not select it")
                    self.course_registration_screen(student, course_list)
                    return

            conflict_msg = course_registration_system.check_for_conflicts(requested_courses)
            if conflict_msg != "":
                print(conflict_msg)
                self.course_registration_screen(student, course_list)
                return
            for s in selected:
                course_registration_system.request_in_course(available_courses[int(s) - 1], student)
            print("Selected courses sent to the advisor")
            self.welcome_student()

        except ValueError:
            print("Invalid input. Please enter valid course numbers.")
            self.course_registration_screen(student, course_list)
    
    def show_final_request(self, student):
        try:
            if student.get_total_credits() >= 105 and student.get_semester() >= 7:
                if not student.get_project_assistant():
                    print("Select your project assistant:\n1: Betül Boz\n2: Borahan Tümer\n3: Beste Turanlı\n4: Çiğdem Eroğlu")
                    selected_ass = int(input())
                    json_methods = JSONMethods()
                    if 1 <= selected_ass <= 4:
                        assistants = ["Betül Boz", "Borahan Tümer", "Beste Turanlı", "Çiğdem Eroğlu"]
                        selected_assistant = assistants[selected_ass - 1]
                        print(f"You now have taken the project\nProject Assistant: {selected_assistant}")
                        json_methods.update_project_assistant(student, selected_assistant)
                    else:
                        print("Invalid index. Please enter a valid assistant number.")
                        self.show_final_request(student)
                else:
                    print(f"You already selected your project assistant\nYour project assistant is {student.get_project_assistant()}")
                self.welcome_student()
            else:
                print("You cannot take the final project because your credits or semester do not satisfy our department rules")
                self.welcome_student()
        except ValueError:
            print("Invalid input. Please enter a number.")
            self.show_final_request(student)


    def show_student_schedule(self, student):
        try:
            enrolled_courses = student.get_enrolled_courses()
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            for day in days:
                print(f"{day}:")
                hours = self.get_hour_from_course_sections(day, student)
                hours.sort()
                print("|     Time      | Course ID |               Course Name                |          Instructor        |")
                print("|---------------|-----------|------------------------------------------|----------------------------|")

                for hour in hours:
                    for course in enrolled_courses:
                        course_section = course.get_course_section()
                        if course_section.get_day().lower() == day.lower() and course_section.get_hour() == hour:
                            print(f"| {hour:<13} | {course.get_course_id():<9} | {course.get_course_name():<40} | {course_section.get_instructor():<27}|")

                print()

            print("0: Back to the main menu")
            choice = int(input())
            if choice == 0:
                self.welcome_student()
            else:
                print("Invalid Input, returning to the main menu..")
                self.welcome_student()
        except ValueError:
            print("Invalid Input, returning to the main menu..")
            self.welcome_student()

    def get_hour_from_course_sections(self, day: str, student) -> List[str]:
        course_sections = self.get_course_sections_for_day(day, student)
        return [cs.get_hour() for cs in course_sections]

    def get_course_sections_for_day(self, day: str, student) -> List[CourseSection]:
        enrolled_courses = student.get_enrolled_courses()
        return [course.get_course_section() for course in enrolled_courses if course.get_course_section().get_day().lower() == day.lower()]

    def sort_hours(hours: List[str]):
        hours.sort(key=lambda x: int(x.split(":")[0]))

    def handle_no_course_requests(self):
        try:
            print("There are no students who have course requests.\n")
            print("Please choose what you want to do:\n1: View advised students\n0: Log out")

            choice = int(input())

            if choice == 1:
                self.view_student_transcript(advisor)
            elif choice == 0:
                print("Logging out...")
                self.login()
            else:
                print("Invalid input, try again!")
                self.welcome_advisor(advisor)
        except ValueError:
            print("Invalid input, try again!")
            self.welcome_advisor(advisor)

    def handle_course_requests(self, request_students: List[Student], crg):
        try:
            print("There are student(s) who want to enroll in the course...\n")
            print("Please choose what you want to do:\n1: View advised students\n2: See advised students who wants to enroll classes\n0: Log out")

            choice = int(input())

            if choice == 1:
                self.view_student_transcript(advisor)
            elif choice == 2:
                self.view_and_approve_courses(request_students, crg)
            elif choice == 0:
                print("Logging out...")
                self.login()
            else:
                print("Invalid input, try again!")
                self.welcome_advisor(advisor)
        except ValueError:
            print("Invalid input, try again!")
            self.welcome_advisor(advisor)

    def view_and_approve_courses(self, request_students, crg):
        student_index = self.display_requested_students(request_students)

        if student_index == -1:
            print("Invalid input, returning to the main menu")
            self.welcome_advisor()
            return

        current_student = request_students[student_index - 1]
        req_courses = current_student.get_requested_courses()

        self.display_requested_courses(req_courses)

        try:
            print("Please write the number of the courses you want to approve, with commas (Others will be rejected)\n(For reject all, write 0)")
            user_input = input().strip()

            if user_input == "0":
                self.reject_all_courses(req_courses, crg)
            else:
                selected = user_input.split(",")

                for s in selected:
                    try:
                        course_index = int(s)
                        if course_index <= 0 or course_index > len(req_courses):
                            raise ValueError
                    except ValueError:
                        print("Invalid course number. Returning to the student list.")
                        self.view_and_approve_courses(request_students, crg)
                        return

                self.approve_selected_courses(selected, current_student, req_courses, crg)

            jM = JSONMethods()
            jM.clear_requested_courses(current_student)

            self.welcome_advisor(advisor)
        except ValueError:
            print("Invalid input. Please enter valid course numbers.")
            self.view_and_approve_courses(request_students, crg)


    def display_requested_students(self, request_students):
        a = 1

        headers_req_students = f"   {'Name':<30} {'Surname':<30} {'Student ID':<8}"
        print(headers_req_students)

        for s in request_students:
            print(f"{a}: {s.__str__()}")
            a += 1

        try:
            print("Please select which student you want to see: ")
            student_index = int(input())
            return student_index if 0 < student_index <= len(request_students) else -1
        except ValueError:
            input("Invalid input. Please enter a valid number.")
            return -1


    def display_requested_courses(self, req_courses):
        t = 1

        headers_req_course = f"      {'Course ID':<15} {'Course Name':<40} {'Credit':<8} {'Prerequisite Lesson':<20} {'Term':<10} {'Day-Hour':<23} {'Instructor':<20}"
        print(headers_req_course)

        for req_course in req_courses:
            print(f"{t}: {req_course.__str__()}")
            t += 1

    def should_reject_all(selected, req_courses):
        return len(selected) == 1 and int(selected[0]) == 0


    def reject_all_courses(self, req_courses, crg):
        for course in req_courses:
            crg.reject_course(course)
        print("All courses are rejected")


    def approve_selected_courses(self, selected, current_student, req_courses, crg):
        dummy_req_courses = req_courses

        for s in selected:
            course_index = int(s)

            if 0 < course_index <= len(dummy_req_courses):
                advisor.approve_course_registration(current_student, dummy_req_courses[course_index - 1])
                current_student.get_requested_courses().remove(dummy_req_courses[course_index - 1])

        for course in current_student.get_requested_courses():
            crg.reject_course(course)

        print("Selected courses are approved, others' rejected")

        

controller = SystemController()
controller.main()
