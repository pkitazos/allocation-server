from src.request_data import RequestData, StudentData, SupervisorData, ProjectData, RequestDataWithArgs


    
 
student_data = [
        {"id": "00", "preferences": ["p01"],},
        {"id": "01", "preferences": ["p01", "p02", "p03", "p04", "p05", "p06"],},
        {"id": "02", "preferences": ["p02", "p01", "p04"],},
        {"id": "03", "preferences": ["p02"],},
        {"id": "04", "preferences": ["p01", "p02", "p03", "p04"],},
        {"id": "05", "preferences": ["p02", "p03", "p04", "p05", "p06"],},
        {"id": "06", "preferences": ["p05", "p03", "p08"],},
        ]


supervisor_data =[
    {"id": "l01","lowerBound": 0,"upperBound": 2,"target": 3,},
    {"id": "l02","lowerBound": 0,"upperBound": 2,"target": 2,},
    {"id": "l03","lowerBound": 0,"upperBound": 2,"target": 2,},
    ]


project_data = [
        {"id": "p01","lowerBound": 0, "upperBound": 1, "supervisorId": "l01",},
        {"id": "p03","lowerBound": 0, "upperBound": 1, "supervisorId": "l01",},
        {"id": "p02","lowerBound": 0, "upperBound": 1, "supervisorId": "l01",},
        {"id": "p04","lowerBound": 0, "upperBound": 1, "supervisorId": "l02",},
        {"id": "p05","lowerBound": 0, "upperBound": 1, "supervisorId": "l02",},
        {"id": "p06","lowerBound": 0, "upperBound": 1, "supervisorId": "l02",},
        {"id": "p07","lowerBound": 0, "upperBound": 1, "supervisorId": "l03",},
        {"id": "p08","lowerBound": 0, "upperBound": 1, "supervisorId": "l03",},
        ]


my_students=[
        StudentData(id='00', preferences=['p01']), 
        StudentData(id='01', preferences=['p01', 'p02', 'p03', 'p04', 'p05', 'p06']), 
        StudentData(id='02', preferences=['p02', 'p01', 'p04']), 
        StudentData(id='03', preferences=['p02']), 
        StudentData(id='04', preferences=['p01', 'p02', 'p03', 'p04']), 
        StudentData(id='05', preferences=['p02', 'p03', 'p04', 'p05', 'p06']), 
        StudentData(id='06', preferences=['p05', 'p03', 'p08'])
] 

my_projects=[
        ProjectData(id='p01', lowerBound=0, upperBound=1, supervisorId='l01'), 
        ProjectData(id='p03', lowerBound=0, upperBound=1, supervisorId='l01'), 
        ProjectData(id='p02', lowerBound=0, upperBound=1, supervisorId='l01'), 
        ProjectData(id='p04', lowerBound=0, upperBound=1, supervisorId='l02'), 
        ProjectData(id='p05', lowerBound=0, upperBound=1, supervisorId='l02'), 
        ProjectData(id='p06', lowerBound=0, upperBound=1, supervisorId='l02'), 
        ProjectData(id='p07', lowerBound=0, upperBound=1, supervisorId='l03'), 
        ProjectData(id='p08', lowerBound=0, upperBound=1, supervisorId='l03')
] 

my_supervisors=[
        SupervisorData(id='l01', lowerBound=0, target=3, upperBound=2), 
        SupervisorData(id='l02', lowerBound=0, target=2, upperBound=2), 
        SupervisorData(id='l03', lowerBound=0, target=2, upperBound=2)]



test_data = RequestData(students=my_students, supervisors=my_supervisors, projects=my_projects)



