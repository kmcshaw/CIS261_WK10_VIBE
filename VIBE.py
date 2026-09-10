"""Student Grade Calculator.

Stores student records, calculates grades, and saves records in a
pipe-delimited text file.
"""

FILE_NAME = "student_grades.txt"


class Student:
	"""A student record with three test scores and calculated results."""

	def __init__(self, name, student_id, test_scores):
		self.name = name
		self.student_id = student_id
		self.test_scores = test_scores
		self.average = sum(test_scores) / len(test_scores)
		self.grade = calculate_letter_grade(self.average)


def calculate_letter_grade(average):
	"""Return the letter grade for an average score."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def get_score(test_number):
	"""Prompt until a valid score from 0 through 100 is entered."""
	while True:
		try:
			score = float(input(f"Test {test_number} score (0-100): "))
			if 0 <= score <= 100:
				return score
			print("Score must be between 0 and 100.")
		except ValueError:
			print("Please enter a numeric score.")


def add_student(students):
	"""Prompt for and add one student record."""
	print("\nAdd Student")
	name = input("Student name: ").strip()
	student_id = input("Student ID: ").strip()

	if not name or not student_id:
		print("Name and student ID are required.")
		return

	scores = [get_score(number) for number in range(1, 4)]
	students.append(Student(name, student_id, scores))
	print(f"Added {name} with average {students[-1].average:.2f} ({students[-1].grade}).")


def display_students(students):
	"""Display all student records in a formatted table."""
	if not students:
		print("\nNo student records found.")
		return

	print("\nStudent Records")
	print("-" * 86)
	print(
		f"{'Name':<22}{'ID':<14}{'Test 1':>10}{'Test 2':>10}"
		f"{'Test 3':>10}{'Average':>11}{'Grade':>9}"
	)
	print("-" * 86)
	for student in students:
		print(
			f"{student.name:<22.22}{student.student_id:<14.14}"
			f"{student.test_scores[0]:>10.2f}{student.test_scores[1]:>10.2f}"
			f"{student.test_scores[2]:>10.2f}{student.average:>11.2f}"
			f"{student.grade:>9}"
		)
	print("-" * 86)


def display_statistics(students):
	"""Display highest, lowest, and overall class averages."""
	if not students:
		print("\nNo student records available for statistics.")
		return

	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	class_average = sum(student.average for student in students) / len(students)

	print("\nClass Statistics")
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average:  {lowest.average:.2f} ({lowest.name})")
	print(f"Class average:   {class_average:.2f}")


def search_student(students):
	"""Find and display records whose names contain the search text."""
	search_text = input("\nEnter student name to search: ").strip().lower()
	matches = [student for student in students if search_text in student.name.lower()]

	if matches:
		display_students(matches)
	else:
		print(f"No student found matching '{search_text}'.")


def save_students(students, file_name=FILE_NAME):
	"""Save all student records in the required pipe-delimited format."""
	try:
		with open(file_name, "w", encoding="utf-8") as file:
			for student in students:
				scores = "|".join(f"{score:.2f}" for score in student.test_scores)
				file.write(
					f"{student.name}|{student.student_id}|{scores}|"
					f"{student.average:.2f}|{student.grade}\n"
				)
		print(f"Saved {len(students)} student record(s) to {file_name}.")
	except OSError as error:
		print(f"Unable to save student records: {error}")


def load_students(file_name=FILE_NAME):
	"""Load student records, skipping malformed lines with a message."""
	students = []
	try:
		with open(file_name, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipped invalid record on line {line_number}.")
					continue
				try:
					scores = [float(fields[index]) for index in range(2, 5)]
					if any(score < 0 or score > 100 for score in scores):
						raise ValueError
					students.append(Student(fields[0], fields[1], scores))
				except ValueError:
					print(f"Skipped invalid record on line {line_number}.")
		print(f"Loaded {len(students)} student record(s) from {file_name}.")
	except FileNotFoundError:
		print(f"No existing {file_name} file found. Starting with an empty list.")
	except OSError as error:
		print(f"Unable to load student records: {error}")
	return students


def display_menu():
	"""Display the main menu."""
	print("\nStudent Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search for a student")
	print("5. Save records")
	print("Press ESC, or enter 0, to exit")


def main():
	"""Run the student grade calculator."""
	students = load_students()

	while True:
		display_menu()
		choice = input("Select an option: ")

		if choice == "\x1b" or choice.strip() == "0":
			save_students(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		elif choice == "5":
			save_students(students)
		else:
			print("Invalid option. Please choose 1 through 5, or press ESC to exit.")


if __name__ == "__main__":
	main()