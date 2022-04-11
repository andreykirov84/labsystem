# LIMS
Custom user model. All models are can be soft deleted (not realy deleted from the database, but deleted_at field is filled with Date and Time of "deletion". All softly deleted objects can be restored, with is important as this system is designed to store and process clinical data.
A Laboratory information management system project with some basic functionality:
  - register patients, physicians, lab staff, health facilities
  - create analysis fields and analysis
  - create new results for any patient (The correcsponding result lines are auto created after result creation signal 
