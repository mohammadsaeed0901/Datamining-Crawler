import csv
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger('__main__')


class RUG:
    Course_Page_Url = "https://www.rug.nl/ocasys/rug/main/courseSearchResults?keywords=&code=&faculty=rug&cLevelRestrictionsState=0&cLangRestrictionsState=0&cPeriodRestrictionsState=0&new=1&cOptionsState=none"
    University = "University of Groningen"
    Abbreviation = "RUG"
    University_Homepage = "https://www.rug.nl/ocasys/rug/main"

    Objective = None
    Unit_Count = None
    Required_Skills = None
    Scores = None
    Projects = None
    References = None

    output_file = None
    course_count = 0

    def __init__(self):
        self.output_file = csv.writer(
            open(f'data/{self.__class__.__name__}.csv', 'w', encoding='utf-8', newline=''))
        self.output_file.writerow(
            ['University', 'Abbreviation', 'Department', 'Course title', 'Unit', 'Professor', 'Objective',
             'Prerequisite', 'Required Skills', 'Outcome', 'References', 'Scores', 'Description', 'Projects',
             'University Homepage', 'Course Homepage', 'Professor Homepage']
        )

    def get_courses_of_department(self, department):
        ...

    def get_course_data(self, course):
        a_element = course.find('a')
        if a_element is not None:
            department_url = "http://www.rug.nl" + a_element.get('href')
            Course_Homepage = department_url

            department_page_content = requests.get(department_url).content
            department_soup = BeautifulSoup(
                department_page_content, 'html.parser')

            headerTable = department_soup.find(class_="userTable")

            header_names = headerTable.find_all('tr')

            for header_name in header_names:
                data = header_name.find('td', class_='fieldLabel')

                if data is not None:
                    results = data.findNext('td')
                    try:
                        if data.text == 'Faculteit':
                            Department_Name = results.text.strip()
                    except:
                        Department_Name = None

            courses = department_soup.find(class_="detailTable")

            details_name = courses.find_all('tr')

            for detail_name in details_name:
                # find title of data's
                data = detail_name.find('td', class_='fieldLabel')

                if data is not None:
                    results = data.findNext('td')
                    try:
                        if data.text == 'Leerdoelen':
                            Outcome = results.text.strip()
                    except:
                        Outcome = None

                    try:
                        if data.text == 'Entreevoorwaarden':
                            Prerequisite = results.text.strip()
                    except:
                        Prerequisite = None

                    try:
                        if data.text == 'Uitgebreide vaknaam':
                            Course_Title = results.text.strip()
                    except:
                        Course_Title = None

                    try:
                        if data.text == 'Omschrijving':
                            Description = results.text.strip()
                    except:
                        Description = None

                    try:
                        if data.text == 'Docent(en)':
                            try:
                                Professor = results.text.replace(
                                    ",", " ").strip()
                            except:
                                Professor = None
                            try:
                                Professor_Homepage = "https://www.rug.nl" + \
                                    results.find('a').get('href')
                            except:
                                Professor_Homepage = None
                    except:
                        pass

            return Department_Name, Course_Title, Professor, Professor_Homepage, Outcome, Prerequisite, Description, Course_Homepage

    def save_course_data(self, university, abbreviation, department_name, course_title, unit_count, professor,
                         objective, prerequisite, required_skills, outcome, references, scores, description, projects,
                         university_homepage, course_homepage, professor_homepage):
        try:
            self.output_file.writerow([university, abbreviation, department_name, course_title, unit_count, professor,
                                       objective, prerequisite, required_skills, outcome, references, scores,
                                       description, projects, university_homepage, course_homepage, professor_homepage])

            self.course_count += 1
        except Exception as e:
            logger.error(
                f"{abbreviation} - {department_name} - {course_title}: An error occurred while saving course data: {e}"
            )

    def handler(self):
        html_content = requests.get(self.Course_Page_Url).content
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find(class_='userTable')
        courses = table.find_all('tr')

        for course in courses:
            try:
                Department_Name, Course_Title, Professor, Professor_Homepage, Outcome, Prerequisite, Description, Course_Homepage = self.get_course_data(
                    course)
            except:
                Department_Name = None
                Course_Title = None
                Professor = None
                Prerequisite = None
                Outcome = None
                Description = None
                Course_Homepage = None
                Professor_Homepage = None

            self.save_course_data(
                self.University, self.Abbreviation, Department_Name, Course_Title, self.Unit_Count,
                Professor, self.Objective, Prerequisite, self.Required_Skills, Outcome, self.References, self.Scores,
                Description, self.Projects, self.University_Homepage, Course_Homepage, Professor_Homepage
            )

        logger.info(
            f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")


RUG().handler()
