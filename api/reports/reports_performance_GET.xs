// Download or retrieve consolidated student performance report data
query "reports/performance" verb=GET {
  api_group = "Reports"
  auth = "user"

  input {
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $user_subjects

    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id
      return = {type: "list"}
    } as $user_tasks
  }

  response = {
    user_id: $auth.id,
    subjects: $user_subjects,
    tasks: $user_tasks
  }
  tags = ["edutrack:reports"]
}
