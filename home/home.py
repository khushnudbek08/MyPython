from datetime import date, timedelta

REST_LABEL = "Dam olish"

students = [
    "Otabek M",
    "Muhammad Sodiq",
    "Ibrohim",
    "Kamoldin",
    "Qodiriy",
    "Otabek P",
    "Xushnudbek",
]

tasks = [
    {
        "name": "Hammomni tozalash",
        "description": "Vanna ichi, pollar, kirmoshina ustini artish.",
    },
    {
        "name": "Honalarni supurish",
        "description": "Uy ichidagi barcha honalarni supurib, ahlatlarni olish.",
    },
    {
        "name": "Changlarni artish",
        "description": "Barcha honalar, oshhona, mebel, deraza tokcha va pollarni artish.",
    },
    {
        "name": "Hojatxonani tozalash",
        "description": "Pol, devor, unitaz ichi va qog'ozlarni tashqariga olib chiqish.",
    },
    {
        "name": "Gaz plitani tozalash",
        "description": "Gaz plita, folga, qozon va choynakdagi yog'larni ketkazib yuvish.",
    },
    {
        "name": "Holodilnikni tozalash",
        "description": "Oyna, ichi-tashi va muddati o'tgan narsalarni chiqarib tashlash.",
    },
]

first_fixed_person = "Otabek M"
first_fixed_task = "Hammomni tozalash"
num_rounds = 7


def first_sunday_from_today(today: date) -> date:
    days_until_sunday = (6 - today.weekday()) % 7
    return today + timedelta(days=days_until_sunday)


def validate_inputs() -> None:
    if len(students) != len(tasks) + 1:
        raise ValueError(
            "Talabalar soni ishlar sonidan aynan 1 taga ko'p bo'lishi kerak."
        )

    if first_fixed_person not in students:
        raise ValueError("Birinchi maxsus odam ro'yxatda topilmadi.")

    task_names = [task["name"] for task in tasks]
    if first_fixed_task not in task_names:
        raise ValueError("Birinchi maxsus ish ro'yxatda topilmadi.")


def build_rotation_symbols():
    task_names = [task["name"] for task in tasks]
    remaining_tasks = [name for name in task_names if name != first_fixed_task]
    return [first_fixed_task, *remaining_tasks, REST_LABEL]


def generate_schedule():
    validate_inputs()

    start_date = first_sunday_from_today(date.today())
    symbols = build_rotation_symbols()
    student_count = len(students)
    fixed_index = students.index(first_fixed_person)
    schedule = []

    for round_index in range(num_rounds):
        round_date = start_date + timedelta(days=14 * round_index)
        assignments = {}
        rest_person = None

        for student_index, student in enumerate(students):
            symbol_index = (student_index - fixed_index + round_index) % student_count
            assigned_item = symbols[symbol_index]

            if assigned_item == REST_LABEL:
                rest_person = student
            else:
                assignments[student] = assigned_item

        schedule.append(
            {
                "round_number": round_index + 1,
                "date": round_date,
                "rest_person": rest_person,
                "assignments": assignments,
            }
        )

    return schedule


def print_schedule(schedule):
    task_descriptions = {task["name"]: task["description"] for task in tasks}

    print("7 navbatlik tozalash ro'yxati")
    print(f"Birinchi sana: {schedule[0]['date'].isoformat()} (Yakshanba)")
    print("Har bir navbat 14 kunda bir marta takrorlanadi.")

    for round_info in schedule:
        print()
        print(
            f"{round_info['round_number']}-navbat | Sana: "
            f"{round_info['date'].isoformat()} (Yakshanba)"
        )
        print(f"Dam oladi: {round_info['rest_person']}")
        print("Ish taqsimoti:")

        for student, task_name in round_info["assignments"].items():
            description = task_descriptions[task_name]
            print(f"  {student} -> {task_name} -> {description}")


if __name__ == "__main__":
    print_schedule(generate_schedule())
