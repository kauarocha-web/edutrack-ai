// Delete an academic task belonging to the authenticated user
query "academic_tasks/{id}" verb=DELETE {
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

    db.del academic_tasks {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true, message: "Academic task successfully deleted."}
  tags = ["edutrack:academic"]
  guid = "R41AdXUfRId0qUGxdwxu6Tt4g8E"
}
