# subjects Specification

## Purpose
Permite a modelagem, integridade e persistência de dados das disciplinas acadêmicas (`subjects`) vinculadas aos usuários no EduTrack AI.

## Requirements

### Requirement: Subjects Table Schema
The system SHALL define and maintain the `subjects` table schema in XanoScript containing fields `id`, `name`, `teacher`, `hours`, and `user_id` referencing the `user` table.

#### Scenario: Valid subjects schema definition
- **WHEN** the `subjects` table schema is loaded from `tables/subjects.xs`
- **THEN** it SHALL contain an integer primary key `id`, text fields `name` and `teacher`, an integer field `hours`, and a foreign key `user_id` pointing to the `user` table

#### Scenario: Foreign key relationship to authentication user
- **WHEN** a subject record is created or updated with a `user_id`
- **THEN** `user_id` SHALL establish a reference to the `user` table representing the authenticated user in Xano
