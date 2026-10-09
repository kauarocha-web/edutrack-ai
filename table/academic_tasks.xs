// Stores academic tasks, assignments, and exams linked to subjects and users
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    text title filters=trim
    text? description filters=trim
    date? due_date
    text status?="pending" filters=trim

    // Reference to the subject
    int subject_id? {
      table = "subjects"
    }

    // Reference to the authenticated student/user
    int user_id? {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "due_date", op: "asc"}]}
    {type: "btree", field: [{name: "subject_id", op: "asc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
  ]
}
