import requests
import re

class Student:
    def __init__(self, idnp) -> None:
        self.idnp = idnp
        self.completed = False
        self.payload = {"code": 0}

    def getData(self):
        response = requests.post("https://api.ceiti.md/date/login", data={"idnp": str(self.idnp)})
        content = response.content
        payload = {"code": 0}
        if b'method="post"' in content:
            self.completed = True
            return {"code": 405, "motiv": "INDP Invalid"}
        # the data is in bytes, .decote('utf-8') brings it back to unicode
        payload['nume'] = re.findall(b"<th>Numele</th>\n.*<td>(.*?)</td>", content)[0].decode('utf-8')
        payload['prenume'] = re.findall(b"<th>Prenumele</th>\n.*<td>(.*?)</td>", content)[0].decode('utf-8')
        payload['anul'] = {"I": 1, "II": 2, "III": 3, "IV": 4}[re.findall(b"<th>Anul de studii</th>\n.*<td>(.*?)</td>", content)[0].decode('utf-8')]
        payload['diriginte'] = re.findall(b"<th>Diriginte</th>\n.*<td>(.*?)</td>", content)[0].decode('utf-8')
        payload['grupa'] = re.findall(b"<th>Grupa</th>\n.*<td>(.*?)</td>", content)[0].decode('utf-8')
        payload['specialitate'] = re.findall(b"<th>Specialitatea</th>\n.*?<td>(.*?)</td>", content)[0].split(b',')[0].decode('utf-8')
        payload['semestre'] = [{}, {}]
        # load data for the semesters ->
        # every semester is in a div marked by collaps3e followed by the number of the semester
        # which then is followed by a table which contains all grades this regex will match
        # both semesters by finding the collaps3e div, and the closing element of the table
        semester_data = re.findall(b"<div id=\"collaps3e[1-2]\".+?/tr>(.*?)</table>", content, (re.S))
        for index, semester in enumerate(semester_data):
            # every subject and list of grades is held in a html paragraph
            # this extracts all of them, where every odd index is a subject
            # and the following even index is the grades
            subjects = re.findall(b"<p>(.*?)</p>", semester, (re.S))
            # every subject in a list of two elements: [subject, grade]
            subjects_organized = [subjects[i:i+2] for i in range(0, len(subjects), 2)]
            for subject_name, subject_grade in subjects_organized:
                grades_list = [int(element) for element in subject_grade.decode('utf-8').split(', ') if element.isdigit()]
                payload['semestre'][index][subject_name.decode('utf-8')] = grades_list
            payload['semestre'][index]['absente'] = {}
            # same premise, but with absences: stored in <td><i> tags
            absente = re.findall(b"<td><i>(.*?)</i></td>", semester)
            absente_organized = [absente[i:i+2] for i in range(0, len(absente), 2)]
            for absence_type, absence_nr in absente_organized:
                payload['semestre'][index]['absente'][absence_type.decode('utf-8')] = int(absence_nr)
            # total absences do not include "Bolnav". extracting them with regex is 
            # quicker and shorter than doing the math
            payload['semestre'][index]['absente']['Total'] = int(re.findall(b"<th>Absen.*<th>([0-100]*)", semester, (re.S))[0])
        payload['examene'] = []
        # exams are stored in the exact same way as subject grades, but the id 
        # of the div is called collapse (not collaps3e) followed by the number
        exams = re.findall(b"<div id=\"collapse[0-7]\".+?/tr>(.*?)</table>", content, (re.S))
        for index, semester in enumerate(exams):
            payload['examene'].append({})
            exams_data = re.findall(b"<p>(.*?)</p>", semester, (re.S))
            exams_organized = [exams_data[i:i+2] for i in range(0, len(exams_data), 2)]
            for exam_name, exam_grade in exams_organized:
                payload['examene'][index][exam_name.decode('utf-8')] = float(exam_grade.replace(b'---', b'0'))
        payload['code'] = 200
        self.payload = payload
        self.completed = True
        return payload

