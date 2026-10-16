// Create a new academic task for the authenticated user
query "academic_tasks" verb=POST {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    text title filters=trim
    text? description filters=trim
    date? due_date
    text? status?="pending" filters=trim
    int? subject_id
  }

  stack {
    db.add academic_tasks {
      data = {
        created_at: "now"
        title: $input.title
        description: $input.description
        due_date: $input.due_date
        status: $input.status
        subject_id: $input.subject_id
        user_id: $auth.id
      }
    } as $task
  }

  response = $task
  tags = ["edutrack:academic"]
  guid = "Iydx0ddyqZ21HnFIHkoK-UEonXg"
}
