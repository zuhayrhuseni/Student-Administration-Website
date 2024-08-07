import pandas as pd
import json

def excel_to_json(excel_file, output_json_course, output_json_subj):
    try:
        #Read the Excel file
        df = pd.read_excel(excel_file)

        #Get the column names (first row in Excel)
        columns = df.columns.tolist()
        #columns lists to handle selection of data
        cskip = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "CLASSM_MEETING_TIME_START", "CLASSM_MEETING_TIME_END", "Subject", "Name", "Subject", "Number"]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        subjcols = ["Name", "Subject"]

        #lists of objects
        class_objects = []
        subj_objects = []
        #for duplicate checking
        courseids = set()
        courseidsec = set()

        #iterate by row
        count = 0
        num = 0
        for index, row in df.iterrows():
            #taking only sections of the sheet - whole thing is too much
            count += 1
            if count % (40 + 200) >= 40:
                continue
            #dictionary for each row
            courseid = row["Subject"] + " " + row["Number"]
            classes_dict = dict()
            for column in columns:
                if column not in cskip:
                    classes_dict[column] = row[column]
            classes_dict["CourseID"] = courseid

            #changing schedule formatting to fit database
            time = row["CLASSM_MEETING_TIME_START"] + " - " + row["CLASSM_MEETING_TIME_END"]
            Schedule = dict()
            for day in days:
                if row[day] == "Y":
                    Schedule[day] = time
            classes_dict["Schedule"] = Schedule
            cidsec = courseid + row["Section"]

            #checking for incomplete courses and duplicates
            if classes_dict["Schedule"] != {} and classes_dict["TeacherName"] != " " and classes_dict["Location"] != "." and cidsec not in courseidsec:
                classes_dict["StudentList"] = []
                classes_dict["TeacherID"] = ''
                class_objects.append(classes_dict)
                courseidsec.add(cidsec)
                num += 1
                #checking for duplicates
                if courseid not in courseids:
                    subj_dict = dict()
                    subj_dict["subject"] = row["Subject"]
                    subj_dict["courseid"] = courseid
                    subj_dict["Name"] = row["Name"]
                    courseids.add(courseid)
                    subj_objects.append(subj_dict)
        #number of courses that will be added
        print(num)
        #store json objects
        with open(output_json, 'w') as json_file:
            json.dump(class_objects, json_file, indent=2)
        print(f'Success: JSON objects written to {output_json}')

        with open(output_json_subj, 'w') as json_file:
            json.dump(subj_objects, json_file, indent=2)
        print(f'Success: JSON objects written to {output_json_subj}')

    except Exception as e:
        print(f'Error: {e}')

excel_file = 'resources/All_Classes_Table_Format_Spring.xlsx'
output_json = 'resources/All_Classes.json'
output_json_subjs = 'resources/All_Subjs.json'
excel_to_json(excel_file, output_json, output_json_subjs)
