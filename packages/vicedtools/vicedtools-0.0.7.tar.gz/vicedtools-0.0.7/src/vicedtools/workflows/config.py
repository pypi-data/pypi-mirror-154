import os
import re

import numpy as np
import pandas as pd

root_dir = "C:\\Users\\08639305\\Documents\\lyndale data"

# vass
#iedriver_path = "C:\\Users\\08639305\\Documents\\data\\scripts and notebooks\\IEDriverServer.exe"
iedriver_path = "C:\\Users\\08639305\\Documents\\data\\scripts and notebooks\\IEDriverServer_win32_3141.exe"

vass_grid_password = [('4', '4'), ('5', '4'), ('4', '5'), ('5', '5'),
                      ('3', '6'), ('6', '6')]
vass_year = "2021"
vass_username = "gregb"
vass_password = """}{P][p00"""
vass_folder = "vass exports"
vass_dir = os.path.join(root_dir, vass_folder)
vass_student_details_dir = os.path.join(vass_dir, "personal details summary")
vass_school_program_dir = os.path.join(vass_dir, "school program summary")
vass_predicted_scores_dir = os.path.join(vass_dir, "predicted scores")
vass_school_scores_dir = os.path.join(vass_dir, "school scores")
vass_gat_scores_dir = os.path.join(vass_dir, "gat scores")
vass_external_scores_dir = os.path.join(vass_dir, "external scores")
vass_moderated_coursework_scores_dir = os.path.join(
    vass_dir, "moderated coursework scores")

# compass
from vicedtools.compass.compasssession import CompassConfigAuthenticator

compass_username = '08639305'
compass_password = '}{P][p00'
compass_school_code = "lyndale-vic"

compass_authenticator = CompassConfigAuthenticator(compass_username,
                                                   compass_password)
compass_folder = "compass exports"
student_details_folder = "student details"
sds_folder = "SDS export"
learning_tasks_folder = "learning tasks"
reports_folder = "reports"
progress_reports_folder = "progress reports"
student_details_csv = os.path.join(root_dir, compass_folder,
                                   student_details_folder,
                                   "student details.csv")
student_household_information_csv = os.path.join(
    root_dir, compass_folder, student_details_folder,
    "student household information.csv")
sds_dir = os.path.join(root_dir, compass_folder, sds_folder)
reports_file = os.path.join(root_dir, compass_folder, "reports.csv")
reports_summary_file = os.path.join(root_dir, compass_folder,
                                    "reports_summary.csv")
compass_dir = os.path.join(root_dir, compass_folder)
progress_reports_dir = os.path.join(root_dir, compass_folder,
                                    progress_reports_folder)
learning_tasks_dir = os.path.join(root_dir, compass_folder,
                                  learning_tasks_folder)
reports_dir = os.path.join(root_dir, compass_folder, reports_folder)
subjects_dir = os.path.join(compass_dir, "subjects")
class_details_dir = os.path.join(compass_dir, "class details")
academic_groups_json = os.path.join(compass_dir, "academic groups.json")
progress_report_cycles_json = os.path.join(compass_dir,
                                           "progress report cycles.json")
report_cycles_json = os.path.join(compass_dir, "report cycles.json")

# naplan
from vicedtools.naplan.dataservicesession import DataServiceConfigAuthenticator

dataservice_username = "LYND01"
dataservice_password = "WBF79nnt"
dataservice_authenticator = DataServiceConfigAuthenticator(
    dataservice_username, dataservice_password)
naplan_dir = os.path.join(root_dir, "naplan exports")
naplan_outcomes_dir = os.path.join(naplan_dir, "outcomes exports")
naplan_sssr_dir = os.path.join(naplan_dir, "sssr exports")

# oars
oars_username = "BRG"
oars_password = "}{P][p00acer!"
from vicedtools.acer import OARSConfigAuthenticator

oars_authenticator = OARSConfigAuthenticator(oars_username, oars_password)
oars_school_code = "lyndale-secondary-college"

