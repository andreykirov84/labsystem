from django.urls import path
from labsystem.laboratory.views.analysis_field_views import CreateAnalysisFieldView, EditAnalysisFieldView, \
    delete_analysis_field_view, restore_analysis_field_view, AnalysisFieldsListView, DeletedAnalysisFieldsListView
from labsystem.laboratory.views.analysis_views import CreateAnalysisView, EditAnalysisView, delete_analysis_view, \
    restore_analysis_view, AnalysisListView, DeletedAnalysisListView, SearchAnalysesView
from labsystem.laboratory.views.department_views import DepartmentCreation, EditDepartment, delete_department, \
    restore_department, DepartmentsListView, DeletedDepartmentsListView
from labsystem.laboratory.views.health_facility_views import HealthFacilityCreation, EditHealthFacility, \
    delete_health_facility, restore_health_facility, HealthFacilityListView, DeletedHealthFacilityListView
from labsystem.laboratory.views.patient_views import PatientUserCreateView, PatientCreateView, EditPatientView, \
    PatientDetailsView, delete_patient_view, restore_patient_view, PatientsListView, DeletedPatientsListView, \
    AllPhysicianPatientsListView, SearchPatientsView
from labsystem.laboratory.views.physician_views import PhysicianListView, DeletedPhysicianListView, EditPhysicianView, \
    PhysicianDetailsView, delete_physician_view, restore_physician_view, PhysicianUserCreateView, PhysicianCreateView
from labsystem.laboratory.views.results_views import CreateResultView, EditResultView, PatientSpecificResultListView, \
    ResultDetailsView, EditResultLineView
from labsystem.laboratory.views.staff_views import StaffCreateView, StaffListView, StaffUserCreateView, \
    StaffDetailsView, delete_staff_view, restore_staff_view, DeletedStaffListView, EditStaffView
from labsystem.laboratory.views.main_views import HomeView, UserLoginView, UserLogoutView
from labsystem.laboratory.views.user_view import PasswordChangeView

urlpatterns = (
    path('', HomeView.as_view(), name='index'),
    path('users/login/', UserLoginView.as_view(), name='login user'),
    path('users/logout/', UserLogoutView.as_view(), name='logout user'),
    path('users/<int:pk>/password/change/', PasswordChangeView.as_view(), name='change password'),
    path('register/user_as_patient/', PatientUserCreateView.as_view(), name='create user_as_patient'),
    path('register/user_as_staff/', StaffUserCreateView.as_view(), name='create staff user'),
    path('register/user_as_physician/', PhysicianUserCreateView.as_view(), name='create physician user'),

    path('patients/create/<int:pk>/profile/', PatientCreateView.as_view(), name='create patient'),
    path('patients/<int:pk>/edit/', EditPatientView.as_view(), name='edit patient'),
    path('patients/<int:pk>/details/', PatientDetailsView.as_view(), name='show details patient'),
    path('patients/<int:pk>/delete/', delete_patient_view, name='delete patient'),
    path('patients/<int:pk>/restore/', restore_patient_view, name='restore patient'),
    path('patients/all', PatientsListView.as_view(), name='all patients'),
    path('patients/all/deleted/', DeletedPatientsListView.as_view(), name='all deleted patients'),
    path('patients/all/search/', SearchPatientsView.as_view(), name='search patient'),

    path('staffs/create/<int:pk>/profile', StaffCreateView.as_view(), name='create staff'),
    path('staffs/<int:pk>/edit/', EditStaffView.as_view(), name='edit staff'),
    path('staffs/<int:pk>/details/', StaffDetailsView.as_view(), name='show details staff'),
    path('staffs/<int:pk>/delete/', delete_staff_view, name='delete staff'),
    path('staffs/<int:pk>/restore/', restore_staff_view, name='restore staff'),
    path('staffs/all', StaffListView.as_view(), name='all staffs'),
    path('staffs/all/deleted/', DeletedStaffListView.as_view(), name='all deleted staffs'),

    path('physicians/create/<int:pk>/profile', PhysicianCreateView.as_view(), name='create physician'),
    path('physicians/<int:pk>/edit/', EditPhysicianView.as_view(), name='edit physician'),
    path('physicians/<int:pk>/details/', PhysicianDetailsView.as_view(), name='show details physician'),
    path('physicians/<int:pk>/delete/', delete_physician_view, name='delete physician'),
    path('physicians/<int:pk>/restore/', restore_physician_view, name='restore physician'),
    path('physicians/all', PhysicianListView.as_view(), name='all physicians'),
    path('physicians/all/deleted/', DeletedPhysicianListView.as_view(), name='all deleted physicians'),
    path('physicians/<int:pk>/patient/all/', AllPhysicianPatientsListView.as_view(), name='all specific physician patients'),

    path('health_facility/create/', HealthFacilityCreation.as_view(), name='health facility register'),
    path('health_facility/<int:pk>/edit/', EditHealthFacility.as_view(), name='edit health facility'),
    path('health_facility/<int:pk>/delete/', delete_health_facility, name='delete health facility'),
    path('health_facility/<int:pk>/restore/', restore_health_facility, name='restore health facility'),
    path('health_facility/all/', HealthFacilityListView.as_view(), name='all health facilities'),
    path('health_facility/all_deleted/', DeletedHealthFacilityListView.as_view(), name='all deleted health facilities'),

    path('department/create/', DepartmentCreation.as_view(), name='department register'),
    path('department/<int:pk>/edit/', EditDepartment.as_view(), name='edit department'),
    path('department/<int:pk>/delete/', delete_department, name='delete department'),
    path('department/<int:pk>/restore/', restore_department, name='restore department'),
    path('department/all/', DepartmentsListView.as_view(), name='all departments'),
    path('department/all_deleted/', DeletedDepartmentsListView.as_view(), name='all deleted departments'),

    path('analysis_fields/create/', CreateAnalysisFieldView.as_view(), name='create analysis field'),
    path('analysis_fields/<int:pk>/edit/', EditAnalysisFieldView.as_view(), name='edit analysis field'),
    path('analysis_fields/<int:pk>/delete/', delete_analysis_field_view, name='delete analysis field'),
    path('analysis_fields/<int:pk>/restore/', restore_analysis_field_view, name='restore analysis field'),
    path('analysis_fields/all/', AnalysisFieldsListView.as_view(), name='all analysis fields'),
    path('analysis_fields/all_deleted/', DeletedAnalysisFieldsListView.as_view(), name='all deleted analysis fields'),

    path('analyses/create/', CreateAnalysisView.as_view(), name='create analysis'),
    path('analyses/<int:pk>/edit/', EditAnalysisView.as_view(), name='edit analysis'),
    path('analyses/<int:pk>/delete/', delete_analysis_view, name='delete analysis'),
    path('analyses/<int:pk>/restore/', restore_analysis_view, name='restore analysis'),
    path('analyses/all/', AnalysisListView.as_view(), name='all analyses'),
    path('analyses/all/search/', SearchAnalysesView.as_view(), name='all searched analyses'),
    path('analyses/all_deleted/', DeletedAnalysisListView.as_view(), name='all deleted analyses'),

    path('patient/<int:pk>/result/create/', CreateResultView.as_view(), name='add result to patient'),
    path('patient/<int:pk>/result/edit/', EditResultView.as_view(), name='edit result'),
    path('patient/<int:pk>/results/', PatientSpecificResultListView.as_view(), name='all patient specific results'),
    path('patient/<int:patient_pk>/results/<int:pk>/', ResultDetailsView.as_view(), name='result details'),

    path('resultline/<int:pk>/edit', EditResultLineView.as_view(), name='result line details'),
)