new_students=[
        StudentData(id='001-234567k', preferences=['prjkt-014-001', 'prjkt-004-001', 'prjkt-006-001', 'prjkt-012-001', 'prjkt-019-001', 'prjkt-020-001']), 
        StudentData(id='001-234568g', preferences=['prjkt-011-001', 'prjkt-015-001', 'prjkt-009-001', 'prjkt-007-001', 'prjkt-010-001', 'prjkt-012-001']), 
        StudentData(id='001-234569c', preferences=['prjkt-020-001', 'prjkt-018-001', 'prjkt-008-001', 'prjkt-011-001', 'prjkt-010-001', 'prjkt-013-001']), 
        StudentData(id='001-234570p', preferences=['prjkt-007-001', 'prjkt-006-001', 'prjkt-008-001', 'prjkt-018-001', 'prjkt-005-001', 'prjkt-020-001']), 
        StudentData(id='001-234571d', preferences=['prjkt-005-001', 'prjkt-013-001', 'prjkt-020-001', 'prjkt-008-001', 'prjkt-017-001', 'prjkt-012-001']), 
        StudentData(id='001-234572c', preferences=['prjkt-015-001', 'prjkt-010-001', 'prjkt-008-001', 'prjkt-014-001', 'prjkt-001-001', 'prjkt-020-001']), 
        StudentData(id='001-234573b', preferences=['prjkt-018-001', 'prjkt-006-001', 'prjkt-005-001', 'prjkt-019-001', 'prjkt-015-001', 'prjkt-020-001']), 
        StudentData(id='001-234574o', preferences=['prjkt-015-001', 'prjkt-010-001', 'prjkt-004-001', 'prjkt-017-001', 'prjkt-008-001', 'prjkt-003-001']), 
        StudentData(id='001-234575y', preferences=['prjkt-007-001', 'prjkt-015-001', 'prjkt-013-001', 'prjkt-003-001', 'prjkt-006-001', 'prjkt-019-001']), 
        StudentData(id='001-234576n', preferences=['prjkt-001-001', 'prjkt-006-001', 'prjkt-018-001', 'prjkt-011-001', 'prjkt-017-001', 'prjkt-004-001']), 
        StudentData(id='001-234577r', preferences=['prjkt-020-001', 'prjkt-008-001', 'prjkt-002-001', 'prjkt-004-001', 'prjkt-018-001', 'prjkt-019-001']), 
        StudentData(id='001-234578a', preferences=['prjkt-004-001', 'prjkt-005-001', 'prjkt-011-001', 'prjkt-003-001', 'prjkt-013-001', 'prjkt-020-001']), 
        StudentData(id='001-234579k', preferences=['prjkt-013-001', 'prjkt-003-001', 'prjkt-020-001', 'prjkt-008-001', 'prjkt-017-001', 'prjkt-005-001']), 
        StudentData(id='001-234580h', preferences=['prjkt-015-001', 'prjkt-012-001', 'prjkt-017-001', 'prjkt-011-001', 'prjkt-002-001', 'prjkt-008-001'])
] 


new_projects=[
        ProjectData(id='prjkt-001-001', lowerBound=0, upperBound=1, supervisorId='001-123456s'), 
        ProjectData(id='prjkt-002-001', lowerBound=0, upperBound=1, supervisorId='001-123456s'), 
        ProjectData(id='prjkt-003-001', lowerBound=0, upperBound=1, supervisorId='001-123456s'), 
        ProjectData(id='prjkt-004-001', lowerBound=0, upperBound=1, supervisorId='001-123456s'), 
        ProjectData(id='prjkt-005-001', lowerBound=0, upperBound=1, supervisorId='001-123457j'), 
        ProjectData(id='prjkt-006-001', lowerBound=0, upperBound=1, supervisorId='001-123457j'), 
        ProjectData(id='prjkt-007-001', lowerBound=0, upperBound=1, supervisorId='001-123457j'), 
        ProjectData(id='prjkt-008-001', lowerBound=0, upperBound=1, supervisorId='001-123457j'), 
        ProjectData(id='prjkt-009-001', lowerBound=0, upperBound=1, supervisorId='001-123458t'), 
        ProjectData(id='prjkt-010-001', lowerBound=0, upperBound=1, supervisorId='001-123458t'), 
        ProjectData(id='prjkt-011-001', lowerBound=0, upperBound=1, supervisorId='001-123458t'), 
        ProjectData(id='prjkt-012-001', lowerBound=0, upperBound=1, supervisorId='001-123458t'), 
        ProjectData(id='prjkt-013-001', lowerBound=0, upperBound=1, supervisorId='001-123459l'), 
        ProjectData(id='prjkt-014-001', lowerBound=0, upperBound=1, supervisorId='001-123459l'), 
        ProjectData(id='prjkt-015-001', lowerBound=0, upperBound=1, supervisorId='001-123459l'), 
        ProjectData(id='prjkt-016-001', lowerBound=0, upperBound=1, supervisorId='001-123459l'), 
        ProjectData(id='prjkt-017-001', lowerBound=0, upperBound=1, supervisorId='001-123460d'), 
        ProjectData(id='prjkt-018-001', lowerBound=0, upperBound=1, supervisorId='001-123460d'), 
        ProjectData(id='prjkt-019-001', lowerBound=0, upperBound=1, supervisorId='001-123460d'), 
        ProjectData(id='prjkt-020-001', lowerBound=0, upperBound=1, supervisorId='001-123460d')
]

new_supervisors=[
        SupervisorData(id='001-123456s', lowerBound=0, target=1, upperBound=3), 
        SupervisorData(id='001-123457j', lowerBound=0, target=2, upperBound=3), 
        SupervisorData(id='001-123458t', lowerBound=0, target=2, upperBound=3), 
        SupervisorData(id='001-123459l', lowerBound=0, target=2, upperBound=3), 
        SupervisorData(id='001-123460d', lowerBound=0, target=2, upperBound=3)
]


new_real_test_data =  RequestData(students=new_students, supervisors=new_supervisors, projects=new_projects)