oars_dir = os.path.join(root_dir, "OARS exports")
pat_scores_csv = os.path.join(oars_dir, "pat scores.csv")
pat_most_recent_csv = os.path.join(oars_dir, "pat most recent.csv")
ewrite_scores_csv = os.path.join(oars_dir, "eWrite scores.csv")
ewrite_criteria_csv = os.path.join(oars_dir, "eWrite criteria.csv")
pat_sittings_dir = os.path.join(oars_dir, "PAT sittings")
ewrite_sittings_dir = os.path.join(oars_dir, "eWrite sittings")
oars_tests_json = os.path.join(oars_dir, "tests.json")
scale_constructs_json = os.path.join(oars_dir, "scale constructs.json")
oars_staff_xlsx = os.path.join(oars_dir, f"{oars_school_code}-staff.xlsx")
oars_candidates_json = os.path.join(oars_dir, "candidates.json")

# gcp
student_details_table_id = "gwsc-school-data.student_details.student_details"
student_enrolments_table_id = "gwsc-school-data.student_details.student_enrolments"
pat_scores_table_id = "gwsc-school-data.student_results.pat_scores"
pat_most_recent_table_id = "gwsc-school-data.student_results.pat_most_recent"
naplan_outcomes_table_id = "gwsc-school-data.student_results.naplan"
reports_table_id = "gwsc-school-data.student_results.reports"
reports_summary_table_id = "gwsc-school-data.student_results.reports_summary"
gat_table_id = "gwsc-school-data.student_results.gat"
ewrite_scores_table_id = "gwsc-school-data.student_results.ewrite_scores"
ewrite_criteria_table_id = "gwsc-school-data.student_results.ewrite_criteria"
vce_study_scores_table_id = "gwsc-school-data.vce_data.study_scores"
vce_adjusted_scores_table_id = "gwsc-school-data.vce_data.adjusted_scores"
bucket = "gwsc-student-details"

# gwsc
subjects_file = "C:/Users/gbr/Documents/data/SDS exports/subjects metadata.csv"
replace_values = {"SubjectName": {}, "Result": {}}

replace_subject_codes = {
    "SubjectCode": {
        "GTR": "GTAR",
        "GUITAR": "GTAR",
        "VOICE": "VOX",
        "BASSGUITAR": "BGTR",
        "B_GTRA": "BGTR",
        "TRMPT": "TMPT",
        "VIOLIN": "VLN"
    }
}

grade_order = [
    'NA', ' NA (Not applicable)', 'Not Assessed', 'UG', 'Ungraded',
    'Not Satisfactory', 'E', 'Limited', 'Very Low', 'D', 'Low', 'C',
    'Satisfactory', 'Medium', 'Medium - High', 'B', 'Good', 'High', 'Very Good',
    'A', 'Excellent', 'Very High'
]
results_dtype = pd.api.types.CategoricalDtype(categories=grade_order,
                                              ordered=True)


def learning_task_filter(df):
    df = df.loc[df["IsIncludedInReport"] == True]
    df = df.loc[df["ComponentType"].isin([
        "Letter Grade - A, B, C, D, E", "Letter Grade - A, B, C, D, E, UG, NA"
    ])]
    return df


def learning_tasks_result_mapper(result):
    if result == "UG":
        return 0
    if result == "E":
        return 0.2
    if result == "D":
        return 0.4
    if result == "C":
        return 0.6
    if result == "B":
        return 0.8
    if result == "A":
        return 1.0
    return float('nan')


def work_habits_result_mapper(result):
    if result == "Unsatisfactory":
        return 0.2
    if result == "Needs Attention":
        return 0.4
    if result == "Acceptable":
        return 0.55
    if result == "Good":
        return 0.7
    if result == "Very Good":
        return 0.80
    if result == "Excellent":
        return 1.0
    return np.nan


def progress_report_result_mapper(result):
    if result == "Unsatisfactory":
        return 0.2
    if result == "Needs Attention":
        return 0.4
    if result == "Acceptable":
        return 0.5
    if result == "Good":
        return 0.65
    if result == "Very Good":
        return 0.80
    if result == "Excellent":
        return 1.0
    return np.nan


progress_report_items = [
    "Behaviour", "Classwork", "Effort", "Homework", "Self-Management"
]


def class_code_parser(class_code, pattern_string):
    m = re.search(pattern_string, class_code)
    if m:
        subject_code = m.group('code')
        # test for Global Goodies vs Geography
        if subject_code == "10GG":
            m = re.search("10GGD[12345]", class_code)
            if m:
                subject_code = "10GL"
        return subject_code
    else:
        print(class_code + " not found")
        return ""
