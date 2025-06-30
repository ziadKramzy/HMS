{
    "name" : "HMS",
    "summary": "hostpitals management system",
    "author" : "Ziad",
    'depends': ['base', 'contacts', 'crm'],
    "data" : [
        'security/hms_groups.xml',
        'security/ir.model.access.csv',
        'security/hms_record_rules.xml',
        'report/report.xml',
        'report/patient_status_report.xml',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/res_partner_view.xml',
    ],
}

