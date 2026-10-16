// Update an academic task belonging to the authenticated user
query "academic_tasks/{id}" verb=PATCH {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int id
    text? title filters=trim
    text? description filters=trim
    date? due_date
    text? status filters=trim
    int? subject_id
  }

  stack {
    db.query academic_tasks {
      where = ($db.academic_tasks.id == $input.id) && ($db.academic_tasks.user_id == $auth.id)
      return = {type: "single"}
    } as $task

    precondition ($task != null) {
      error_type = "notfound"
      error = "Academic task not found or does not belong to the authenticated user."
    }

    db.patch academic_tasks {
      field_name = "id"
      field_value = $input.id
      data = {
        title: $input.title
        description: $input.description
        due_date: $input.due_date
        status: $input.status
        subject_id: $input.subject_id
      }
    } as $updated_task
  }

  response = $updated_task
  tags = ["edutrack:academic"]
  guid = "It11h7s7cKQfThua7Gkm2IxfO9I"
}
