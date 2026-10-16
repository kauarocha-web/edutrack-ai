// Get a single academic task by ID belonging to the authenticated user
query "academic_tasks/{id}" verb=GET {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int id
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
  }

  response = $task
  tags = ["edutrack:academic"]
  guid = "9WA6fIAV7p3tXRZaWS9zPc2yPOw"
}
